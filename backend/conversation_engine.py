"""
Conversation Intelligence & Scheme Eligibility Engine (MITRA AI)
================================================================
Implements:
  1. Multilingual Intent Classification:
     - GREETING
     - GENERAL_CONVERSATION
     - SCHEME_SEARCH
     - ELIGIBILITY_CHECK
     - SCHEME_DETAILS
     - APPLICATION_HELP
     - CLARIFICATION_REQUIRED
     - EMPLOYMENT_SEARCH (Jobs, Apprenticeships, Skilling)
     - SCHOLARSHIP_SEARCH (Education, Fees, Loans)
     - FARMER_ASSISTANCE (Crops, Rythu, PM-Kisan)
     - WOMEN_WELFARE (Girl Child, Maternal, Self-Help)
     - HEALTH_INSURANCE (Ayushman Bharat, Hospital)
     - HOUSING_FINANCE (PMAY, Home Loans, Rooftop Solar)
  2. Fact-Only Information Extraction:
     - User Name (e.g., Mokshagnateja)
     - State & District (28 States + 8 UTs)
     - Education (e.g., B.Tech, Degree, School)
     - Occupation (Student, Farmer, Vendor, Business, etc.)
     - Income, Landholding, Gender, Special Categories
     - Multi-turn conversation memory with user correction support.
  3. Context-Aware Grounded Response Generator:
     - Distinguishes students asking about employment from unemployed individuals.
     - Never returns hardcoded generic replies for specific citizen inquiries.
     - Progressive targeted clarifying questions before eligibility claims.
  4. Real AI / LLM Integration via ai_connector:
     - Connects to Google Gemini or OpenAI when API key is set in environment.
     - Transparently falls back to the deterministic context engine when offline.
     - Never claims an LLM is connected when no key is present.
  5. Deterministic Real-Database Scheme Evaluator with strict statuses:
     - 'Potential Match'
     - 'Additional Information Required'
     - 'Likely Does Not Match' (discarded)
  6. Relevancy & Honest Empty-State Enforcement.
"""
import re
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from .database import get_db_connection, row_to_dict, query_scheme_by_id
from .ai_connector import generate_ai_response, get_ai_config

logger = logging.getLogger(__name__)

# =====================================================================
# INTENT CONSTANTS
# =====================================================================
class IntentType:
    GREETING = "GREETING"
    GENERAL_CONVERSATION = "GENERAL_CONVERSATION"
    PROFILE_UPDATE = "PROFILE_UPDATE"
    SCHEME_SEARCH = "SCHEME_SEARCH"
    ELIGIBILITY_CHECK = "ELIGIBILITY_CHECK"
    SCHEME_DETAILS = "SCHEME_DETAILS"
    APPLICATION_HELP = "APPLICATION_HELP"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"
    EMPLOYMENT_SEARCH = "EMPLOYMENT_SEARCH"
    SCHOLARSHIP_SEARCH = "SCHOLARSHIP_SEARCH"
    FARMER_ASSISTANCE = "FARMER_ASSISTANCE"
    WOMEN_WELFARE = "WOMEN_WELFARE"
    HEALTH_INSURANCE = "HEALTH_INSURANCE"
    HOUSING_FINANCE = "HOUSING_FINANCE"


# =====================================================================
# ELIGIBILITY STATUS CONSTANTS
# =====================================================================
class EligibilityStatus:
    POTENTIAL_MATCH = "Potential Match"
    ADDITIONAL_INFO_REQUIRED = "Additional Information Required"
    LIKELY_DOES_NOT_MATCH = "Likely Does Not Match"


# =====================================================================
# INDIC TEXT NORMALIZATION & AUTOMATIC MULTILINGUAL DETECTION
# =====================================================================
def normalize_indic_text(text: str) -> str:
    """
    Normalize Indic (Telugu/Hindi) text by stripping Zero Width Non-Joiner (\u200c),
    Zero Width Joiner (\u200d), and soft hyphens (\u00ad), and trimming whitespace.
    """
    if not text:
        return ""
    return text.replace('\u200c', '').replace('\u200d', '').replace('\u00ad', '').strip().lower()


TANGLISH_MARKERS = {
    "nenu", "naaku", "naku", "kavali", "kaavali", "kavalenu", "vadhu", "vaddu",
    "ela", "elaga", "unnav", "unnavu", "unnaru", "unnadu", "unnadi", "undhi", "undi",
    "unnaya", "unnai", "unnayi", "unnam", "cheppu", "cheppandi", "telusuko", "telusukovali",
    "cheyali", "cheyyali", "vastunda", "vastundi", "chaduvuthunnanu", "chaduvutunna",
    "chaduvutunnanu", "chaduvukuntunna", "chadiva", "chadivina", "nerchukovali",
    "udyogam", "udyoga", "udyogalu", "raitu", "rythu", "raithu", "rythulu",
    "nirudyoga", "nirudyogi", "nirudyogula", "pathakam", "pathakalu", "pathakamu",
    "sahayam", "sahayamu", "dabbu", "dabbulu", "bhumi", "bhoomi", "illu", "panta", "pantalu",
    "aarogyam", "arogyam", "kutumbam", "kosam", "gurinchi", "mariyu", "kani", "bagunnara", "baagunnara"
}

HINGLISH_MARKERS = {
    "mujhe", "humko", "hamko", "chahiye", "kaise", "kya", "batao", "batayein", "bataiye",
    "karen", "kare", "yojana", "yojanaye", "sarkari", "naukri", "madad", "paise", "kisan",
    "chahie", "sahayata"
}


def detect_message_language(text: str, fallback_lang: str = "en") -> Tuple[str, bool]:
    """
    Automatically detects if a message is Telugu (script or Tanglish),
    Hindi (script or Hinglish), or English.
    Returns: (lang_code: 'te' | 'hi' | 'en', is_romanized: bool)
    """
    norm = normalize_indic_text(text)
    # 1. Telugu Unicode script
    if re.search(r'[\u0C00-\u0C7F]', text):
        return 'te', False
    # 2. Hindi / Devanagari Unicode script
    if re.search(r'[\u0900-\u097F]', text):
        return 'hi', False
    # 3. Tokenize words for Romanized Indic checks
    words = set(re.findall(r'[a-zA-Z]+', norm))
    te_matches = words.intersection(TANGLISH_MARKERS)
    if ('lo' in words or 'ki' in words or 'ku' in words) and (te_matches or 'schemes' in words or 'unemployed' in words or 'youth' in words or 'government' in words or 'job' in words):
        te_matches.add('particle')

    hi_matches = words.intersection(HINGLISH_MARKERS)

    if len(te_matches) >= 1:
        return 'te', True
    if len(hi_matches) >= 1:
        return 'hi', True

    return (fallback_lang if fallback_lang in ['en', 'te', 'hi'] else 'en'), False


# =====================================================================
# SYNONYM & LOCATION DICTIONARIES
# =====================================================================
INDIAN_STATES_SYNONYMS = {
    "Andhra Pradesh": ["andhra pradesh", "andhra", "ap", "ఆంధ్రప్రదేశ్", "ఆంధ్ర", "आंध्र प्रदेश", "आंध्र"],
    "Arunachal Pradesh": ["arunachal pradesh", "arunachal", "అరుణాచల్", "अरुणाचल"],
    "Assam": ["assam", "asom", "అస్సాం", "असम"],
    "Bihar": ["bihar", "బీహార్", "बिहार"],
    "Chhattisgarh": ["chhattisgarh", "chhatisgarh", "ఛత్తీస్‌గఢ్", "छत्तीसगढ़"],
    "Goa": ["goa", "గోవా", "गोवा"],
    "Gujarat": ["gujarat", "గుజరాత్", "गुजरात"],
    "Haryana": ["haryana", "హర్యానా", "हरियाणा"],
    "Himachal Pradesh": ["himachal pradesh", "himachal", "hp", "హిమాచల్", "हिमाचल"],
    "Jharkhand": ["jharkhand", "జార్ఖండ్", "झारखंड"],
    "Karnataka": ["karnataka", "కర్ణాటక", "कर्नाटक"],
    "Kerala": ["kerala", "కేరళ", "केरल"],
    "Madhya Pradesh": ["madhya pradesh", "mp", "మధ్యప్రదేశ్", "मध्य प्रदेश", "एमपी"],
    "Maharashtra": ["maharashtra", "మహారాష్ట్ర", "महाराष्ट्र"],
    "Manipur": ["manipur", "మణిపూర్", "मणिपुर"],
    "Meghalaya": ["meghalaya", "మేఘాలయ", "मेघालय"],
    "Mizoram": ["mizoram", "మిజోరం", "मिजोरम"],
    "Nagaland": ["nagaland", "నాగాలాండ్", "नागालैंड"],
    "Odisha": ["odisha", "orissa", "ఒడిశా", "ओडिशा", "उड़ीसा"],
    "Punjab": ["punjab", "పంజాబ్", "पंजाब"],
    "Rajasthan": ["rajasthan", "రాజస్థాన్", "राजस्थान"],
    "Sikkim": ["sikkim", "సిక్కిం", "सिक्किम"],
    "Tamil Nadu": ["tamil nadu", "tamilnadu", "tamil", "tn", "తమిళనాడు", "तमिलनाडु", "तमिल"],
    "Telangana": ["telangana", "tg", "ts", "తెలంగాణ", "तेलंगाना"],
    "Tripura": ["tripura", "త్రిపుర", "त्रिपुरा"],
    "Uttar Pradesh": ["uttar pradesh", "up", "ఉత్తర ప్రదేశ్", "उत्तर प्रदेश", "यूपी"],
    "Uttarakhand": ["uttarakhand", "uttaranchal", "ఉత్తరాఖండ్", "उत्तराखंड"],
    "West Bengal": ["west bengal", "bengal", "wb", "పశ్చిమ బెంగాల్", "पश्चिम बंगाल", "बंगाल"],
    # Union Territories
    "Andaman and Nicobar Islands": ["andaman", "nicobar", "అండమాన్", "अंडमान"],
    "Chandigarh": ["chandigarh", "చండీగఢ్", "चंडीगढ़"],
    "Dadra and Nagar Haveli and Daman and Diu": ["daman", "diu", "dadra", "नगर हवेली", "दमन"],
    "Delhi": ["delhi", "new delhi", "nct", "ఢిల్లీ", "दिल्ली", "नई दिल्ली"],
    "Jammu and Kashmir": ["jammu and kashmir", "jammu", "kashmir", "j&k", "జమ్మూ", "कश्मीर", "जम्मू"],
    "Ladakh": ["ladakh", "leh", "kargil", "లడఖ్", "लद्दाख"],
    "Lakshadweep": ["lakshadweep", "లక్షద్వీప్", "लक्षद्वीप"],
    "Puducherry": ["puducherry", "pondicherry", "పాండిచ్చేరి", "పుదుచ్చేరి", "पुदुचेरी", "पांडिचेरी"]
}

OCCUPATION_SYNONYMS = {
    "farmer": [
        "farmer", "farmers", "cultivator", "agriculture", "agricultural", "farming",
        "crop", "crops", "kisan", "rythu", "kisano", "agri",
        "రైతు", "రైతులు", "వ్యవసాయం", "కౌలు రైతు", "భూమి",
        "किसान", "खेती", "खेतिहर", "कृषि", "अन्नदाता"
    ],
    "student": [
        "student", "students", "scholar", "studying", "college", "school",
        "university", "scholarship", "scholarships", "fee", "tuition", "hostel",
        "degree", "undergraduate", "postgraduate", "btech", "b.tech", "bsc", "bcom", "intermediate", "class 10", "class 12",
        "విద్యార్థి", "విద్యార్థులు", "చదువు", "స్కాలర్‌షిప్", "హాస్టల్",
        "छात्र", "छात्रा", "विद्यार्थी", "पढ़ाई", "छात्रवृत्ति", "कॉलेज", "स्कूल"
    ],
    "vendor": [
        "vendor", "vendors", "street vendor", "hawker", "hawkers", "shopkeeper",
        "artisan", "cobbler", "barber", "tailor", "cart",
        "వీధి వ్యాపారి", "చిరు వ్యాపారి", "చేతివృత్తులు",
        "स्ट्रीट वेंडर", "फेरीवाले", "ठेले", "दुकानदार", "कारीगर"
    ],
    "business": [
        "business", "entrepreneur", "msme", "micro enterprise", "small business",
        "startup", "trader", "shop", "enterprise", "commercial",
        "వ్యాపారం", "చిన్న వ్యాపారం", "పరిశ్రమ", "ఎంఎస్ఎంఈ",
        "व्यापार", "व्यवसाय", "उद्यमी", "एमएसएमई", "स्टार्टअप"
    ],
    "unorganized": [
        "daily wage", "construction worker", "labourer", "worker", "unorganized",
        "coolie", "driver", "rickshaw", "helper",
        "దినసరి కూలీ", "భవన నిర్మాణ కార్మికుడు", "కూలీ",
        "दैनिक वेतनभोगी", "मजदूर", "श्रमिक", "असंगठित"
    ],
    "senior": [
        "senior", "senior citizen", "retired", "pension", "pensioner", "elderly", "old age",
        "వృద్ధు", "వృద్ధులు", "సీనియర్ సిటిజన్", "పెన్షన్", "పదవీ విరమణ",
        "वरिष्ठ नागरिक", "बुजुर्ग", "पेंशन", "पेंशनभोगी", "वृद्धावस्था"
    ],
    "unemployed": [
        "job seeker", "seeking job", "unemployment", "youth looking for job", "without job",
        "నిరుద్యోగి", "నిరుద్యోగులు", "ఉద్యోగార్ధి",
        "बेरोजगार", "बेरोजगारी", "नौकरी चाहने वाले"
    ]
}

CATEGORY_NEED_KEYWORDS = {
    "education": ["scholarship", "scholarships", "education", "study", "fee", "college", "school", "exam", "coaching", "admission", "స్కాలర్‌షిప్", "విద్య", "छात्रवृत्ति", "शिक्षा"],
    "employment": ["employment", "job", "jobs", "internship", "apprenticeship", "career", "skill development", "skill india", "placement", "unemployment", "ఉద్యోగం", "ఉపాధి", "నైపుణ్యం", "रोजगार", "नौकरी"],
    "agriculture": ["farmer", "farming", "crop", "seeds", "fertilizer", "tractor", "cultivation", "land", "rythu", "kisan", "వ్యవసాయం", "రైతు", "कृषि", "किसान"],
    "health": ["health", "hospital", "medical", "treatment", "ayushman", "disease", "surgery", "medicine", "ఆరోగ్యం", "చికిత్స", "ఆసుపత్రి", "स्वास्थ्य", "इलाज", "अस्पताल"],
    "business": ["loan", "loans", "mudra", "business", "capital", "subsidy", "msme", "startup", "రుణం", "వ్యాపారం", "ऋण", "लोन", "व्यापार"],
    "women": ["women", "woman", "girl", "daughter", "widow", "mother", "female", "sukanya", "మహిళ", "స్త్రీ", "బాలిక", "ఆడపిల్ల", "महिला", "बेटी", "लड़की", "कन्या"],
    "housing": ["house", "housing", "awas", "home", "shelter", "ఇల్లు", "గృహం", "आवास", "मकान", "घर"],
    "energy": ["solar", "electricity", "energy", "rooftop", "bijli", "సౌర", "విద్యుత్", "सौर", "बिजली"],
    "social": ["pension", "pensions", "disability", "divyang", "senior", "pensioner", "పెన్షన్", "దివ్యాంగులు", "पेंशन", "दिव्यांग"]
}


# =====================================================================
# IN-MEMORY SESSION STORE (TTL / Process-Safe)
# =====================================================================
SESSION_STORE: Dict[str, Dict[str, Any]] = {}


def get_or_create_session(session_id: Optional[str], initial_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Retrieve or initialize an active multi-turn conversation session."""
    sid = session_id or "default_session"
    if sid not in SESSION_STORE:
        SESSION_STORE[sid] = {
            "session_id": sid,
            "profile": {
                "user_name": None,
                "state": None,
                "district": None,
                "age": None,
                "occupation": None,
                "income": None,
                "education": None,
                "gender": None,
                "land": None,
                "land_acres": None,
                "has_girl_child": None,
                "has_bpl": None,
                "disability": None,
                "social_category": None,
                "category_need": None,
                "specific_scheme_id": None
            },
            "last_intent": None,
            "pending_question_topic": None,
            "history": []
        }

    session = SESSION_STORE[sid]
    if initial_profile and isinstance(initial_profile, dict):
        for k, v in initial_profile.items():
            if v is not None and k in session["profile"]:
                session["profile"][k] = v

    return session


def clear_session(session_id: Optional[str]) -> None:
    """Clear conversation session memory when user clicks Clear Chat."""
    sid = session_id or "default_session"
    if sid in SESSION_STORE:
        del SESSION_STORE[sid]


# =====================================================================
# 1. INTENT CLASSIFICATION
# =====================================================================
def classify_intent(message: str, session: Dict[str, Any]) -> str:
    """
    Classify the user message into canonical context-aware intents.
    Accurately recognizes employment, scholarships, scheme details, farmer needs, and small talk.
    """
    m = normalize_indic_text(message)

    # 1. Check for single-word or pure greetings & Tanglish greetings (e.g. "Hi", "Hello", "Hi, this is Mokshagna")
    greeting_patterns = [
        r"^(hi|hello|hey|namaste|namaskar|namaskaram|greetings|good\s*(morning|afternoon|evening|day))(\s*,?\s*(this\s+is|i\s+am|mitra|assistant|there|team|sir|madam)?\s*[A-Za-z\u0C00-\u0C7F\u0900-\u097F]*)?[!.]*$",
        r"^(హలో|నమస్కారం|నమస్తే|బాగున్నారా)[!.]*$",
        r"^(नमस्ते|नमस्कार|हेलो|हाय|प्रणाम)[!.]*$",
        r"^(hi\s*,?\s*)?(ela\s*unnav|ela\s*unnaru|bagunnara|baagunnara)[!?. ]*$",
        r"^(hi\s*,?\s*)?(kaise\s*ho|kaise\s*hain)[!?. ]*$"
    ]
    for pat in greeting_patterns:
        if re.match(pat, m, re.IGNORECASE):
            return IntentType.GREETING

    # 2. Check for general polite conversation / identity / small talk
    general_conv_patterns = [
        r"^.*\b(how\s+are\s+you|who\s+are\s+you|what\s+is\s+your\s+name|what\s+can\s+you\s+do|what\s+do\s+you\s+do|tell\s+me\s+about\s+yourself|are\s+you\s+(an?\s+)?ai|thank\s*you|thanks|nice\s+to\s+meet\s+you)\b.*$",
        r"^.*\b(ela\s*unnav|ela\s*unnaru|bagunnara|baagunnara|ఎలా\s*ఉన్నారు|ఎలా\s*ఉన్నావు|మీరు\s*ఎవరు|ధన్యవాదాలు|థాంక్స్)\b.*$",
        r"^.*\b(आप\s*कैसे\s*हैं|आप\s*कौन\s*हैं|तुम्हारा\s*नाम\s*क्या\s*है|धन्यवाद|शुक्रिया|kaise\s*ho|kaise\s*hain)\b.*$"
    ]
    for pat in general_conv_patterns:
        if re.search(pat, m, re.IGNORECASE):
            return IntentType.GENERAL_CONVERSATION

    # 3. Check for obvious out-of-scope / unrelated questions
    unrelated_triggers = [
        "capital of", "weather in", "bake a cake", "make tea", "recipe for",
        "write a poem", "solve math", "who won", "cricket score", "movie review",
        "who is president of", "prime minister of uk", "write python code"
    ]
    if any(trigger in m for trigger in unrelated_triggers) and not any(k in m for k in ["scheme", "yojana", "benefit", "scholarship", "loan", "farmer", "పథకం"]):
        return IntentType.GENERAL_CONVERSATION

    # 4. Check for PROFILE_UPDATE (Profile Information supplied without explicit search action)
    search_triggers = [
        "find", "search", "show me", "show schemes", "show", "give me", "list", "apply for", "how to apply",
        "looking for", "need", "want",
        "eligible for", "am i eligible", "check eligibility", "details",
        "కావాలి", "చూపించు", "చూపండి", "చెప్పు",
        "चाहिए", "दिखाओ", "दिखाइए", "बताओ", "खोजो"
    ]
    has_search_action = any(trig in m for trig in search_triggers)


    profile_declarations = [
        r"^(my\s+name\s+is|name\s+is|this\s+is|నా\s*పేరు|मेरा\s*नाम)\b",
        r"^i\s+am\s+(a\s+)?(student|b\.?tech|engineering|degree|graduate|unemployed|farmer|vendor|artisan|worker|\d{1,3}\b)",
        r"^i\s+am\s+\d{1,3}\s*(years\s+old|and\s+unemployed)?",
        r"^my\s+age\s+is\s+\d{1,3}",
        r"^nenu\s+(b\.?tech|student|nirudyogi|unemployed|raitu|chaduvuthunnanu|\d{1,3})",
        r"^నేను\s+(విద్యార్థి|చదువుతున్నా|రైతు|నిరుద్యోగి|\d{1,3})",
        r"^मैं\s+(छात्र|बेरोजगार|किसान|\d{1,3})"
    ]
    if not has_search_action and any(re.search(pat, m, re.IGNORECASE) for pat in profile_declarations):
        return IntentType.PROFILE_UPDATE

    # Application & Document guidance triggers
    application_triggers = [
        "how to apply", "how do i apply", "where to apply", "application process", "apply link",
        "documents required", "required documents", "what documents", "documents needed", "which documents", "documents for",
        "official link", "application link", "official application link", "portal link", "portal url",
        "official website", "website link", "apply online", "online application", "give me the link", "share the link",
        "tell me the documents", "documents required for this", "official application link",
        "आवेदन कैसे करें", "आवेदन प्रक्रिया", "दस्तावेज", "दस्तावेज़", "आवेदन लिंक", "आधिकारिक लिंक", "पोर्टल लिंक",
        "ఎలా దరఖాస్తు చేయాలి", "దరఖాస్తు విధానం", "కావలసిన పత్రాలు", "పత్రాలు", "దరఖాస్తు లింక్", "అధికారిక లింక్", "పోర్టల్ లింక్",
        "documents kavali", "documents cheppu", "documents enti", "patralu kavali", "patralu cheppu",
        "link kavali", "link cheppu", "link ivvandi"
    ]

    # 5. Check for Specific Scheme Inquiries (Details / Documents / Link lookup)
    scheme_name_triggers = [
        ("pm-kisan", ["pm kisan", "pm-kisan", "kisan samman", "పీఎం కిసాన్", "पीएम किसान"]),
        ("nsp-scholarship", ["nsp", "national scholarship", "national scholarship portal", "కేంద్ర స్కాలర్‌షిప్", "राष्ट्रीय छात्रवृत्ति"]),
        ("ayushman-bharat", ["ayushman bharat", "pmjay", "pm-jay", "jan arogya", "ఆయుష్మాన్ భారత్", "आयुष्मान भारत"]),
        ("pm-mudra", ["mudra", "pm mudra", "mudra loan", "ముద్రా లోన్", "मुद्रा लोन"]),
        ("vidya-lakshmi", ["vidya lakshmi", "vidyalakshmi", "విద్యాలక్ష్మి", "विद्या लक्ष्मी"]),
        ("pm-svanidhi", ["svanidhi", "pm svanidhi", "street vendor loan", "స్వనిధి", "स्वनिधि"]),
        ("sukanya-samriddhi", ["sukanya", "sukanya samriddhi", "సుకున్య సమృద్ధి", "सुकन्या समृद्धि"]),
        ("rythu-bharosa-bandhu", ["rythu bharosa", "rythu bandhu", "రైతు భరోసా", "రైతు బంధు", "रयथु भरोसा"]),
        ("atal-pension-yojana", ["atal pension", "apy", "అటల్ పెన్షన్", "अटल पेंशन"]),
        ("pmay-urban-gramin", ["pmay", "awas yojana", "pm awas", "ఆవాస్ యోజన", "आवास योजना"]),
        ("pm-surya-ghar", ["surya ghar", "muft bijli", "solar rooftop", "సూర్య ఘర్", "सूर्य घर"])
    ]
    for scheme_id, aliases in scheme_name_triggers:
        if any(alias in m for alias in aliases):
            session["profile"]["specific_scheme_id"] = scheme_id
            if any(trig in m for trig in application_triggers):
                return IntentType.APPLICATION_HELP
            return IntentType.SCHEME_DETAILS

    if any(trig in m for trig in application_triggers):
        return IntentType.APPLICATION_HELP

    if any(q in m for q in ["tell me about this scheme", "about this scheme", "scheme details", "explain this scheme", "ఈ పథకం గురించి", "इस योजना के बारे में"]):
        return IntentType.SCHEME_DETAILS


    # 5. Check for Scholarships, Student Benefits, Education Loans
    scholarship_keywords = [
        "scholarship", "scholarships", "fee reimbursement", "tuition fee", "vidya lakshmi", "student grant",
        "scholarships in india", "education loan", "study assistance", "స్కాలర్షిప్", "స్కాలర్‌షిప్", "ఫీజు రీయింబర్స్‌మెంట్",
        "చదువు", "విద్యార్థి", "छात्रवृत्ति", "स्कॉलरशिप", "फीस प्रतिपूर्ति",
        "scholarships unnaya", "scholarship kavali", "chaduvuthunnanu", "chaduvutunna", "chaduvutunnanu", "chaduvukuntunna"
    ]
    if any(k in m for k in scholarship_keywords):
        return IntentType.SCHOLARSHIP_SEARCH

    # 6. Check for Employment, Jobs, Internships, Skill Development
    employment_keywords = [
        "employment", "unemployment", "unemployed", "jobless", "job", "jobs", "internship", "internships", "career",
        "skill development", "skill india", "pmkvy", "nats", "apprenticeship", "placement", "placement opportunities",
        "employment schemes", "job schemes", "opportunities in india", "unemployed youth", "youth",
        "ఉద్యోగం", "ఉపాధి", "నైపుణ్యం", "నిరుద్యోగ", "నిరుద్యోగులు",
        "रोजगार", "नौकरी", "बेरोजगारी", "कौशल विकास", "अप्रेन्टिसशिप",
        "udyogam", "udyoga", "udyogalu", "nirudyoga", "nirudyogi", "nirudyogula",
        "schemes cheppu", "government job", "government job schemes"
    ]
    if any(k in m for k in employment_keywords):
        return IntentType.EMPLOYMENT_SEARCH

    # 7. Check for Farmer Assistance
    farmer_keywords = [
        "farmer", "farmers", "farming", "crop", "crops", "agriculture", "cultivator", "rythu", "kisan",
        "వ్యవసాయం", "రైతు", "రైతులు", "కౌలు రైతు", "భూమి", "किसान", "खेती", "कृषि"
    ]
    if any(k in m for k in farmer_keywords) and any(need in m for need in ["scheme", "schemes", "benefit", "subsidy", "help", "assistance", "support", "from", "in", "కావాలి", "సహాయం", "योजना", "चाहिए"]):
        return IntentType.FARMER_ASSISTANCE

    # 8. Check for Women's Welfare
    women_keywords = [
        "women", "woman", "girl child", "daughter", "maternal", "pregnant", "widow", "mahila", "sukanya", "ladli",
        "మహిళ", "స్త్రీ", "బాలిక", "ఆడపిల్ల", "महिला", "बेटी", "लड़की"
    ]
    if any(k in m for k in women_keywords) and any(w in m for w in ["scheme", "benefit", "yojana", "help", "పథకం", "योजना"]):
        return IntentType.WOMEN_WELFARE

    # 9. Check for Health & Medical Insurance
    health_keywords = [
        "health", "hospital", "ayushman", "pmjay", "medical", "treatment", "surgery", "insurance",
        "ఆరోగ్యం", "ఆసుపత్రి", "చికిత్స", "स्वास्थ्य", "अस्पताल", "इलाज", "बीमा"
    ]
    if any(k in m for k in health_keywords) and any(w in m for w in ["scheme", "benefit", "card", "cover", "help", "పథకం", "योजना"]):
        return IntentType.HEALTH_INSURANCE

    # 10. Check for Housing & Financial Aid
    housing_keywords = [
        "house", "housing", "pmay", "awas", "home loan", "rooftop solar", "surya ghar", "mudra loan",
        "ఇల్లు", "ఆవాస్", "సౌర", "मकान", "आवास", "घर", "सौर ऊर्जा"
    ]
    if any(k in m for k in housing_keywords):
        return IntentType.HOUSING_FINANCE

    # 11. Check for Eligibility Checking
    eligibility_triggers = [
        "am i eligible", "check my eligibility", "can i get", "am i qualified",
        "check eligibility", "who is eligible", "do i qualify",
        "నాకు పథకం వస్తుందా", "అర్హత ఉందా", "నా అర్హత తనిఖీ చేయండి",
        "क्या मैं पात्र हूँ", "पात्रता जांचें", "क्या मुझे मिल सकता है"
    ]
    if any(trig in m for trig in eligibility_triggers):
        return IntentType.ELIGIBILITY_CHECK

    # 13. Check if user is in an active clarification dialogue
    if session.get("pending_question_topic") is not None:
        return IntentType.CLARIFICATION_REQUIRED

    # 14. Check for General Scheme Search / Need Expression
    search_keywords = [
        "need", "want", "looking for", "find", "search", "give me", "show me", "available", "apply for",
        "schemes", "scheme", "government schemes", "welfare programs", "financial assistance", "subsidy", "grant",
        "పథకం", "పథకాలు", "కావాలి", "రుణం",
        "योजना", "योजनाएं", "चाहिए", "लोन", "सहायता"
    ]
    if any(word in m for word in search_keywords):
        return IntentType.SCHEME_SEARCH

    # Default fallback
    return IntentType.GENERAL_CONVERSATION


# =====================================================================
# 2. FACT-ONLY INFORMATION EXTRACTION
# =====================================================================
def extract_user_information(message: str, current_profile: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """
    Extract ONLY facts genuinely provided in the user's message.
    Preserves existing session state and accurately logs user corrections.
    """
    m = normalize_indic_text(message)
    updated = dict(current_profile)
    corrections: List[str] = []

    # --- 0. User Name Extraction ---
    # Matches: 'My name is Mokshagna Teja', 'Hi, this is Mokshagna', 'Name is Rahul Sharma', 'నా పేరు మోక్షజ్ఞ తేజ'
    name_match = re.search(
        r"\b(?:my\s+name\s+is|name\s+is|this\s+is|i\s+am|నా\s*పేరు|నాపేరు|मेरा\s*नाम|नाम\s*है)\s+([A-Za-z\u0C00-\u0C7F\u0900-\u097F]+(?:\s+[A-Za-z\u0C00-\u0C7F\u0900-\u097F]+){0,2})",
        message,
        re.IGNORECASE
    )
    if name_match:
        cand_name = name_match.group(1).strip().rstrip(".,!?")
        cand_first = cand_name.split()[0].lower()
        stopwords = [
            "a", "an", "the", "farmer", "student", "seeking", "looking", "here", "studying",
            "from", "working", "btech", "engineering", "unemployed", "18", "years", "old",
            "in", "living", "resident", "citizen", "doing", "pursuing"
        ]
        if cand_first not in stopwords and len(cand_name) >= 2:
            if updated.get("user_name") and updated["user_name"].lower() != cand_name.lower():
                corrections.append(f"Name updated to {cand_name}")
            updated["user_name"] = cand_name

    # --- 1. State & Union Territory Extraction ---
    for state_name, synonyms in INDIAN_STATES_SYNONYMS.items():
        matched = False
        for syn in synonyms:
            syn_norm = normalize_indic_text(syn)
            if syn_norm.isascii():
                if re.search(rf"\b{re.escape(syn_norm)}\b", m):
                    matched = True
                    break
            else:
                if syn_norm in m:
                    matched = True
                    break
        if matched:
            if updated.get("state") and updated["state"] != state_name:
                corrections.append(f"State corrected from {updated['state']} to {state_name}")
            updated["state"] = state_name
            break

    # --- 2. Education Extraction ---
    education_terms = [
        ("B.Tech (Engineering)", ["btech", "b.tech", "b tech", "engineering", "b.e.", "b.e", "బిటెక్", "బీటెక్", "बीटेक", "इंजीनियरिंग"]),
        ("Postgraduate / Masters", ["mtech", "m.tech", "msc", "m.sc", "mba", "postgraduate", "pg", "पीजी", "एमटेक"]),
        ("Undergraduate / Degree", ["bsc", "b.sc", "bcom", "b.com", "ba", "degree", "undergraduate", "ug", "డిగ్రీ", "ग्रेजुएशन"]),
        ("Intermediate / +2", ["intermediate", "inter", "class 12", "12th", "ఇంటర్", "12वीं", "इंटर"]),
        ("School / Class 10", ["class 10", "10th", "school", "high school", "పాఠశాల", "10वीं"]),
        ("Diploma / Polytechnic", ["diploma", "polytechnic", "డిప్లొమా", "डिप्लोमा"])
    ]
    for edu_key, syns in education_terms:
        matched_edu = False
        for s in syns:
            s_norm = normalize_indic_text(s)
            if s_norm.isascii():
                if re.search(rf"\b{re.escape(s_norm)}\b", m):
                    matched_edu = True
                    break
            else:
                if s_norm in m:
                    matched_edu = True
                    break
        if matched_edu:
            if updated.get("education") and updated["education"] != edu_key:
                corrections.append(f"Education updated to {edu_key}")
            updated["education"] = edu_key
            # If user states they are studying, mark occupation as student and need as education
            if any(w in m for w in ["study", "studying", "student", "pursuing", "chaduvuthunnanu", "chaduvutunna", "chaduvutunnanu", "చదువుతున్నాను", "చదువుతున్నా", "చదువు"]):
                updated["occupation"] = "student"
                if not updated.get("category_need"):
                    updated["category_need"] = "education"
            break

    # --- 3. Occupation Extraction ---
    # Only assign unemployed if user says "I am unemployed", "18 and unemployed", etc.
    is_explicitly_unemployed = any(k in m for k in [
        "i am unemployed", "currently unemployed", "lost my job", "jobless",
        "నిరుద్యోగిని", "నిరుద్యోగి", "nenu unemployed", "nenu nirudyogi", "बेरोजगार हूँ"
    ]) or bool(re.search(r"\b(?:unemployed|jobless|job\s*seeker)\b|నిరుద్యోగ|నిరుద్యోగి|बेरोजगार", m, re.IGNORECASE))

    if is_explicitly_unemployed:
        updated["occupation"] = "unemployed"
        if not updated.get("category_need"):
            updated["category_need"] = "employment"
    else:
        for occ_key, synonyms in OCCUPATION_SYNONYMS.items():
            if occ_key == "unemployed":
                continue # Handled via explicit phrasing above
            matched_occ = False
            for syn in synonyms:
                if syn.isascii():
                    if re.search(rf"\b{re.escape(syn)}\b", m):
                        matched_occ = True
                        break
                else:
                    if syn in m:
                        matched_occ = True
                        break
            if matched_occ:
                if updated.get("occupation") and updated["occupation"] != occ_key:
                    corrections.append(f"Occupation corrected from {updated['occupation']} to {occ_key}")
                updated["occupation"] = occ_key
                if occ_key == "student" and not updated.get("category_need"):
                    updated["category_need"] = "education"
                elif occ_key == "farmer" and not updated.get("category_need"):
                    updated["category_need"] = "agriculture"
                break

    # --- 4. Age Extraction ---
    age_patterns = [
        r"(?:age(?:\s*is|\s*:)?\s*|i\s*am\s*(?:an?\s+)?|నేను\s*|నా\s*వయస్సు\s*|मेरी\s*उम्र\s*)(\d{1,3})\s*(?:years?\s*old|yrs?\s*old|years?|yrs?|year|ఏళ్ళు|సంవత్సరాలు|సంవత్సరాల|वर्ष|साल)?",
        r"(\d{1,3})\s*(?:years?\s*old|yrs?\s*old|years?|yrs?|ఏళ్ళు|సంవత్సరాలు|సంవత్సరాల|वर्ष|साल)"
    ]
    for pat in age_patterns:
        match = re.search(pat, m, re.IGNORECASE)
        if match:
            val = int(match.group(1))
            if 1 <= val <= 115:
                if updated.get("age") and updated["age"] != val:
                    corrections.append(f"Age corrected from {updated['age']} to {val}")
                updated["age"] = val
                break

    # --- 5. Income Extraction ---
    income_lakh_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs|lpa|లక్ష|లక్షలు|लाख)", m)
    if income_lakh_match:
        val = float(income_lakh_match.group(1)) * 100000
        val_int = int(val)
        if updated.get("income") and abs(updated["income"] - val_int) > 500:
            corrections.append(f"Income corrected to Rs.{val_int:,}")
        updated["income"] = val_int
    else:
        num_income_match = re.search(r"(?:rs\.?|₹|inr|income(?:\s*is|\s*:)?|salary(?:\s*is|\s*:)?)\s*(\d[\d,]*\d|\d{4,9})\b", m)
        if num_income_match:
            raw_num = num_income_match.group(1).replace(",", "")
            val_int = int(raw_num)
            if 1000 <= val_int <= 500000000:
                if updated.get("income") and abs(updated["income"] - val_int) > 500:
                    corrections.append(f"Income corrected to Rs.{val_int:,}")
                updated["income"] = val_int

    # --- 6. Land Ownership Extraction ---
    land_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:acre|acres|hectare|hectares|ఎకరా|ఎకరాలు|एकड़|हेक्टेयर)", m)
    if land_match:
        acres = float(land_match.group(1))
        updated["land_acres"] = acres
        if acres <= 2.5:
            updated["land"] = "marginal"
        elif acres <= 5.0:
            updated["land"] = "small"
        else:
            updated["land"] = "large"
    elif any(k in m for k in ["no land", "landless", "భూమి లేదు", "జమీన్ లేదు", "भूमिहीन", "जमीन नहीं"]):
        updated["land"] = "none"
        updated["land_acres"] = 0.0

    # --- 7. Gender Extraction ---
    if any(k in m for k in ["female", "woman", "women", "girl", "daughter", "widow", "స్త్రీ", "మహిళ", "బాలిక", "महिला", "लड़की", "बेटी"]):
        updated["gender"] = "female"
    elif any(k in m for k in ["male", "man", "boy", "son", "పురుషుడు", "బాలుడు", "पुरुष", "लड़का"]):
        if updated.get("gender") != "female":
            updated["gender"] = "male"

    # --- 8. Category Need Tagging ---
    for cat_name, keywords in CATEGORY_NEED_KEYWORDS.items():
        matched_cat = False
        for kw in keywords:
            if kw.isascii():
                if re.search(rf"\b{re.escape(kw)}\b", m):
                    matched_cat = True
                    break
            else:
                if kw in m:
                    matched_cat = True
                    break
        if matched_cat:
            updated["category_need"] = cat_name
            break

    # --- 9. Special Inclusions (BPL / Girl Child / Disability) ---
    if any(k in m for k in ["bpl", "ration card", "white ration card", "antyodaya", "రేషన్ కార్డు", "రాషన్ కార్డు", "बीपीएल", "राशन कार्ड"]):
        updated["has_bpl"] = True
    if any(k in m for k in ["girl child", "daughter under 10", "10 years daughter", "ఆడపిల్ల ఉంది", "చిన్న కుమార్తె", "बेटी है"]):
        updated["has_girl_child"] = True
    if any(k in m for k in ["disability", "disabled", "divyang", "divyangjan", "handicap", "దివ్యాంగులు", "దివ్యాంగ్", "दिव्यांग"]):
        updated["disability"] = "yes"

    return updated, corrections


# =====================================================================
# 3. CONCISE TARGETED FOLLOW-UP QUESTION GENERATOR
# =====================================================================
def generate_follow_up_question(profile: Dict[str, Any], lang: str = "en") -> Optional[str]:
    """
    Generate progressive, concise questions when essential eligibility information is missing.
    Never asks for all details at once.
    """
    cat = profile.get("category_need")
    occ = profile.get("occupation")
    state = profile.get("state")
    land = profile.get("land")
    income = profile.get("income")
    education = profile.get("education")

    # A. Student / Scholarship
    if cat == "education" or occ == "student":
        if not education and not state:
            if lang == "te":
                return "మీరు ప్రస్తుతం ఏం చదువుతున్నారు? ఏ కోర్సు మరియు ఏ రాష్ట్రంలో చదువుతున్నారు?"
            elif lang == "hi":
                return "आप वर्तमान में क्या पढ़ाई कर रहे हैं? आप किस कक्षा/कोर्स और किस राज्य में पढ़ रहे हैं?"
            return "Are you currently studying? Which course or class and in which State are you studying?"
        elif not state:
            if lang == "te":
                return "మీరు ఏ రాష్ట్రంలో చదువుతున్నారు లేదా నివసిస్తున్నారు?"
            elif lang == "hi":
                return "आप किस राज्य में पढ़ाई कर रहे हैं या रहते हैं?"
            return "Which State or Union Territory do you reside or study in?"
        elif not education:
            if lang == "te":
                return "మీ ప్రస్తుత చదువు ఏమిటి (ఉదా: 10వ తరగతి, ఇంటర్, లేదా డిగ్రీ)?"
            elif lang == "hi":
                return "आपकी वर्तमान पढ़ाई क्या है (जैसे 10वीं, 12वीं या डिग्री)?"
            return "What level or course are you currently enrolled in (e.g., School, Intermediate, or Degree)?"
        elif income is None:
            if lang == "te":
                return "మీ కుటుంబ వార్షిక ఆదాయం ఎంతవరకు ఉంటుంది?"
            elif lang == "hi":
                return "आपकी अनुमानित वार्षिक पारिवारिक आय कितनी है?"
            return "What is your approximate annual family income?"
        return None

    # B. Employment / Skilling
    if cat == "employment" or occ == "unemployed":
        if not state:
            if lang == "te":
                return "మీరు ఏ రాష్ట్రంలో ఉపాధి లేదా నైపుణ్య శిక్షణ కోసం చూస్తున్నారు?"
            elif lang == "hi":
                return "आप किस राज्य में रोजगार या कौशल प्रशिक्षण के अवसर तलाश रहे हैं?"
            return "Which State or Union Territory are you currently located in or seeking employment in?"
        return None

    # C. Farmer
    if cat == "agriculture" or occ == "farmer":
        if not state:
            if lang == "te":
                return "మీ వ్యవసాయ భూమి ఏ రాష్ట్రంలో ఉంది?"
            elif lang == "hi":
                return "आपकी कृषि भूमि किस राज्य में स्थित है?"
            return "Which State or Union Territory is your agricultural land located in?"
        elif land is None:
            if lang == "te":
                return "మీకు ఎన్ని ఎకరాల వ్యవసాయ భూమి ఉంది?"
            elif lang == "hi":
                return "आपके पास कितने एकड़ कृषि भूमि है?"
            return "How many acres of cultivable agricultural land do you own?"
        elif income is None:
            if lang == "te":
                return "మీ సుమారు వార్షిక కుటుంబ ఆదాయం ఎంత?"
            elif lang == "hi":
                return "आपकी अनुमानित वार्षिक पारिवारिक आय क्या है?"
            return "What is your approximate annual family income?"
        return None

    # D. Missing State for any specific occupation
    if (occ or cat) and not state:
        if lang == "te":
            return "మీరు ఏ రాష్ట్రంలో నివసిస్తున్నారు?"
        elif lang == "hi":
            return "आप किस राज्य के निवासी हैं?"
        return "Which State or Union Territory do you reside in?"

    # E. Missing all profile facts (General scheme inquiries)
    if not state and not occ and not cat:
        if lang == "te":
            return "భారత ప్రభుత్వం మరియు రాష్ట్రాల సంక్షేమ పథకాలను కనుగొనడానికి, మీరు ఏ రాష్ట్రంలో నివసిస్తున్నారు మరియు మీ వృత్తి లేదా విద్యార్హత ఏమిటి?"
        elif lang == "hi":
            return "सरकारी योजनाओं को खोजने के लिए, आप किस राज्य के निवासी हैं और आपका व्यवसाय या शिक्षा क्या है?"
        return "Which State or Union Territory do you reside in, and what is your occupation or educational qualification?"

    return None


# =====================================================================
# 4. DETERMINISTIC DATABASE SCHEME EVALUATOR
# =====================================================================
def evaluate_scheme(scheme: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic rule-based evaluation of a database scheme against known user facts.
    Strictly categorizes status into:
      - 'Potential Match'
      - 'Additional Information Required'
      - 'Likely Does Not Match'
    """
    conflicts: List[str] = []
    missing: List[str] = []
    evidence: List[str] = []
    breakdown: Dict[str, Any] = {}

    # 1. State Domicile Check
    scheme_states = [s.strip().lower() for s in scheme.get("states", [])]
    is_pan_india = "all" in scheme_states or scheme.get("scope", "").startswith("Central")
    user_state = profile.get("state")
    has_specific_state = user_state and user_state.strip().lower() not in ["all", "any", "pan-india", "pan india"]

    if has_specific_state:
        if is_pan_india or user_state.lower() in scheme_states:
            evidence.append(f"State: Applicable in {user_state} ({scheme.get('scope', 'Central/State')})")
            breakdown["state"] = {"status": "matched", "detail": f"Applicable in {user_state}"}
        else:
            conflicts.append(f"State Conflict: Scheme restricted to {', '.join(scheme.get('states', []))}, but user is in {user_state}")
            breakdown["state"] = {"status": "unmet", "detail": f"Restricted to {', '.join(scheme.get('states', []))}"}
    else:
        if is_pan_india:
            evidence.append("State: Pan-India scheme open to all States/UTs")
            breakdown["state"] = {"status": "matched", "detail": "Pan-India central scheme"}
        else:
            missing.append(f"State Domicile (Requires {', '.join(scheme.get('states', []))})")
            breakdown["state"] = {"status": "pending", "detail": "User state not specified"}

    # 2. Occupation Check
    scheme_occs = [o.strip().lower() for o in scheme.get("occupations", [])]
    user_occ = profile.get("occupation")
    has_specific_occ = user_occ and user_occ.strip().lower() not in ["all", "any"]

    if has_specific_occ:
        if "all" in scheme_occs or user_occ.lower() in scheme_occs:
            evidence.append(f"Occupation: Matches target group ({user_occ.title()})")
            breakdown["occupation"] = {"status": "matched", "detail": f"Open to {user_occ.title()}"}
        else:
            conflicts.append(f"Occupation Conflict: Scheme is for {', '.join(scheme_occs)}, not for {user_occ.title()}")
            breakdown["occupation"] = {"status": "unmet", "detail": f"Targeted for {', '.join(scheme_occs)}"}
    else:
        if "all" in scheme_occs:
            evidence.append("Occupation: Open to all occupations")
            breakdown["occupation"] = {"status": "matched", "detail": "Universal occupation eligibility"}
        else:
            missing.append(f"Occupation (Requires {', '.join(scheme_occs)})")
            breakdown["occupation"] = {"status": "pending", "detail": "User occupation not specified"}

    # 3. Age Limit Check
    min_age = scheme.get("min_age", 0)
    max_age = scheme.get("max_age", 100)
    user_age = profile.get("age")

    if user_age is not None:
        if min_age <= user_age <= max_age:
            evidence.append(f"Age: {user_age} years falls within {min_age}–{max_age} years")
            breakdown["age"] = {"status": "matched", "detail": f"Within {min_age}–{max_age} years"}
        else:
            conflicts.append(f"Age Conflict: User age {user_age} is outside eligible bracket {min_age}–{max_age} years")
            breakdown["age"] = {"status": "unmet", "detail": f"Outside {min_age}–{max_age} years limit"}
    else:
        if min_age == 0 and max_age >= 90:
            evidence.append("Age: Open to all age groups")
            breakdown["age"] = {"status": "matched", "detail": "Universal age limit"}
        else:
            missing.append(f"Age (Requires between {min_age} and {max_age} years)")
            breakdown["age"] = {"status": "pending", "detail": f"Age bracket: {min_age}–{max_age} yrs"}

    # 4. Income Threshold Check
    income_max = scheme.get("income_max", 10000000)
    user_income = profile.get("income")

    if user_income is not None:
        if user_income <= income_max:
            evidence.append(f"Income: Annual income Rs.{user_income:,} is within ceiling Rs.{income_max:,}")
            breakdown["income"] = {"status": "matched", "detail": f"Under limit Rs.{income_max:,}"}
        else:
            conflicts.append(f"Income Conflict: Income Rs.{user_income:,} exceeds maximum ceiling Rs.{income_max:,}")
            breakdown["income"] = {"status": "unmet", "detail": f"Exceeds cap Rs.{income_max:,}"}
    else:
        if income_max >= 5000000:
            evidence.append("Income: No strict low-income threshold mandated")
            breakdown["income"] = {"status": "matched", "detail": "Open income limit"}
        else:
            missing.append(f"Annual Income (Ceiling is Rs.{income_max:,}/yr)")
            breakdown["income"] = {"status": "pending", "detail": f"Income ceiling: Rs.{income_max:,}"}

    # 5. Gender Specificity Check
    scheme_gender = scheme.get("gender", "all").strip().lower()
    user_gender = profile.get("gender")
    has_specific_gender = user_gender and user_gender.strip().lower() not in ["all", "any"]

    if scheme_gender != "all":
        if has_specific_gender:
            if user_gender.lower() == scheme_gender:
                evidence.append(f"Gender: Matches dedicated {scheme_gender} entitlement")
                breakdown["gender"] = {"status": "matched", "detail": f"Targeted for {scheme_gender}"}
            else:
                conflicts.append(f"Gender Conflict: Dedicated to {scheme_gender} beneficiaries, user is {user_gender}")
                breakdown["gender"] = {"status": "unmet", "detail": f"Restricted to {scheme_gender}"}
        else:
            missing.append(f"Gender (Dedicated to {scheme_gender} beneficiaries)")
            breakdown["gender"] = {"status": "pending", "detail": f"Requires {scheme_gender}"}

    # 6. Landholding Ownership Check
    requires_land = bool(scheme.get("requires_land", 0))
    user_land = profile.get("land")

    if requires_land:
        if user_land is not None:
            if user_land != "none":
                evidence.append("Land: Agricultural cultivable landholding verified")
                breakdown["land"] = {"status": "matched", "detail": "Landowner criteria fulfilled"}
            else:
                conflicts.append("Land Conflict: Requires agricultural landholding; user reported no land owned")
                breakdown["land"] = {"status": "unmet", "detail": "Cultivable land mandatory"}
        else:
            missing.append("Agricultural Land Ownership (Mandatory for this program)")
            breakdown["land"] = {"status": "pending", "detail": "Requires agricultural landholding"}

    # 7. Girl Child Check
    requires_girl_child = bool(scheme.get("requires_girl_child", 0))
    user_girl_child = profile.get("has_girl_child")

    if requires_girl_child:
        if user_girl_child is not None:
            if user_girl_child is True:
                evidence.append("Special: Family has girl child under 10 years")
                breakdown["girl_child"] = {"status": "matched", "detail": "Girl child criteria fulfilled"}
            else:
                conflicts.append("Criteria Conflict: Scheme is specifically for families with girl children under 10")
                breakdown["girl_child"] = {"status": "unmet", "detail": "Requires girl child under 10"}
        else:
            missing.append("Girl child in family under 10 years")
            breakdown["girl_child"] = {"status": "pending", "detail": "Requires girl child under 10"}

    # 8. BPL / Ration Card Check
    requires_bpl = bool(scheme.get("requires_bpl", 0))
    user_bpl = profile.get("has_bpl")

    if requires_bpl:
        if user_bpl is not None:
            if user_bpl is True:
                evidence.append("Special: Active Ration Card / BPL card verified")
                breakdown["bpl"] = {"status": "matched", "detail": "BPL inclusion verified"}
            else:
                conflicts.append("Criteria Conflict: Scheme mandates BPL / Ration card possession")
                breakdown["bpl"] = {"status": "unmet", "detail": "Requires BPL / Ration Card"}
        else:
            missing.append("BPL / Ration card status")
            breakdown["bpl"] = {"status": "pending", "detail": "Requires BPL / Ration Card"}

    # Final Status Decision
    if len(conflicts) > 0:
        status = EligibilityStatus.LIKELY_DOES_NOT_MATCH
        confidence = 10
    elif len(missing) > 0:
        status = EligibilityStatus.ADDITIONAL_INFO_REQUIRED
        confidence = max(40, 90 - (len(missing) * 15))
    else:
        status = EligibilityStatus.POTENTIAL_MATCH
        confidence = 95

    return {
        "status": status,
        "confidence_score": confidence,
        "evidence": evidence,
        "missing_criteria": missing,
        "conflicts": conflicts,
        "rule_breakdown": breakdown
    }


# =====================================================================
# 5. RELEVANT DATABASE FILTERING ENGINE WITH IN-MEMORY CACHE
# =====================================================================
_ACTIVE_SCHEMES_CACHE: Optional[List[Dict[str, Any]]] = None

def get_cached_active_schemes() -> List[Dict[str, Any]]:
    global _ACTIVE_SCHEMES_CACHE
    if _ACTIVE_SCHEMES_CACHE is not None:
        return _ACTIVE_SCHEMES_CACHE
    with get_db_connection() as conn:
        conn.row_factory = None
        cur = conn.cursor()
        cur.execute("SELECT * FROM schemes WHERE scheme_status='active'")
        cols = [col[0] for col in cur.description]
        raw_rows = cur.fetchall()
    _ACTIVE_SCHEMES_CACHE = [row_to_dict(dict(zip(cols, r))) for r in raw_rows]
    return _ACTIVE_SCHEMES_CACHE


def find_relevant_schemes_from_db(profile: Dict[str, Any], query_text: str = "", limit: int = 10) -> List[Dict[str, Any]]:
    """
    Query actual stored schemes in SQLite database with sub-millisecond in-memory caching.
    Filter deterministically. Discard 'Likely Does Not Match'.
    Only return schemes with 'Potential Match' or domain-relevant 'Additional Information Required'.
    """
    matched_results: List[Dict[str, Any]] = []
    candidate_schemes = get_cached_active_schemes()
    cat = profile.get("category_need")

    for s in candidate_schemes:
        # Domain Relevancy Guard
        if cat:
            scheme_cat = s.get("category", "")
            scheme_title_lower = s.get("title", "").lower()
            scheme_occs = [o.strip().lower() for o in s.get("occupations", [])]

            if cat == "education":
                # Only genuine education/scholarship programs; exclude retirement pensions like APY!
                is_edu_prog = (scheme_cat == "education") or any(w in scheme_title_lower for w in ["scholarship", "vidya", "coaching", "fellowship", "education", "student"])
                is_pension = any(p in scheme_title_lower for p in ["pension", "apy", "atal pension"])
                if not is_edu_prog or is_pension:
                    continue

            if cat == "employment":
                # Must be targeted for unemployed/job seekers or employment generation
                is_emp_prog = ("unemployed" in scheme_occs) or any(w in scheme_title_lower for w in ["employment", "udyami", "swavalamban", "livelihood", "mudra", "pmegp", "job", "skill"])
                is_pension_or_health = any(p in scheme_title_lower for p in ["pension", "apy", "atal pension", "ayushman", "jan arogya", "arogya"])
                if not is_emp_prog or is_pension_or_health:
                    continue

            if cat == "agriculture" and scheme_cat not in ["agriculture"]:
                continue
            if cat == "health" and scheme_cat not in ["health"]:
                continue
            if cat == "business" and scheme_cat not in ["business"]:
                continue
            if cat == "women" and scheme_cat not in ["women", "business"]:
                continue
            if cat == "housing" and scheme_cat not in ["housing"]:
                continue
            if cat == "energy" and scheme_cat not in ["energy"]:
                continue

        eval_res = evaluate_scheme(s, profile)

        # Discard conflicting schemes
        if eval_res["status"] == EligibilityStatus.LIKELY_DOES_NOT_MATCH:
            continue

        s_copy = dict(s)
        s_copy["eligibility_status"] = eval_res["status"]
        s_copy["confidence_score"] = eval_res["confidence_score"]
        s_copy["evidence"] = eval_res["evidence"]
        s_copy["missing_criteria"] = eval_res["missing_criteria"]
        s_copy["conflicts"] = eval_res["conflicts"]
        s_copy["rule_breakdown"] = eval_res["rule_breakdown"]
        matched_results.append(s_copy)

    # Sort: Potential Match first, then by confidence score
    matched_results.sort(
        key=lambda x: (
            1 if x["eligibility_status"] == EligibilityStatus.POTENTIAL_MATCH else 0,
            x["confidence_score"],
            x.get("benefit_value", 0)
        ),
        reverse=True
    )

    return matched_results[:limit]


# =====================================================================
# 6. MAIN CHAT ORCHESTRATION PIPELINE
# =====================================================================
def process_chat_message(
    message: str,
    session_id: Optional[str] = None,
    current_profile: Optional[Dict[str, Any]] = None,
    language: str = "en",
    selected_scheme_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main entry point for assistant conversation intelligence.
    Orchestrates Intent Detection -> Fact Extraction -> Follow-up Question -> Real DB Matching / LLM.
    """
    session = get_or_create_session(session_id, current_profile)
    # Priority to language selected in the existing language selector
    req_lang = (language or "").strip().lower()
    detected_lang, is_romanized = detect_message_language(message, fallback_lang=req_lang or "en")
    if req_lang in ["te", "hi"]:
        lang = req_lang
    elif detected_lang in ["te", "hi"]:
        lang = detected_lang
    else:
        lang = req_lang or "en"

    # Save user message to history
    session["history"].append({"role": "user", "message": message})

    if selected_scheme_id:
        session["profile"]["specific_scheme_id"] = selected_scheme_id

    # Step 1: Fact extraction & corrections
    updated_profile, corrections = extract_user_information(message, session["profile"])
    session["profile"] = updated_profile

    # Step 2: Intent classification
    intent = classify_intent(message, session)
    session["last_intent"] = intent

    user_name = session["profile"].get("user_name")
    if user_name:
        name_salutation = f"నమస్కారం {user_name}! " if lang == "te" else (f"नमस्ते {user_name}! " if lang == "hi" else f"Hello {user_name}! ")
    else:
        name_salutation = ""

    # Step 3: Check if genuine LLM integration is active and succeeds
    candidate_schemes_for_llm = get_cached_active_schemes()
    llm_result = generate_ai_response(
        message=message,
        conversation_history=session["history"],
        user_profile=session["profile"],
        candidate_schemes=candidate_schemes_for_llm,
        language=lang
    )

    # If genuine LLM is connected and generated response, use it
    if llm_result and llm_result.get("text"):
        ai_reply = llm_result["text"]
        session["history"].append({"role": "assistant", "message": ai_reply})
        return {
            "status": "success",
            "intent": intent,
            "message": ai_reply,
            "follow_up_question": None,
            "updated_profile": session["profile"],
            "schemes": [],
            "requires_schemes_display": False,
            "ai_status": get_ai_config()
        }

    # =================================================================
    # OFFLINE CONTEXT-AWARE INTELLIGENCE ENGINE (When no LLM API key set)
    # =================================================================
    response_text = ""
    follow_up = None
    schemes_to_return: List[Dict[str, Any]] = []
    requires_schemes_display = False
    m_norm = normalize_indic_text(message)

    # -------------------------------------------------------------
    # CASE A: GREETING -> Conversational reply only, NO scheme cards
    # -------------------------------------------------------------
    if intent == IntentType.GREETING:
        session["pending_question_topic"] = None
        if any(w in m_norm for w in ["ela unnav", "ela unnaru", "bagunnara", "baagunnara", "how are you", "ఎలా ఉన్నారు"]):
            if lang == "te":
                response_text = f"నమస్కారం{f' {user_name}' if user_name else ''}! నేను బాగున్నాను, ధన్యవాదాలు (I am doing well, thank you)! నేను మీ మిత్ర (Mitra AI). భారతదేశం మరియు మీ రాష్ట్రంలోని ప్రభుత్వ సంక్షేమ పథకాలు, స్కాలర్‌షిప్‌లు, ఉద్యోగ అవకాశాలు, వ్యవసాయ సహాయం గురించి మీకు సహాయం చేయడానికి సిద్ధంగా ఉన్నాను. ఈరోజు మీకు ఎలాంటి పథకం లేదా సమాచారం కావాలి?"
            elif lang == "hi":
                response_text = f"नमस्ते{f' {user_name}' if user_name else ''}! मैं बिल्कुल ठीक हूँ, धन्यवाद! मैं मित्रा (Mitra AI), आपका सरकारी कल्याण सहायक हूँ। आज मैं आपकी क्या सहायता कर सकता हूँ?"
            else:
                response_text = f"Hello{f' {user_name}' if user_name else ''}! I am doing well, thank you! I am Mitra, your citizen benefit assistant. Tell me about your profession, family income, state, or financial need in Telugu, Hindi, or English."
        else:
            if lang == "te":
                response_text = f"నమస్కారం{f' {user_name}' if user_name else ''}! నేను మిత్ర (Mitra AI), మీ ప్రభుత్వ సంక్షేమ సహాయకుడిని. మీకు సరిపోయే పథకాలను గుర్తించడంలో సహాయపడతాను. మీరు మీ రాష్ట్రం, చదువు లేదా వృత్తిని తెలియజేయండి."
            elif lang == "hi":
                response_text = f"नमस्ते{f' {user_name}' if user_name else ''}! मैं मित्रा, आपका सरकारी योजना सहायक हूँ। मैं आपके लिए सही कल्याणकारी योजनाओं को खोजने में मदद कर सकता हूँ। आप अपना राज्य, पढ़ाई या व्यवसाय बता सकते हैं।"
            else:
                response_text = f"Hello{f' {user_name}' if user_name else ''}! I am Mitra, your citizen benefit assistant. Tell me about your profession, family income, state, or financial need in Telugu, Hindi, or English, and I will help you discover verified government programs."

        session["history"].append({"role": "assistant", "message": response_text})
        return {
            "status": "success",
            "intent": intent,
            "message": response_text,
            "follow_up_question": None,
            "updated_profile": session["profile"],
            "schemes": [],
            "requires_schemes_display": False,
            "ai_status": get_ai_config()
        }

    # -------------------------------------------------------------
    # CASE PROFILE_UPDATE: Facts supplied without explicit search -> Store & Ask Follow-up (NO scheme cards)
    # -------------------------------------------------------------
    if intent == IntentType.PROFILE_UPDATE:
        session["pending_question_topic"] = None
        user_name = session["profile"].get("user_name")
        edu = session["profile"].get("education")
        occ = session["profile"].get("occupation")
        age = session["profile"].get("age")
        st = session["profile"].get("state")
        follow_up = None

        # 1. Name Introduction only (e.g. "My name is Mokshagna Teja.")
        if user_name and not edu and not occ and not age and not st:
            session["pending_question_topic"] = "clarification"
            if lang == "te":
                follow_up = "దయచేసి మీరు ఏ రాష్ట్రంలో నివసిస్తున్నారు మరియు మీ వృత్తి లేదా విద్యార్హత ఏమిటో తెలియజేయండి."
                response_text = f"నమస్కారం {user_name} గారు! మిమ్మల్ని కలవడం చాలా సంతోషం. నేను మీ మిత్ర ఏఐ (Mitra AI). భారతదేశం మరియు రాష్ట్రాల అధికారిక సంక్షేమ పథకాలను గుర్తించడంలో మీకు సహాయపడతాను. ప్రారంభించడానికి, దయచేసి మీరు ఏ రాష్ట్రంలో నివసిస్తున్నారు మరియు మీ ప్రస్తుత చదువు లేదా వృత్తి ఏమిటో తెలియజేయండి."
            elif lang == "hi":
                follow_up = "कृपया अपना राज्य और अपनी वर्तमान पढ़ाई या व्यवसाय बताएं।"
                response_text = f"नमस्ते {user_name}! आपसे मिलकर बहुत खुशी हुई। मैं मित्रा एआई हूँ, आपका सरकारी योजना सहायक। आपके लिए सही सरकारी योजनाएं खोजने हेतु, कृपया अपना राज्य और अपनी वर्तमान पढ़ाई या व्यवसाय बताएं।"
            else:
                follow_up = "Please tell me your State of residence, and your occupation or education."
                response_text = f"Hello {user_name}! Pleased to meet you. I am Mitra, your citizen benefit assistant. To help you discover eligible Central and State government schemes, please tell me your State of residence, and your occupation or education (for example, student, job seeker, or farmer)."

        # 2. Student / Course (e.g. "I am a B.Tech student.")
        elif (occ == "student" or edu) and not st:
            session["pending_question_topic"] = "clarification"
            course_name = edu or "student"
            if lang == "te":
                follow_up = "మీరు ఏ రాష్ట్రంలో చదువుతున్నారు లేదా నివసిస్తున్నారు? అలాగే మీ సుమారు వార్షిక కుటుంబ ఆదాయం ఎంత?"
                response_text = (
                    f"మీరు {course_name}గా ఉన్నట్లు మీ ప్రొఫైల్‌లో నమోదు చేసుకున్నాను. కళాశాల మరియు ఉన్నత విద్యార్థుల కోసం భారతదేశంలో ముఖ్యమైన సహాయ పథకాలు అందుబాటులో ఉన్నాయి:\n\n"
                    "• **నేషనల్ స్కాలర్‌షిప్ పోర్టల్ (NSP)**: కాలేజీ విద్యార్థుల కోసం కేంద్ర ప్రభుత్వ మెరిట్-కమ్-మీన్స్ స్కాలర్‌షిప్‌లు.\n"
                    "• **విద్యా లక్ష్మి పోర్టల్ (Vidya Lakshmi)**: వడ్డీ రాయితీ (CSIS) తో కూడిన ఉన్నత విద్యా రుణాలు.\n"
                    "• **AICTE ఇంటర్న్‌షిప్‌లు & NATS శిక్షణ**: ఇంజనీరింగ్ విద్యార్థులకు ఆన్-ది-జాబ్ ప్రాక్టికల్ శిక్షణ మరియు నెలవారీ స్టైపెండ్.\n\n"
                    "మీరు ఏ రాష్ట్రంలో చదువుతున్నారు లేదా నివసిస్తున్నారు? అలాగే మీ సుమారు వార్షిక కుటుంబ ఆదాయం ఎంత? ఈ వివరాలు తెలిపితే మీకు సరిపోయే ఖచ్చితమైన పథకాలను పరిశీలించగలను."
                )
            elif lang == "hi":
                follow_up = "आप किस राज्य में पढ़ाई कर रहे हैं और आपकी अनुमानित पारिवारिक वार्षिक आय कितनी है?"
                response_text = (
                    f"मैंने आपकी प्रोफाइल में {course_name} के रूप में विवरण दर्ज कर लिया है। छात्रों के लिए भारत में प्रमुख योजनाएं सक्रिय हैं:\n\n"
                    "• **नेशनल स्कॉलरशिप पोर्टल (NSP)**: कॉलेज छात्रों के लिए केंद्रीय छात्रवृत्ति योजनाएं।\n"
                    "• **विद्या लक्ष्मी पोर्टल**: ब्याज सब्सिडी (CSIS) के साथ शिक्षा ऋण।\n"
                    "• **AICTE व NATS**: उद्योग इंटर्नशिप और मासिक सरकारी वजीफा।\n\n"
                    "आप किस राज्य में पढ़ाई कर रहे हैं और आपकी अनुमानित पारिवारिक वार्षिक आय कितनी है?"
                )
            else:
                follow_up = "Which State do you study in, and what is your annual family income?"
                response_text = (
                    f"I have recorded your profile as a {course_name}. In India, key support initiatives for college and higher education students include:\n\n"
                    "1. **National Scholarship Portal (NSP)**: Central Sector Schemes providing merit-cum-means financial assistance.\n"
                    "2. **Vidya Lakshmi Education Loan Portal**: Collateral-free education loans with Central Sector Interest Subsidy (CSIS) on moratorium.\n"
                    "3. **AICTE Internships & NATS (Skill India)**: Industry apprenticeships and technical skill programs with monthly government stipends.\n\n"
                    "Which State or Union Territory do you currently reside in or study in? Once you provide your State and approximate annual family income, I will evaluate the verified schemes and scholarships you are eligible for."
                )

        # 3. Unemployed / 18 & Unemployed (e.g. "I am 18 and unemployed.", "I am unemployed.")
        elif occ == "unemployed" and not st:
            session["pending_question_topic"] = "clarification"
            age_str = f"at age {age} " if age else ""
            if lang == "te":
                follow_up = "మీ ప్రస్తుత విద్యార్హత ఏమిటి మరియు మీరు ఏ రాష్ట్రంలో నివసిస్తున్నారు?"
                response_text = (
                    f"భారతదేశంలో{' ' + str(age) + ' సంవత్సరాల' if age else ''} నిరుద్యోగ యువత మరియు ఉపాధి లేదా స్వయం ఉపాధి కోరే వారి కోసం కేంద్ర మరియు రాష్ట్ర ప్రభుత్వాలు ముఖ్యమైన పథకాలను అందిస్తున్నాయి:\n\n"
                    "• **PMKVY 4.0 (స్కిల్ ఇండియా)**: పరిశ్రమలకు అవసరమైన సాంకేతిక మరియు డిజిటల్ నైపుణ్యాలలో ఉచిత శిక్షణ, కేంద్ర ప్రభుత్వ సర్టిఫికేషన్.\n"
                    "• **NATS (నేషనల్ అప్రెంటిస్‌షిప్)**: పరిశ్రమల్లో ఆన్-ది-జాబ్ ప్రాక్టికల్ ట్రైనింగ్ మరియు నెలవారీ ప్రభుత్వ స్టైపెండ్.\n"
                    "• **PMEGP & ముద్రా రుణాలు**: కొత్త వ్యాపారం లేదా స్వయం ఉపాధి ప్రారంభించడానికి పూచీకత్తు లేని సబ్సిడీ రుణాలు.\n\n"
                    "మీ ప్రస్తుత విద్యార్హత (ఉదా: 10వ తరగతి, ఇంటర్, లేదా డిగ్రీ) ఏమిటి మరియు మీరు ఏ రాష్ట్రంలో నివసిస్తున్నారు? ఈ వివరాలు తెలిపితే మీ ప్రాంతానికి సంబంధించిన నిర్దిష్ట పథకాలను సూచించగలను."
                )
            elif lang == "hi":
                follow_up = "आपकी शैक्षणिक योग्यता क्या है और आप किस राज्य के निवासी हैं?"
                response_text = (
                    f"भारत में{' ' + str(age) + ' वर्ष के' if age else ''} बेरोजगार युवाओं और रोजगार/स्वरोजगार के इच्छुक नागरिकों के लिए प्रमुख सरकारी योजनाएं सक्रिय हैं:\n\n"
                    "• **PMKVY 4.0 (स्किल इंडिया)**: तकनीकी व व्यावसायिक कौशल में मुफ्त प्रशिक्षण और सरकारी प्रमाणन।\n"
                    "• **NATS अप्रेंटिसशिप**: उद्योग प्रशिक्षण और मासिक सरकारी वजीफा।\n"
                    "• **PMEGP व मुद्रा योजना**: नया उद्यम शुरू करने हेतु रियायती ऋण।\n\n"
                    "आपकी शैक्षणिक योग्यता क्या है और आप किस राज्य के निवासी हैं? इससे मैं आपके लिए उपयुक्त योजनाएं खोज सकूंगा।"
                )
            else:
                follow_up = "Which State do you reside in, and what is your highest educational qualification?"
                response_text = (
                    f"I have noted your profile {age_str}seeking employment and skill development opportunities. Key flagship initiatives active across India include:\n\n"
                    "1. **PMKVY 4.0 (Skill India)**: Free certified vocational and technical courses in industry-relevant trades.\n"
                    "2. **National Apprenticeship Training Scheme (NATS)**: Practical on-the-job training in recognized enterprises with monthly stipends.\n"
                    "3. **PMEGP & PM Mudra Yojana**: Subsidized seed capital and collateral-free loans up to Rs. 50 Lakhs to start a business or enterprise.\n\n"
                    "Which State or Union Territory do you currently reside in, and what is your highest educational qualification (e.g., 10th, 12th, or Degree)? Letting me know will help me find specific programs in your region."
                )

        # 4. Age only (e.g. "I am 18 years old.")
        elif age and not occ and not edu and not st:
            session["pending_question_topic"] = "clarification"
            if lang == "te":
                follow_up = "మీరు ప్రస్తుతం చదువుకుంటున్నారా, ఉద్యోగం లేదా నైపుణ్య శిక్షణ కోసం చూస్తున్నారా? మరియు ఏ రాష్ట్రంలో నివసిస్తున్నారు?"
                response_text = f"మీ వయస్సు {age} సంవత్సరాలుగా నమోదు చేసుకున్నాను. ఈ వయస్సులో మీరు ఉన్నత విద్య, నైపుణ్య శిక్షణ లేదా యువత ఉపాధి పథకాలకు అర్హత పొందవచ్చు. మీరు ప్రస్తుతం చదువుకుంటున్నారా, ఉద్యోగం లేదా నైపుణ్య శిక్షణ కోసం చూస్తున్నారా? మరియు మీరు ఏ రాష్ట్రంలో నివసిస్తున్నారు?"
            elif lang == "hi":
                follow_up = "क्या आप वर्तमान में पढ़ाई कर रहे हैं या रोजगार की तलाश में हैं? और आप किस राज्य के निवासी हैं?"
                response_text = f"मैंने आपकी आयु {age} वर्ष दर्ज कर ली है। इस आयु में आप उच्च शिक्षा, कौशल विकास और स्वरोजगार के कई कार्यक्रमों के पात्र हैं। क्या आप वर्तमान में पढ़ाई कर रहे हैं या रोजगार/कौशल प्रशिक्षण की तलाश में हैं? और आप किस राज्य के निवासी हैं?"
            else:
                follow_up = "Which State do you reside in, and are you studying or looking for employment?"
                response_text = f"I have recorded your age as {age} years. At this age, you may qualify for higher education scholarships, youth skill development, and employment initiatives. Are you currently a student pursuing education, looking for employment or skill training, or planning to start an enterprise? Which State or Union Territory do you reside in?"

        # 5. Farmer (e.g. "I am a farmer from Andhra Pradesh.")
        elif occ == "farmer":
            session["pending_question_topic"] = "clarification"
            st_name = st or "your State"
            if lang == "te":
                follow_up = "మీకు ఎన్ని ఎకరాల సాగు భూమి ఉంది మరియు మీ సుమారు వార్షిక కుటుంబ ఆదాయం ఎంత?"
                response_text = f"నమస్కారం! {st or 'భారతదేశం'}లో రైతులకు కేంద్ర ప్రభుత్వ PM-కిసాన్ (ఏటా రూ. 6,000) మరియు రాష్ట్ర రైతు సంక్షేమ పథకాలు అమల్లో ఉన్నాయి. మీకు వర్తించే ఖచ్చితమైన సహాయాన్ని గుర్తించడానికి, మీకు ఎన్ని ఎకరాల సాగు భూమి ఉంది మరియు మీ సుమారు వార్షిక కుటుంబ ఆదాయం ఎంత?"
            elif lang == "hi":
                follow_up = "आपके पास कितने एकड़ कृषि भूमि है और आपकी वार्षिक पारिवारिक आय क्या है?"
                response_text = f"स्वागत है! {st or 'भारत'} में किसानों के लिए केंद्र सरकार की पीएम-किसान योजना और राज्य कृषि कल्याण योजनाएं सक्रिय हैं। सटीक लाभ निर्धारित करने के लिए, आपके पास कितने एकड़ कृषि भूमि है और आपकी वार्षिक पारिवारिक आय क्या है?"
            else:
                follow_up = "How many acres of cultivable agricultural land do you own, and what is your approximate annual family income?"
                response_text = f"Welcome! In {st_name}, farmers can benefit from both Central (PM-KISAN: Rs. 6,000/year direct cash support) and State agricultural welfare initiatives. To verify your exact benefit tier, how many acres of cultivable agricultural land do you own, and what is your approximate annual family income?"

        else:
            session["pending_question_topic"] = "clarification"
            follow_q = generate_follow_up_question(session["profile"], lang=lang)
            follow_up = follow_q or "Please share your State and approximate annual income."
            if lang == "te":
                response_text = f"మీ వివరాలు నమోదు చేసుకున్నాను. మీకు సరిపోయే పథకాలను గుర్తించడానికి: {follow_q or 'మీ రాష్ట్రం లేదా కుటుంబ ఆదాయాన్ని తెలపండి.'}"
            elif lang == "hi":
                response_text = f"आपकी जानकारी दर्ज कर ली गई है। उपयुक्त योजनाएं खोजने के लिए: {follow_q or 'कृपया अपना राज्य या पारिवारिक आय बताएं।'}"
            else:
                response_text = f"I have updated your profile with the details provided. To help me find matching government programs: {follow_q or 'Please share your State and approximate annual income.'}"

        session["history"].append({"role": "assistant", "message": response_text})
        return {
            "status": "success",
            "intent": intent,
            "message": response_text,
            "follow_up_question": follow_up,
            "updated_profile": session["profile"],
            "schemes": [],
            "requires_schemes_display": False,
            "ai_status": get_ai_config()
        }


    # -------------------------------------------------------------
    # CASE B: GENERAL CONVERSATION / UNRELATED -> Natural reply, NO scheme cards
    # -------------------------------------------------------------
    if intent == IntentType.GENERAL_CONVERSATION:
        session["pending_question_topic"] = None
        if any(w in m_norm for w in ["how are you", "ela unnav", "ela unnaru", "bagunnara", "baagunnara", "ఎలా ఉన్నారు", "ఎలా ఉన్నావు", "आप कैसे हैं", "kaise ho", "kaise hain"]):
            if lang == "te":
                response_text = f"నమస్కారం{f' {user_name}' if user_name else ''}! నేను చాలా బాగున్నాను, ధన్యవాదాలు (I am doing well, thank you)! భారత ప్రభుత్వ మరియు రాష్ట్ర సంక్షేమ పథకాల గురించి మీ సందేహాలను నివృత్తి చేయడానికి సిద్ధంగా ఉన్నాను. ఈరోజు మీకు ఎలా సహాయపడగలను?"
            elif lang == "hi":
                response_text = f"नमस्ते{f' {user_name}' if user_name else ''}! मैं बिल्कुल ठीक हूँ, धन्यवाद! मैं भारत की सरकारी और राज्य कल्याणकारी योजनाओं को खोजने में आपकी मदद के लिए तैयार हूँ। आज मैं आपकी क्या सहायता कर सकता हूँ?"
            else:
                response_text = f"Hello{f' {user_name}' if user_name else ''}! I am doing well, thank you! I am ready to help you discover government benefits, scholarships, pensions, and financial assistance across India. What type of assistance are you looking for?"
        elif any(w in m_norm for w in ["who are you", "what can you do", "మీరు ఎవరు", "आप कौन हैं"]):
            if lang == "te":
                response_text = "నేను మిత్ర ఏఐ (Mitra AI), భారతీయ పౌరుల సంక్షేమ కో-పైలట్. ఆధార్ లేదా గోప్యమైన పత్రాలు లేకుండా కేంద్ర మరియు రాష్ట్ర పథకాల అధికారిక అర్హత నిబంధనలను విశ్లేషిస్తాను. ప్రారంభించడానికి మీ రాష్ట్రం మరియు వృత్తిని తెలియజేయండి."
            elif lang == "hi":
                response_text = "मैं मित्रा एआई (Mitra AI) हूँ, आपका सरकारी योजना सहायक। मैं आधार या संवेदनशील दस्तावेजों के बिना केंद्रीय और राज्य योजनाओं के आधिकारिक पात्रता नियमों का विश्लेषण करता हूँ। शुरू करने के लिए अपना राज्य और पेशा बताएं।"
            else:
                response_text = "I am Mitra AI, an intelligent citizen welfare co-pilot. I analyze official eligibility criteria for central and state schemes without requiring Aadhaar or confidential documents. Tell me your state and occupation to get started."
        elif any(unrelated in m_norm for unrelated in ["capital of france", "paris", "bake a cake", "make tea", "recipe", "poem", "python code", "solve math"]):
            if "capital of france" in m_norm or "paris" in m_norm:
                if lang == "te":
                    response_text = "ఫ్రాన్స్ రాజధాని ప్యారిస్. అయితే, మిత్ర ఏఐగా నా ప్రాథమిక సేవ భారతీయ పౌరులకు కేంద్ర మరియు రాష్ట్ర ప్రభుత్వ సంక్షేమ పథకాలు, స్కాలర్‌షిప్‌లు, రుణాలు మరియు పెన్షన్‌లను కనుగొనడంలో సహాయపడటం. ఏదైనా ప్రభుత్వ పథకాల అర్హతను పరిశీలించాలనుకుంటే, దయచేసి మీ రాష్ట్రం మరియు వృత్తిని తెలియజేయండి!"
                elif lang == "hi":
                    response_text = "फ्रांस की राजधानी पेरिस है। हालांकि, मित्रा एआई के रूप में मेरी मुख्य सेवा भारतीय नागरिकों को सरकारी कल्याणकारी योजनाओं, छात्रवृत्ति और पेंशन खोजने में मदद करना है। किसी भी योजना के लिए अपनी पात्रता जांचने हेतु अपना राज्य और व्यवसाय बताएं!"
                else:
                    response_text = "The capital of France is Paris. However, my primary service as Mitra AI is to help Indian citizens find relevant government welfare schemes, scholarships, loans, and pensions. If you'd like to check eligibility for any government programs, please tell me your state and occupation!"
            else:
                if lang == "te":
                    response_text = "నేను భారతదేశ ప్రభుత్వ సంక్షేమ కార్యక్రమాలు, స్కాలర్‌షిప్‌లు, పెన్షన్‌లు మరియు ఆర్థిక రాయితీలకు సంబంధించిన సమాచారం అందించడంలో ప్రత్యేకత కలిగి ఉన్నాను. ప్రభుత్వ పథకాల గురించి తెలుసుకోవడానికి మీ రాష్ట్రం లేదా వృత్తిని తెలియజేయండి!"
                elif lang == "hi":
                    response_text = "मैं विशेष रूप से भारतीय सरकारी कल्याणकारी कार्यक्रमों, छात्रवृत्ति, पेंशन और वित्तीय सब्सिडी में सहायता करता हूँ। यदि आपका कोई प्रश्न है, तो अपना राज्य या व्यवसाय बताएं!"
                else:
                    response_text = "I specialize specifically in Indian government welfare programs, scholarships, pensions, and financial subsidies. If you have questions about citizen benefits, tell me your state or profession!"
        else:
            if lang == "te":
                response_text = f"{name_salutation}భారత ప్రభుత్వ మరియు అన్ని రాష్ట్రాల అధికారిక సంక్షేమ పథకాల సమాచారాన్ని అందించడానికి నేను ఇక్కడ ఉన్నాను. మీ వృత్తి, చదువు, కుటుంబ ఆదాయం లేదా సహాయం అవసరాన్ని తెలియజేయండి!"
            elif lang == "hi":
                response_text = f"{name_salutation}मैं केंद्र और राज्यों की सत्यापित सरकारी योजनाओं में आपकी सहायता के लिए तैयार हूँ। अपने व्यवसाय, शिक्षा या सहायता की आवश्यकता के बारे में बताएं!"
            else:
                response_text = f"{name_salutation}I am here to help you navigate verified Indian government schemes across central ministries and all states. Tell me about your profession, education, family income, or assistance needs!"

        session["history"].append({"role": "assistant", "message": response_text})
        return {
            "status": "success",
            "intent": intent,
            "message": response_text,
            "follow_up_question": None,
            "updated_profile": session["profile"],
            "schemes": [],
            "requires_schemes_display": False,
            "ai_status": get_ai_config()
        }

    # -------------------------------------------------------------
    # CASE C: SPECIFIC SCHEME DETAILS & APPLICATION / DOCUMENT / PORTAL HELP
    # -------------------------------------------------------------
    if intent in [IntentType.SCHEME_DETAILS, IntentType.APPLICATION_HELP]:
        target_id = session["profile"].get("specific_scheme_id")

        # Try to infer target scheme from message or known aliases
        for s_id, aliases in [
            ("pm-kisan", ["pm kisan", "pm-kisan", "kisan samman", "పీఎం కిసాన్", "पीएम किसान"]),
            ("nsp-scholarship", ["nsp", "national scholarship", "scholarship portal", "కేంద్ర స్కాలర్‌షిప్", "राष्ट्रीय छात्रवृत्ति"]),
            ("ayushman-bharat", ["ayushman bharat", "pmjay", "pm-jay", "jan arogya", "ఆయుష్మాన్ భారత్", "आयुष्मान भारत"]),
            ("pm-mudra", ["mudra", "pm mudra", "mudra loan", "ముద్రా లోన్", "मुद्रा लोन"]),
            ("vidya-lakshmi", ["vidya lakshmi", "vidyalakshmi", "విద్యాలక్ష్మి", "विद्या लक्ष्मी"]),
            ("pm-svanidhi", ["svanidhi", "street vendor", "స్వనిధి", "स्वनिधि"]),
            ("sukanya-samriddhi", ["sukanya", "సుకున్య సమృద్ధి", "सुकन्या समृद्धि"]),
            ("rythu-bharosa-bandhu", ["rythu bharosa", "rythu bandhu", "రైతు భరోసా", "రైతు బంధు"]),
            ("atal-pension-yojana", ["atal pension", "apy", "అటల్ పెన్షన్", "अटल पेंशन"]),
            ("pmay-urban-gramin", ["pmay", "awas yojana", "ఆవాస్ యోజన", "आवास योजना"]),
            ("pm-surya-ghar", ["surya ghar", "solar rooftop", "సూర్య ఘర్", "सूर्य घर"])
        ]:
            if any(al in m_norm for al in aliases):
                target_id = s_id
                session["profile"]["specific_scheme_id"] = target_id
                break

        if target_id:
            scheme_row = query_scheme_by_id(target_id)
            if scheme_row:
                crit = scheme_row.get("criteria", {})
                crit_summary = crit.get("summary", "Standard eligibility guidelines.")
                raw_docs = scheme_row.get("documents", [])
                if isinstance(raw_docs, list):
                    docs_items = raw_docs
                elif isinstance(raw_docs, str):
                    try:
                        import json
                        docs_items = json.loads(raw_docs)
                    except Exception:
                        docs_items = [d.strip() for d in raw_docs.split(",") if d.strip()]
                else:
                    docs_items = ["Aadhaar Card", "Bank Account Passbook", "Income Certificate"]

                docs_formatted_en = "\n".join([f"{i+1}. {doc}" for i, doc in enumerate(docs_items)])
                docs_formatted_te = "\n".join([f"{i+1}. {doc}" for i, doc in enumerate(docs_items)])
                docs_formatted_hi = "\n".join([f"{i+1}. {doc}" for i, doc in enumerate(docs_items)])

                portal = scheme_row.get("official_url", "https://india.gov.in")
                app_url = scheme_row.get("official_application_url") or portal
                dept = scheme_row.get("department", "Government of India")
                sch_title = scheme_row.get("title", "Government Scheme")
                acronym = scheme_row.get("acronym", "")

                is_asking_docs = any(w in m_norm for w in ["document", "documents", "పత్రాలు", "దస్తావేజ్", "दस्तावेज", "दस्तावेज़", "patralu", "papers"])
                is_asking_link = any(w in m_norm for w in ["link", "url", "portal", "website", "online portal", "లింక్", "వెబ్సైట్", "లింకు", "लिंक", "वेबसाइट", "portal link", "application link"])

                if is_asking_docs and not is_asking_link:
                    if lang == "te":
                        response_text = (
                            f"**{sch_title} ({acronym}) పథకానికి కావలసిన అధికారిక పత్రాలు**:\n\n"
                            f"{docs_formatted_te}\n\n"
                            f"• **అధికారిక దరఖాస్తు పోర్టల్**: {portal}\n"
                            f"• **గమనిక**: దరఖాస్తు సమయంలో ధృవీకరణ కోసం అన్ని ఒరిజినల్ పత్రాలు మరియు స్వయం ధృవీకరణ కాపీలు సిద్ధంగా ఉంచుకోండి."
                        )
                    elif lang == "hi":
                        response_text = (
                            f"**{sch_title} ({acronym}) के लिए आवश्यक आधिकारिक दस्तावेज**:\n\n"
                            f"{docs_formatted_hi}\n\n"
                            f"• **आधिकारिक आवेदन पोर्टल**: {portal}\n"
                            f"• **नोट**: ऑनलाइन आवेदन के समय सत्यापन हेतु सभी मूल दस्तावेज अपने पास रखें।"
                        )
                    else:
                        response_text = (
                            f"Here are the verified required documents for **{sch_title} ({acronym})**:\n\n"
                            f"{docs_formatted_en}\n\n"
                            f"• **Official Application Portal**: [{portal}]({portal})\n"
                            f"• **Note**: Ensure all documents have matching names and dates of birth with your Aadhaar and bank account."
                        )

                elif is_asking_link:
                    if lang == "te":
                        response_text = (
                            f"**{sch_title} ({acronym}) అధికారిక పోర్టల్ మరియు దరఖాస్తు లింక్**:\n\n"
                            f"• **అధికారిక పోర్టల్**: {portal}\n"
                            f"• **ప్రత్యక్ష ఆన్‌లైన్ దరఖాస్తు లింక్**: {app_url}\n"
                            f"• **నోడల్ శాఖ**: {dept}\n\n"
                            f"⚠️ **భద్రతా హెచ్చరిక**: అనధికారిక లేదా ప్రైవేట్ వెబ్‌సైట్‌లలో ఎప్పుడూ వ్యక్తిగత వివరాలు, పాస్‌వర్డ్‌లు లేదా ఓటీపీలను నమోదు చేయవద్దు. కేవలం .gov.in లేదా .nic.in తో ముగిసే అధికారిక ప్రభుత్వ పోర్టల్‌లను మాత్రమే ఉపయోగించండి."
                        )
                    elif lang == "hi":
                        response_text = (
                            f"**{sch_title} ({acronym}) का आधिकारिक पोर्टल एवं आवेदन लिंक**:\n\n"
                            f"• **आधिकारिक पोर्टल**: {portal}\n"
                            f"• **सीधा ऑनलाइन आवेदन लिंक**: {app_url}\n"
                            f"• **नोडल विभाग**: {dept}\n\n"
                            f"⚠️ **सुरक्षा चेतावनी**: कभी भी अनधिकृत निजी वेबसाइटों पर व्यक्तिगत जानकारी या ओटीपी साझा न करें। केवल .gov.in या .nic.in वाले आधिकारिक सरकारी पोर्टलों का ही उपयोग करें।"
                        )
                    else:
                        response_text = (
                            f"Here are the verified official links for **{sch_title} ({acronym})**:\n\n"
                            f"• **Official Government Portal**: [{portal}]({portal})\n"
                            f"• **Direct Online Application Link**: [{app_url}]({app_url})\n"
                            f"• **Nodal Department/Ministry**: {dept}\n\n"
                            f"⚠️ **Security Notice**: Never submit applications or pay processing fees on unverified third-party domains. Always ensure the website address ends with `.gov.in` or `.nic.in`."
                        )
                else:
                    if lang == "te":
                        response_text = (
                            f"**{sch_title} ({acronym}) పథకం పూర్తి వివరాలు**:\n"
                            f"• **నిర్వహణ శాఖ**: {dept}\n"
                            f"• **ప్రయోజనం**: {scheme_row.get('benefit')}\n"
                            f"• **అర్హత నిబంధనలు**: {crit_summary}\n\n"
                            f"**అవసరమైన పత్రాలు**:\n{docs_formatted_te}\n\n"
                            f"• **అధికారిక దరఖాస్తు పోర్టల్**: {portal}"
                        )
                    elif lang == "hi":
                        response_text = (
                            f"**{sch_title} ({acronym}) योजना का पूर्ण विवरण**:\n"
                            f"• **नोडल मंत्रालय**: {dept}\n"
                            f"• **प्रमुख लाभ**: {scheme_row.get('benefit')}\n"
                            f"• **पात्रता मानदंड**: {crit_summary}\n\n"
                            f"**आवश्यक दस्तावेज**:\n{docs_formatted_hi}\n\n"
                            f"• **आधिकारिक आवेदन पोर्टल**: {portal}"
                        )
                    else:
                        response_text = (
                            f"**{sch_title} ({acronym}) Overview**:\n"
                            f"• **Department/Ministry**: {dept}\n"
                            f"• **Key Benefit**: {scheme_row.get('benefit')}\n"
                            f"• **Eligibility Criteria**: {crit_summary}\n\n"
                            f"**Required Documents**:\n{docs_formatted_en}\n\n"
                            f"• **Official Application Portal**: [{portal}]({portal})"
                        )

                scheme_copy = dict(scheme_row)
                scheme_copy["eligibility_status"] = EligibilityStatus.POTENTIAL_MATCH
                scheme_copy["match_score"] = 96
                session["history"].append({"role": "assistant", "message": response_text})

                return {
                    "status": "success",
                    "intent": intent,
                    "message": response_text,
                    "follow_up_question": None,
                    "updated_profile": session["profile"],
                    "schemes": [scheme_copy],
                    "requires_schemes_display": True,
                    "ai_status": get_ai_config()
                }

        # If no specific scheme was selected or identified
        if lang == "te":
            response_text = "మీరు ఏ ప్రభుత్వ పథకం గురించి లేదా ఏ పథకానికి సంబంధించిన పత్రాలు/దరఖాస్తు లింక్ తెలుసుకోవాలనుకుంటున్నారు? ఉదాహరణకు: PM-కిసాన్, నేషనల్ స్కాలర్‌షిప్ పోర్టల్, ఆయుష్మాన్ భారత్, విద్యా లక్ష్మి లేదా ముద్రా లోన్."
        elif lang == "hi":
            response_text = "आप किस सरकारी योजना के बारे में या किस योजना के आवश्यक दस्तावेज/आवेदन लिंक जानना चाहते हैं? उदाहरण: पीएम-किसान, राष्ट्रीय छात्रवृत्ति पोर्टल, आयुष्मान भारत, विद्या लक्ष्मी या मुद्रा लोन।"
        else:
            response_text = "Which government scheme would you like to check? (e.g., PM-Kisan, National Scholarship Portal, Ayushman Bharat, Vidya Lakshmi, or Mudra loans). Please name the scheme so I can provide the verified documents and official portal link."

        session["history"].append({"role": "assistant", "message": response_text})
        return {
            "status": "success",
            "intent": intent,
            "message": response_text,
            "follow_up_question": None,
            "updated_profile": session["profile"],
            "schemes": [],
            "requires_schemes_display": False,
            "ai_status": get_ai_config()
        }


    # -------------------------------------------------------------
    # CASE D: EMPLOYMENT / CAREER / SKILL SCHEMES (e.g. unemployed youth or Mokshagnateja B.Tech student)
    # -------------------------------------------------------------
    if intent == IntentType.EMPLOYMENT_SEARCH:
        session["pending_question_topic"] = "employment_location"
        edu = session["profile"].get("education")
        st = session["profile"].get("state")
        is_student_or_btech = (edu and "b.tech" in edu.lower()) or (session["profile"].get("occupation") == "student")

        if is_student_or_btech:
            if user_name:
                salutation = f"నమస్కారం {user_name}! " if lang == "te" else (f"नमस्ते {user_name}! " if lang == "hi" else f"Hello {user_name}! ")
            else:
                salutation = ""
            if lang == "te":
                response_text = (
                    f"{salutation}మీరు B.Tech ఇంజనీరింగ్ చదువుతున్నందున, భారతదేశంలో విద్యార్థులు మరియు గ్రాడ్యుయేట్ల కోసం ప్రధాన ఉపాధి, ఇంటర్న్‌షిప్ మరియు నైపుణ్య పథకాలు అందుబాటులో ఉన్నాయి:\n\n"
                    "1. **National Apprenticeship Training Scheme (NATS)**: గ్రాడ్యుయేట్ ఇంజనీర్లకు పరిశ్రమలలో 1 సంవత్సరం ఆన్-ది-జాబ్ ప్రాక్టికల్ శిక్షణ మరియు నెలకు కేంద్ర ప్రభుత్వ స్టైపెండ్.\n"
                    "2. **AICTE Internship Portal**: అధికారిక ప్రభుత్వ మరియు పారిశ్రామిక ప్రాజెక్టులలో సాంకేతిక ఇంటర్న్‌షిప్‌ల ప్రత్యక్ష ప్రవేశం.\n"
                    "3. **PMKVY 4.0 (Skill India)**: AI, క్లౌడ్ కంప్యూటింగ్, రోబోటిక్స్ వంటి అధునాతన సాంకేతిక కోర్సుల్లో ఉచిత సర్టిఫికేషన్.\n"
                    "4. **PMEGP & PM Mudra Loan**: టెక్నాలజీ లేదా స్టార్టప్ ప్రారంభించడానికి రూ. 50 లక్షల వరకు పూచీకత్తు లేని సబ్సిడీ రుణం.\n\n"
                    "మీ ఇంజనీరింగ్ కళాశాల ఏ రాష్ట్రంలో ఉంది? మీ రాష్ట్రాన్ని తెలిపితే రాష్ట్ర ప్రభుత్వ నిర్దిష్ట స్కిల్లింగ్ మరియు ప్లేస్‌మెంట్ ప్రోత్సాహకాలను (ఉదా: APSSDC / TASK) వివరించగలను."
                )
            elif lang == "hi":
                response_text = (
                    f"{salutation}चूंकि आप B.Tech इंजीनियरिंग के छात्र हैं, भारत में छात्रों व फ्रेश ग्रेजुएट्स के लिए प्रमुख रोजगार और कौशल विकास योजनाएं उपलब्ध हैं:\n\n"
                    "1. **National Apprenticeship Training Scheme (NATS)**: इंजीनियरिंग स्नातकों के लिए 1 वर्ष का व्यावहारिक उद्योग प्रशिक्षण और मासिक सरकारी वजीफा (Stipend)।\n"
                    "2. **AICTE Internship Portal**: केंद्र सरकार और प्रमुख कंपनियों के साथ तकनीकी इंटर्नशिप के अवसर।\n"
                    "3. **PMKVY 4.0 (स्किल इंडिया)**: AI, मशीन लर्निंग और सॉफ्टवेयर इंजीनियरिंग में उद्योग-मान्यता प्राप्त उन्नत प्रमाणन।\n"
                    "4. **PMEGP व पीएम मुद्रा योजना**: अपना तकनीकी उद्यम या स्टार्टअप शुरू करने के लिए 50 लाख रुपये तक का रियायती ऋण।\n\n"
                    "आप वर्तमान में किस राज्य में पढ़ाई कर रहे हैं या रहते हैं? राज्य बताने पर मैं आपके लिए राज्य-विशिष्ट इंजीनियरिंग प्लेसमेंट योजनाएं भी बता सकूंगा।"
                )
            else:
                response_text = (
                    f"{salutation}As a B.Tech engineering student exploring employment and career opportunities in India, several flagship Central and State initiatives are specifically tailored for you:\n\n"
                    "1. **National Apprenticeship Training Scheme (NATS)**: Offers 1-year paid practical industry apprenticeship training with monthly Central Government stipends for engineering graduates.\n"
                    "2. **AICTE Internship Portal**: Direct gateway to verified technical and research internships across government bodies, PSUs, and technology enterprises.\n"
                    "3. **PMKVY 4.0 (Skill India)**: Free advanced technical certifications in Industry 4.0 domains like Artificial Intelligence, Cloud Systems, and Robotics.\n"
                    "4. **PMEGP & PM Mudra Yojana**: Subsidized seed capital and collateral-free loans up to Rs. 50 Lakhs if you plan to launch a technology startup or engineering enterprise.\n\n"
                    "Which State or Union Territory do you currently reside in or plan to work in? Letting me know your State will help me highlight state-specific engineering incentives and placement missions (such as APSSDC in Andhra Pradesh or TASK in Telangana)."
                )
        else:
            if lang == "te":
                response_text = (
                    f"{name_salutation}భారతదేశంలో నిరుద్యోగ యువత మరియు ఉపాధి లేదా స్వయం ఉపాధి కోరే వారి కోసం కేంద్ర మరియు రాష్ట్ర ప్రభుత్వాలు ముఖ్యమైన పథకాలను అందిస్తున్నాయి:\n\n"
                    "1. **నైపుణ్య శిక్షణ (Skill Development Programs)**:\n"
                    "• **PMKVY 4.0 (ప్రధాన మంత్రి కౌశల్ వికాస్ యోజన)**: పరిశ్రమలకు అవసరమైన సాంకేతిక, డిజిటల్ మరియు వృత్తి నైపుణ్యాలలో ఉచిత శిక్షణ మరియు కేంద్ర ప్రభుత్వ సర్టిఫికేషన్.\n\n"
                    "2. **ఉద్యోగ & అప్రెంటిస్‌షిప్ శిక్షణ (On-the-Job Training & Apprenticeship)**:\n"
                    "• **NATS (నేషనల్ అప్రెంటిస్‌షిప్ ట్రైనింగ్ స్కీమ్)**: ఇంజనీరింగ్, డిప్లొమా మరియు జనరల్ గ్రాడ్యుయేట్లకు పరిశ్రమల్లో 1 సంవత్సరం ప్రాక్టికల్ ట్రైనింగ్ మరియు నెలవారీ ప్రభుత్వ స్టైపెండ్.\n\n"
                    "3. **స్వయం ఉపాధి & వ్యాపార రుణాలు (Self-Employment & Business Loans)**:\n"
                    "• **PMEGP (ప్రధాన మంత్రి ఉపాధి కల్పన కార్యక్రమం)**: కొత్త వ్యాపారం లేదా పరిశ్రమ ప్రారంభించడానికి ప్రాజెక్ట్ వ్యయంపై 15% నుండి 35% వరకు ప్రభుత్వ సబ్సిడీ.\n"
                    "• **PM ముద్రా యోజన (MUDRA Loans)**: పూచీకత్తు లేకుండా రూ. 50,000 నుండి రూ. 10 లక్షల వరకు స్వయం ఉపాధి రుణాలు.\n\n"
                    "మీ ప్రస్తుత విద్యార్హత (ఉదా: 10వ తరగతి, ఇంటర్, లేదా డిగ్రీ/ఇంజనీరింగ్) ఏమిటి మరియు మీరు ఏ రాష్ట్రంలో నివసిస్తున్నారు? ఈ వివరాలు తెలిపితే మీ ప్రాంతానికి సంబంధించిన నిర్దిష్ట పథకాలను సూచించగలను."
                )
            elif lang == "hi":
                response_text = (
                    f"{name_salutation}भारत में बेरोजगार युवाओं और रोजगार/स्वरोजगार के इच्छुक नागरिकों के लिए प्रमुख सरकारी योजनाएं सक्रिय हैं:\n\n"
                    "1. **कौशल विकास (PMKVY 4.0)**: विभिन्न उद्योगों में मुफ्त तकनीकी व व्यावसायिक प्रशिक्षण और सरकारी प्रमाणन।\n"
                    "2. **अप्रेंटिसशिप व नौकरी प्रशिक्षण (NATS)**: स्नातकों और डिप्लोमा धारकों के लिए उद्योग प्रशिक्षण व मासिक वजीफा।\n"
                    "3. **स्वरोजगार ऋण (PMEGP व मुद्रा योजना)**: नया उद्यम शुरू करने हेतु 10 से 50 लाख रुपये तक की रियायती पूंजी।\n\n"
                    "आपकी शैक्षणिक योग्यता क्या है और आप किस राज्य के निवासी हैं? इससे मैं आपके लिए सबसे उपयुक्त योजनाएं चिन्हित कर सकूंगा।"
                )
            else:
                response_text = (
                    f"{name_salutation}India offers several employment, skill development, and self-employment initiatives for unemployed youth and job seekers:\n\n"
                    "1. **Skill Training (PMKVY 4.0)**: Free industry-aligned vocational certifications under Skill India.\n"
                    "2. **Apprenticeships (NATS)**: Practical 1-year industry training with monthly stipend for graduates and diploma holders.\n"
                    "3. **Self-Employment (PMEGP & PM Mudra)**: Collateral-free loans and subsidies up to Rs. 50 Lakhs to start an enterprise.\n\n"
                    "To accurately identify eligible programs, what is your educational qualification, and which State do you reside in?"
                )

        if lang == "te":
            follow_up = "మీరు ఏ రాష్ట్రం లేదా కేంద్రపాలిత ప్రాంతంలో నివసిస్తున్నారు?"
        elif lang == "hi":
            follow_up = "आप किस राज्य या केंद्र शासित प्रदेश के निवासी हैं?"
        else:
            follow_up = "Which State or Union Territory do you reside in?"

        session["history"].append({"role": "assistant", "message": response_text})
        return {
            "status": "success",
            "intent": intent,
            "message": response_text,
            "follow_up_question": follow_up,
            "updated_profile": session["profile"],
            "schemes": [],
            "requires_schemes_display": False,
            "ai_status": get_ai_config()
        }

    # -------------------------------------------------------------
    # CASE E: SCHOLARSHIPS SEARCH ("I need a scholarship")
    # -------------------------------------------------------------
    if intent == IntentType.SCHOLARSHIP_SEARCH:
        session["pending_question_topic"] = "scholarship_details"
        edu = session["profile"].get("education")
        st = session["profile"].get("state")
        inc = session["profile"].get("income")

        if edu and not st:
            if lang == "te":
                response_text = (
                    f"మీరు {edu} చదువుతున్నందుకు సంతోషం. ఇంజనీరింగ్ మరియు కళాశాల విద్యార్థుల కోసం భారతదేశంలో నేషనల్ స్కాలర్‌షిప్ పోర్టల్ (NSP), విద్యా లక్ష్మి ఎడ్యుకేషన్ లోన్ పోర్టల్, AICTE సాంకేతిక స్కాలర్‌షిప్‌లు, మరియు రాష్ట్ర ప్రభుత్వ ఫీజు రీయింబర్స్‌మెంట్ పథకాలు అందుబాటులో ఉన్నాయి.\n\n"
                    "మీకు సరిగ్గా వర్తించే స్కాలర్‌షిప్‌లను సరిపోల్చడానికి: మీరు ఏ రాష్ట్రంలో చదువుతున్నారు లేదా నివసిస్తున్నారు? అలాగే మీ కుటుంబ సుమారు వార్షిక ఆదాయం ఎంత?"
                )
                follow_up = "మీరు ఏ రాష్ట్రంలో చదువుతున్నారు లేదా నివసిస్తున్నారు? అలాగే మీ కుటుంబ సుమారు వార్షిక ఆదాయం ఎంత?"
            elif lang == "hi":
                response_text = f"आप {edu} कर रहे हैं। आपके लिए नेशनल स्कॉलरशिप पोर्टल (NSP) और विद्या लक्ष्मी पोर्टल जैसे अवसर उपलब्ध हैं। सही योजनाओं के लिए, आप किस राज्य में पढ़ रहे हैं और आपकी वार्षिक पारिवारिक आय कितनी है?"
                follow_up = "आप किस राज्य में पढ़ रहे हैं और आपकी वार्षिक पारिवारिक आय कितनी है?"
            else:
                response_text = f"Since you are studying {edu}, opportunities like National Scholarship Portal (NSP), Vidya Lakshmi Education Loans, and State Fee Reimbursements are available. Which State is your institution located in, and what is your approximate annual family income?"
                follow_up = "Which State is your institution located in, and what is your annual family income?"
        elif not edu and not st:
            if lang == "te":
                response_text = "ఖచ్చితంగా! విద్యార్థుల కోసం అనేక కేంద్ర మరియు రాష్ట్ర ప్రభుత్వ స్కాలర్‌షిప్‌లు అందుబాటులో ఉన్నాయి. మీకు అర్హత ఉన్న ఖచ్చితమైన పథకాలను గుర్తించడానికి: మీరు ప్రస్తుతం ఏ కోర్సు లేదా తరగతి చదువుతున్నారు? మరియు మీరు ఏ రాష్ట్రంలో చదువుతున్నారు?"
                follow_up = "మీరు ప్రస్తుతం ఏ కోర్సు లేదా తరగతి చదువుతున్నారు? మరియు మీరు ఏ రాష్ట్రంలో చదువుతున్నారు?"
            elif lang == "hi":
                response_text = "छात्रवृत्ति पात्रता जांचने के लिए कुछ जानकारी आवश्यक है: आप वर्तमान में कौन सी कक्षा या कोर्स कर रहे हैं? और आप किस राज्य में पढ़ रहे हैं?"
                follow_up = "आप वर्तमान में कौन सी कक्षा या कोर्स कर रहे हैं? और किस राज्य में पढ़ रहे हैं?"
            else:
                response_text = "To accurately match scholarship programs, are you currently studying in school, intermediate, or college? Which course/degree and State are you studying in?"
                follow_up = "Which course and State are you studying in?"
        elif not st:
            if lang == "te":
                response_text = "మీ విద్యా సంస్థ ఏ రాష్ట్రం లేదా కేంద్రపాలిత ప్రాంతంలో ఉంది?"
            elif lang == "hi":
                response_text = "आपका शिक्षण संस्थान किस राज्य या केंद्र शासित प्रदेश में स्थित है?"
            else:
                response_text = "Which State or Union Territory is your educational institution located in?"
            follow_up = response_text
        else:
            # Both education and state are known -> Evaluate database for scholarships!
            matched = find_relevant_schemes_from_db(session["profile"], limit=4)
            if matched:
                session["profile"]["specific_scheme_id"] = matched[0]["id"]
                session["last_returned_scheme_ids"] = [s["id"] for s in matched]
                if lang == "te":
                    response_text = f"{st}లో {edu or 'విద్యార్థుల'} కోసం ధృవీకరించిన స్కాలర్‌షిప్ నిబంధనల ప్రకారం అర్హత గల {len(matched)} స్కాలర్‌షిప్ మరియు విద్యా సహాయ పథకాలను గుర్తించాము:"
                elif lang == "hi":
                    response_text = f"{st} में {edu or 'छात्रों'} के लिए सत्यापित छात्रवृत्ति नियमों के आधार पर {len(matched)} उपयुक्त छात्रवृत्ति और शुल्क सहायता योजनाएं पाई गई हैं:"
                else:
                    response_text = f"Analyzed verified scholarship criteria for {edu or 'students'} in {st}. Found {len(matched)} matching scholarship and fee support programs:"
                session["history"].append({"role": "assistant", "message": response_text})
                return {
                    "status": "success",
                    "intent": intent,
                    "message": response_text,
                    "follow_up_question": None,
                    "updated_profile": session["profile"],
                    "schemes": matched,
                    "requires_schemes_display": True,
                    "ai_status": get_ai_config()
                }

            else:
                if lang == "te":
                    response_text = "ప్రస్తుత సమాచారంతో సరిపోలే ప్రభుత్వ పథకాలు ఏవీ లభించలేదు. మీ రాష్ట్రం, వయస్సు లేదా ఆదాయ పరిమితులను సవరించి మళ్ళీ ప్రయత్నించండి."
                elif lang == "hi":
                    response_text = "वर्तमान जानकारी के साथ कोई प्रासंगिक योजना नहीं मिली। कृपया अपने राज्य, आयु या आय सीमा में बदलाव करके पुनः प्रयास करें।"
                else:
                    response_text = "No relevant schemes were found with the current information. Try relaxing search criteria, verifying income limits, or checking central pan-India options."

        session["history"].append({"role": "assistant", "message": response_text})
        return {
            "status": "success",
            "intent": IntentType.CLARIFICATION_REQUIRED,
            "message": response_text,
            "follow_up_question": follow_up,
            "updated_profile": session["profile"],
            "schemes": [],
            "requires_schemes_display": False,
            "ai_status": get_ai_config()
        }

    # -------------------------------------------------------------
    # CASE F: FARMER ASSISTANCE ("I am a farmer from Andhra Pradesh")
    # -------------------------------------------------------------
    if intent == IntentType.FARMER_ASSISTANCE:
        st = session["profile"].get("state")
        land = session["profile"].get("land")
        inc = session["profile"].get("income")

        if st and (land is None or inc is None):
            session["pending_question_topic"] = "farmer_land"
            if lang == "te":
                response_text = f"నమస్కారం! {st}లో కేంద్ర (PM-కిసాన్) మరియు రాష్ట్ర రైతు సంక్షేమ పథకాలు అమల్లో ఉన్నాయి. మీకు సరిపోయే సహాయాన్ని ఖరారు చేయడానికి, మీకు ఎన్ని ఎకరాల సాగు భూమి ఉంది మరియు వార్షిక కుటుంబ ఆదాయం ఎంత?"
                follow_up = "మీకు ఎన్ని ఎకరాల సాగు భూమి ఉంది మరియు వార్షిక కుటుంబ ఆదాయం ఎంత?"
            elif lang == "hi":
                response_text = f"स्वागत है! {st} में केंद्र (पीएम-किसान) और राज्य कृषि योजनाएं सक्रिय हैं। सटीक लाभ निर्धारित करने के लिए, आपके पास कितने एकड़ कृषि भूमि है और आपकी वार्षिक पारिवारिक आय क्या है?"
                follow_up = "आपके पास कितने एकड़ कृषि भूमि है और आपकी वार्षिक पारिवारिक आय क्या है?"
            else:
                response_text = f"Welcome! In {st}, both Central (PM-KISAN) and State agricultural welfare programs are active. To verify your exact benefit tier, how many acres of cultivable agricultural land do you own, and what is your approximate annual family income?"
                follow_up = "How many acres of agricultural land do you own?"

            session["history"].append({"role": "assistant", "message": response_text})
            return {
                "status": "success",
                "intent": IntentType.CLARIFICATION_REQUIRED,
                "message": response_text,
                "follow_up_question": follow_up,
                "updated_profile": session["profile"],
                "schemes": [],
                "requires_schemes_display": False,
                "ai_status": get_ai_config()
            }

    # -------------------------------------------------------------
    # CASE G: CLARIFICATION REQUIRED (Missing crucial eligibility details)
    # -------------------------------------------------------------
    if intent in [IntentType.SCHEME_SEARCH, IntentType.CLARIFICATION_REQUIRED]:
        follow_up = generate_follow_up_question(session["profile"], lang=lang)

        if follow_up:
            session["pending_question_topic"] = "clarification"
            prefix = ""
            if corrections:
                prefix = f"({', '.join(corrections)}) "

            if lang == "te":
                response_text = f"{prefix}మీ అవసరాలకు సరైన పథకాన్ని గుర్తించడానికి మరికొంత సమాచారం అవసరం: {follow_up}"
            elif lang == "hi":
                response_text = f"{prefix}आपकी आवश्यकता के अनुसार सटीक योजना खोजने के लिए कुछ और जानकारी आवश्यक है: {follow_up}"
            else:
                response_text = f"{prefix}To accurately identify eligible programs for you, I need a few additional details: {follow_up}"

            session["history"].append({"role": "assistant", "message": response_text})
            return {
                "status": "success",
                "intent": IntentType.CLARIFICATION_REQUIRED,
                "message": response_text,
                "follow_up_question": follow_up,
                "updated_profile": session["profile"],
                "schemes": [],
                "requires_schemes_display": False,
                "ai_status": get_ai_config()
            }

    # -------------------------------------------------------------
    # CASE H: ENOUGH DETAILS FOR REAL DATABASE MATCHING
    # -------------------------------------------------------------
    session["pending_question_topic"] = None
    matched_schemes = find_relevant_schemes_from_db(session["profile"], query_text=message, limit=6)

    # Empty State check
    if len(matched_schemes) == 0:
        if lang == "te":
            response_text = "ప్రస్తుత సమాచారంతో సరిపోలే ప్రభుత్వ పథకాలు ఏవీ లభించలేదు. మీ రాష్ట్రం, వయస్సు లేదా ఆదాయ పరిమితులను సవరించి మళ్ళీ ప్రయత్నించండి."
        elif lang == "hi":
            response_text = "वर्तमान जानकारी के साथ कोई प्रासंगिक योजना नहीं मिली। कृपया अपने राज्य, आयु या आय सीमा में बदलाव करके पुनः प्रयास करें।"
        else:
            response_text = "No relevant schemes were found with the current information. Try relaxing search criteria, verifying income limits, or checking central pan-India options."

        session["history"].append({"role": "assistant", "message": response_text})
        return {
            "status": "success",
            "intent": intent,
            "message": response_text,
            "follow_up_question": None,
            "updated_profile": session["profile"],
            "schemes": [],
            "requires_schemes_display": True,
            "ai_status": get_ai_config()
        }

    # Potential Matches Found from SQLite Database
    schemes_to_return = matched_schemes
    match_count = len(schemes_to_return)
    if schemes_to_return:
        session["profile"]["specific_scheme_id"] = schemes_to_return[0]["id"]
        session["last_returned_scheme_ids"] = [s["id"] for s in schemes_to_return]


    if lang == "te":
        response_text = f"మీ ప్రొఫైల్ వివరాలను ధృవీకరించిన డేటాబేస్ నిబంధనలతో సరిపోల్చాము. మీకు సరిపోలే {match_count} ప్రభుత్వ సంక్షేమ పథకాలను గుర్తించాము:"
    elif lang == "hi":
        response_text = f"आपके विवरण का सरकारी नियमों के आधार पर विश्लेषण किया गया। आपकी स्थिति के अनुकूल {match_count} प्रामाणिक योजनाएं पाई गई हैं:"
    else:
        response_text = f"Analyzed your information against verified government criteria. Found {match_count} relevant welfare programs matching your profile:"

    session["history"].append({"role": "assistant", "message": response_text})
    return {
        "status": "success",
        "intent": intent,
        "message": response_text,
        "follow_up_question": None,
        "updated_profile": session["profile"],
        "schemes": schemes_to_return,
        "requires_schemes_display": True,
        "ai_status": get_ai_config(),
        "disclaimer": "Preliminary eligibility evaluation only. Final approval rests with the respective government nodal authority."
    }
