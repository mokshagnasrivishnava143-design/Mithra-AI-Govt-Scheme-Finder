/**
 * GOVERNMENT SCHEME FINDER - CORE CLIENT LOGIC & ENGINE
 * Multilingual, Voice-First Benefits Discovery Platform
 * Pure Vanilla JavaScript (ES6+)
 */

'use strict';

/* ==========================================================================
   1. MULTILINGUAL DICTIONARY (English, Telugu, Hindi)
   ========================================================================== */
const TRANSLATIONS = {
  en: {
    skip_to_content: "Skip to main content",
    demo_badge: "Demonstration Prototype",
    announcement_text: "Direct official links to verified government portals. No Aadhaar or sensitive passwords collected.",
    accessibility_nav: "Accessibility",
    brand_subtitle: "Citizen Benefits Discovery",
    nav_home: "Home",
    nav_assistant: "Voice Assistant",
    nav_wizard: "Eligibility Wizard",
    nav_schemes: "Discover Schemes",
    nav_how_it_works: "How It Works",
    select_language: "Select Language",
    header_cta: "Find Benefits",
    hero_pill: "Multilingual • Voice-First • Privacy Preserving",
    hero_title: "Government Benefits, Made Simple.",
    hero_desc: "Discover government schemes that may match your needs, understand eligibility, and find official application links in your preferred language.",
    cta_find_schemes: "Find My Schemes",
    cta_explore: "Explore How It Works",
    cta_talk_assistant: "Talk to AI Assistant",
    trust_privacy: "No Aadhaar or sensitive passwords asked",
    trust_speed: "Instant match in under 60 seconds",
    trust_official: "Official .gov.in verified portals",
    hero_pill_match: "Personalized Match Found",
    badge_match_pct: "96% Match",
    assistant_tag: "Voice-First AI Discovery",
    assistant_title: "Let's Find Your Benefits",
    assistant_subtitle: "Speak or type in Telugu, Hindi, or English. Tell us about your occupation, family, state, or financial need, and our assistant will instantly find matching programs.",
    agent_name: "Mitra AI Citizen Copilot",
    assistant_welcome_text: "Hello! I am Mitra, your citizen benefit assistant. Tell me about your profession, family income, state, or financial need in Telugu, Hindi, or English. You can speak using the microphone or type below.",
    agent_ready: "Ready • Browser Speech Enabled",
    agent_listening: "Listening to your voice...",
    agent_processing: "Analyzing your request...",
    agent_analyzing: "Analyzing eligibility rules against verified government databases...",
    speak_in: "Language:",
    tts_on: "Voice Audio: ON",
    tts_off: "Voice Audio: OFF",
    btn_stop_audio: "Stop Audio",
    btn_clear_chat: "Clear Chat",
    chat_user_you: "You",
    live_listening: "Listening live...",
    scheme_view_details: "View Details & Eligibility",
    official_portal_link: "Official Portal ↗",
    verified_record_tag: "Verified Public Record",
    docs_count_tag: "Required Documents",
    mic_prompt: "Click the microphone and speak your situation, or pick an example prompt below.",
    mic_listening_prompt: "Listening... Speak clearly into your microphone.",
    btn_start_listening: "Start Listening",
    btn_stop_listening: "Stop Listening",
    mic_active_instruction: "Listening... Speak continuously with natural pauses. Click Stop when finished.",
    mic_paused_instruction: "Listening stopped. You can edit your text above or click Ask Assistant.",
    mic_err_not_allowed: "Microphone permission blocked. Please allow mic access in browser settings.",
    mic_err_no_speech: "No speech detected. Please check your mic and try speaking again.",
    mic_err_network: "Network issue during speech recognition. Please check connection.",
    mic_err_unsupported: "Speech recognition is not supported in this browser. Please use text search below.",
    assistant_placeholder: "e.g. Farmer with 2 acres in Telangana seeking income support...",
    btn_ask: "Ask Assistant",
    try_asking: "Try asking:",
    chip_farmer: "Farmer with 2 acres in Telangana",
    chip_student: "College student seeking scholarship",
    chip_woman_business: "Woman entrepreneur starting business",
    chip_health: "Senior citizen health coverage",
    chip_vendor: "Street vendor working capital loan",
    btn_listen: "Listen",
    btn_speaking: "Speaking...",
    tts_err_te_missing: "Telugu speech voice is not installed on this device/browser. Please install a Telugu voice pack in Windows Settings (Settings > Time & Language > Speech) to enable Telugu speech.",
    tts_err_hi_missing: "Hindi speech voice is not installed on this device/browser. Please install a Hindi voice pack in Windows Settings to enable Hindi speech.",
    btn_sync_profile: "Auto-fill Eligibility Wizard",
    wizard_tag: "Personalized Matching",
    wizard_title: "Check Your Exact Eligibility Match",
    wizard_subtitle: "Answer 4 simple questions. Your answers stay in your local browser and are evaluated securely against public criteria rules.",
    step_1_num: "Step 1",
    step_1_name: "Demographics",
    step_2_num: "Step 2",
    step_2_name: "Occupation & Income",
    step_3_num: "Step 3",
    step_3_name: "Category & Needs",
    step_4_num: "Step 4",
    step_4_name: "Review & Match",
    step1_heading: "Tell us about your age, gender, and state",
    step1_sub: "Many government programs have age limits or are specific to your domicile state.",
    label_age: "Your Age (Years)",
    hint_age: "Between 5 and 100 years",
    label_gender: "Gender",
    select_option: "-- Select Option --",
    gender_female: "Female",
    gender_male: "Male",
    gender_trans: "Transgender",
    gender_other: "Prefer not to say",
    label_state: "State or Union Territory",
    select_state: "-- Select State / UT --",
    btn_back: "Back",
    btn_continue: "Continue",
    step2_heading: "What is your occupation and family income?",
    step2_sub: "Benefits are tailored for farmers, students, entrepreneurs, and income tiers.",
    label_occupation: "Primary Occupation",
    select_occupation: "-- Select Occupation --",
    occ_farmer: "Farmer / Cultivator / Agri Labourer",
    occ_student: "Student / Scholar",
    occ_business: "Small Business / MSME / Trader",
    occ_vendor: "Street Vendor / Hawkers / Artisan",
    occ_unorganized: "Daily Wage / Construction Worker",
    occ_salaried: "Private / Salaried Employee",
    occ_senior: "Senior Citizen / Retired",
    occ_unemployed: "Unemployed / Job Seeker",
    label_income: "Annual Family Income",
    select_income: "-- Select Income Range --",
    inc_below_1l: "Below ₹1,00,000 / year (BPL Tier)",
    inc_1_25l: "₹1,00,000 to ₹2,50,000 / year",
    inc_25_5l: "₹2,50,000 to ₹5,00,000 / year",
    inc_5_8l: "₹5,00,000 to ₹8,00,000 / year (EWS Cap)",
    inc_above_8l: "Above ₹8,00,000 / year",
    label_land: "Agricultural Land Ownership",
    land_none: "No agricultural land owned",
    land_marginal: "Marginal Farmer (Up to 2.5 acres / 1 hectare)",
    land_small: "Small Farmer (2.5 to 5 acres / 1 - 2 hectares)",
    land_large: "Medium / Large Farmer (More than 5 acres)",
    hint_land: "Needed for schemes like PM-KISAN & State Rythu programs",
    step3_heading: "Special Criteria & Inclusion Categories",
    step3_sub: "Several flagship initiatives have specialized quotas, subsidies, or relaxed criteria.",
    label_category: "Social Category",
    cat_general: "General",
    cat_obc: "OBC (Other Backward Classes)",
    cat_sc: "SC (Scheduled Caste)",
    cat_st: "ST (Scheduled Tribe)",
    cat_ews: "EWS (Economically Weaker Section)",
    cat_minority: "Minority Community",
    label_disability: "Person with Disability (Divyangjan)?",
    opt_no: "No",
    opt_yes: "Yes (40% or more benchmark disability)",
    label_girl_child: "Family has girl child under 10 years",
    desc_girl_child: "Enables Sukanya Samriddhi and dedicated girl education schemes",
    label_ration: "Holds Ration Card / BPL / Antyodaya Card",
    desc_ration: "Prioritizes Ayushman Bharat healthcare and food security programs",
    btn_review_match: "Review & Match Schemes",
    step4_heading: "Confirm Your Profile Summary",
    step4_sub: "Review your inputs. Click \"Discover Matching Benefits\" to rank schemes with personalized match scores.",
    rev_age: "Age & Gender:",
    rev_state: "State:",
    rev_occ: "Occupation:",
    rev_income: "Annual Income:",
    rev_category: "Social Category:",
    rev_special: "Special Factors:",
    privacy_note: "Your data is stored in your local browser storage only. No central servers or third-party trackers are utilized.",
    btn_edit: "Edit Answers",
    btn_discover_benefits: "Discover Matching Benefits Now",
    schemes_tag: "Curated Benefits Catalog",
    schemes_title: "Explore Government Schemes",
    schemes_subtitle: "Verified central and state programs with accurate eligibility rules, required documents, and official application portals.",
    clear_profile: "Clear Profile Filter",
    search_schemes_ph: "Search by scheme name, keyword, or benefit amount...",
    filter_all_states: "All States / Central",
    sort_relevance: "Sort: Highest Match %",
    sort_amount: "Sort: Max Benefit Value",
    sort_name: "Sort: Scheme Name (A-Z)",
    cat_all: "All Categories",
    cat_agriculture: "Agriculture & Farmers",
    cat_education: "Education & Youth",
    cat_health: "Health & Wellness",
    cat_business: "Business, MSME & Loans",
    cat_women: "Women & Children",
    cat_social: "Social Security & Housing",
    showing_schemes: "Showing",
    schemes_found: "schemes",
    sample_data_note: "Verified Demonstration Records • Real Criteria",
    empty_title: "No matching schemes found",
    empty_desc: "Try relaxing your search terms, changing the category tab, or broadening your state filter.",
    btn_reset_filters: "Reset All Filters",
    how_tag: "Transparent & Simple",
    how_title: "How SchemeFinder Works",
    how_subtitle: "Three intuitive steps connecting citizens directly to eligible government welfare programs.",
    how_step1_title: "Tell Us About Your Needs",
    how_step1_desc: "Speak naturally in Telugu, Hindi, or English via voice assistant, or complete our 60-second eligibility wizard. No private Aadhaar or confidential documents are ever requested.",
    how_step1_link: "Try Voice Search →",
    how_step2_title: "Discover Potentially Relevant Schemes",
    how_step2_desc: "Our intelligent client-side rule engine compares your age, occupation, state, and income against thousands of public welfare conditions, ranking programs by match confidence.",
    how_step2_link: "Browse All Schemes →",
    how_step3_title: "Review Eligibility & Official Sources",
    how_step3_desc: "Inspect criteria side-by-side with your profile, tick off required documents, and follow direct verified links to apply on official government portals (.gov.in / .nic.in).",
    how_step3_link: "Start Wizard →",
    modal_benefit: "Benefit Amount",
    modal_match_score: "Match Confidence",
    modal_scope: "Applicability",
    modal_criteria_heading: "Eligibility Criteria Comparison",
    modal_criteria_sub: "How your current profile compares against the official rule parameters:",
    th_rule: "Parameter",
    th_scheme_req: "Scheme Requirement",
    th_your_info: "Your Information",
    th_status: "Status",
    modal_docs_heading: "Required Documents Readiness",
    modal_docs_sub: "Check off the documents you currently hold ready for submission:",
    modal_steps_heading: "How to Apply Officially",
    disclaimer_heading: "Important Public Advisory",
    disclaimer_body: "Final eligibility, verification, and disbursement are determined solely by the competent government department or nodal bank. SchemeFinder is an independent citizen discovery service and does not guarantee sanction, provide approvals, or collect government processing fees.",
    btn_print: "Print Document Checklist",
    btn_close: "Close",
    btn_visit_portal: "Visit Official Portal",
    saved_title: "Saved Schemes",
    btn_clear_saved: "Clear All Saved",
    a11y_title: "Accessibility Preferences",
    a11y_contrast: "High Contrast Mode",
    a11y_contrast_sub: "Enhances contrast and borders for low-vision readability.",
    a11y_text_size: "Text Size Adjustment",
    a11y_text_sub: "Adjust typography scaling across the application.",
    a11y_motion: "Reduce Animations",
    a11y_motion_sub: "Minimizes screen motion and transitions.",
    btn_done: "Save Preferences",
    footer_mission: "Empowering every Indian citizen to discover welfare entitlements easily through voice, vernacular languages, and transparent criteria matching.",
    available_in: "Available in:",
    footer_nav: "Navigation",
    footer_portals: "Official Portals",
    footer_trust: "Citizen Trust",
    trust_title: "Open Discovery Standard",
    trust_desc: "This client-side application evaluates publicly published scheme guidelines. All names and logos are copyright of their respective ministries.",
    footer_status: "National Hackathon Demonstration Edition"
  },

  te: {
    skip_to_content: "ప్రధాన విషయానికి వెళ్లండి",
    demo_badge: "డెమో ప్రొటోటైప్",
    announcement_text: "అధికారిక ప్రభుత్వ పోర్టళ్లకు ప్రత్యక్ష లింకులు. ఆధార్ లేదా గోప్యమైన సమాచారం తీసుకోబడదు.",
    accessibility_nav: "యాక్సెసిబిలిటీ",
    brand_subtitle: "ప్రజా సంక్షేమ పథకాల అన్వేషణ",
    nav_home: "హోమ్",
    nav_assistant: "వాయిస్ అసిస్టెంట్",
    nav_wizard: "అర్హత విజార్డ్",
    nav_schemes: "పథకాల అన్వేషణ",
    nav_how_it_works: "ఎలా పనిచేస్తుంది",
    select_language: "భాషను ఎంచుకోండి",
    header_cta: "పథకాలు కనుగొనండి",
    hero_pill: "బహుభాషా • వాయిస్ ఆధారిత • గోప్యత రక్షణ",
    hero_title: "ప్రభుత్వ పథకాలు, సులభంగా మీ కోసం.",
    hero_desc: "మీ అవసరాలకు తగిన ప్రభుత్వ పథకాలను తెలుసుకోండి, అర్హత నిబంధనలను అర్థం చేసుకోండి మరియు మీ సొంత భాషలో అధికారిక దరఖాస్తు లింకులను పొందండి.",
    cta_find_schemes: "నా పథకాలను వెతకండి",
    cta_explore: "ఇది ఎలా పనిచేస్తుందో చూడండి",
    cta_talk_assistant: "ఏఐ అసిస్టెంట్‌తో మాట్లాడండి",
    trust_privacy: "ఆధార్ లేదా రహస్య పాస్‌వర్డ్‌లు అడగబడవు",
    trust_speed: "60 సెకన్లలో సరిపోలే పథకాల గుర్తింపు",
    trust_official: "ధృవీకరించబడిన .gov.in అధికారిక పోర్టళ్లు",
    hero_pill_match: "సరిపోలే పథకం లభించింది",
    badge_match_pct: "96% అర్హత",
    assistant_tag: "వాయిస్ ఏఐ అసిస్టెంట్",
    assistant_title: "మీ సంక్షేమ ప్రయోజనాలను కనుగొనండి",
    assistant_subtitle: "తెలుగు, హిందీ లేదా ఇంగ్లీషులో మాట్లాడండి లేదా టైప్ చేయండి. మీ వృత్తి, కుటుంబ ఆదాయం, రాష్ట్రం చెప్పండి, మా అసిస్టెంట్ మీకు తగిన పథకాలను సూచిస్తుంది.",
    agent_name: "మిత్ర ఏఐ సంక్షేమ సహాయకుడు",
    assistant_welcome_text: "నమస్కారం! నేను మీ మిత్ర ఏఐ సంక్షేమ సహాయకుడిని. మీ వృత్తి, కుటుంబ ఆదాయం, రాష్ట్రం లేదా ఆర్థిక అవసరాల గురించి తెలుగు, హిందీ లేదా ఇంగ్లీషులో చెప్పండి. మైక్ ద్వారా మాట్లాడవచ్చు లేదా క్రింద టైప్ చేయవచ్చు.",
    agent_ready: "సిద్ధంగా ఉంది • బ్రౌజర్ వాయిస్ సపోర్ట్",
    agent_listening: "మీ మాట వింటున్నాను...",
    agent_processing: "విశ్లేషిస్తున్నాము...",
    agent_analyzing: "ప్రభుత్వ నిబంధనల ప్రకారం అర్హతను విశ్లేషిస్తున్నాము...",
    speak_in: "భాష:",
    tts_on: "వాయిస్ ఆడియో: ఆన్",
    tts_off: "వాయిస్ ఆడియో: ఆఫ్",
    btn_stop_audio: "వాయిస్ ఆపండి",
    btn_clear_chat: "చాట్ క్లియర్ చేయండి",
    chat_user_you: "మీరు",
    live_listening: "ప్రత్యక్షంగా వింటున్నాము...",
    scheme_view_details: "అర్హత వివరాలు చూడండి",
    official_portal_link: "అధికారిక పోర్టల్ ↗",
    verified_record_tag: "ధృవీకరించబడిన అధికారిక రికార్డు",
    docs_count_tag: "కావలసిన పత్రాలు",
    mic_prompt: "మైక్రోఫోన్‌పై క్లిక్ చేసి మాట్లాడండి లేదా క్రింది ఉదాహరణలను ఎంచుకోండి.",
    mic_listening_prompt: "వింటున్నాను... మైక్రోఫోన్‌లో స్పష్టంగా మాట్లాడండి.",
    btn_start_listening: "వాయిస్ ప్రారంభించండి",
    btn_stop_listening: "వాయిస్ ఆపండి",
    mic_active_instruction: "వింటున్నాను... నిరంతరంగా మాట్లాడండి. మధ్యలో ఆగవచ్చు. పూర్తయిన తర్వాత ఆపండి.",
    mic_paused_instruction: "వాయిస్ ఆపబడింది. పై వచనాన్ని సరిచూసి అసిస్టెంట్‌ను అడగండి.",
    mic_err_not_allowed: "మైక్రోఫోన్ అనుమతి నిరాకరించబడింది. దయచేసి బ్రౌజర్ సెట్టింగ్స్‌లో మైక్ అనుమతించండి.",
    mic_err_no_speech: "శబ్దం వినబడలేదు. దయచేసి మైక్ సరిచూసి మళ్ళీ మాట్లాడండి.",
    mic_err_network: "వాయిస్ గుర్తింపులో నెట్‌వర్క్ సమస్య ఏర్పడింది. ఇంటర్నెట్ కనెక్షన్ సరిచూసుకోండి.",
    mic_err_unsupported: "ఈ బ్రౌజర్‌లో వాయిస్ రికగ్నిషన్ సపోర్ట్ లేదు. దయచేసి క్రింద టైప్ చేయండి.",
    assistant_placeholder: "ఉదా: తెలంగాణలో 2 ఎకరాల భూమి ఉన్న రైతును, ఆర్థిక సహాయం కావాలి...",
    btn_ask: "అసిస్టెంట్‌ను అడగండి",
    try_asking: "ఇలా అడగండి:",
    chip_farmer: "తెలంగాణలో 2 ఎకరాలున్న రైతును",
    chip_student: "స్కాలర్‌షిప్ కోరుకుంటున్న విద్యార్థిని",
    chip_woman_business: "వ్యాపారం ప్రారంభించాలనుకుంటున్న మహిళను",
    chip_health: "వృద్ధులకు ఉచిత ఆరోగ్య బీమా",
    chip_vendor: "చిరు వ్యాపారులకు బ్యాంక్ లోన్",
    btn_listen: "వినండి",
    btn_speaking: "చదువుతోంది...",
    tts_err_te_missing: "ఈ పరికరంలో/బ్రౌజర్‌లో తెలుగు వాయిస్ లేదు. దయచేసి సిస్టమ్ సెట్టింగ్స్‌లో (Settings > Time & Language > Speech) తెలుగు వాయిస్ ప్యాక్ ఇన్‌స్టాల్ చేసుకోండి.",
    tts_err_hi_missing: "ఈ పరికరంలో హిందీ వాయిస్ లేదు. దయచేసి సిస్టమ్ సెట్టింగ్స్‌లో హిందీ వాయిస్ ప్యాక్ ఇన్‌స్టాల్ చేసుకోండి.",
    btn_sync_profile: "విజార్డ్‌లోకి వివరాలు పూరించండి",
    wizard_tag: "వ్యక్తిగత అర్హత తనిఖీ",
    wizard_title: "మీ ఖచ్చితమైన అర్హతను సరిచూసుకోండి",
    wizard_subtitle: "4 సులభమైన ప్రశ్నలకు సమాధానమివ్వండి. మీ సమాచారం మీ బ్రౌజర్‌లోనే భద్రంగా ఉంటుంది.",
    step_1_num: "దశ 1",
    step_1_name: "ప్రాథమిక వివరాలు",
    step_2_num: "దశ 2",
    step_2_name: "వృత్తి & ఆదాయం",
    step_3_num: "దశ 3",
    step_3_name: "వర్గం & ప్రత్యేక అర్హతలు",
    step_4_num: "దశ 4",
    step_4_name: "సమీక్ష & సరిపోల్చడం",
    step1_heading: "మీ వయస్సు, లింగం మరియు రాష్ట్రాన్ని తెలపండి",
    step1_sub: "చాలా ప్రభుత్వ పథకాలు వయస్సు పరిమితి లేదా నివాస రాష్ట్రం ఆధారంగా ఉంటాయి.",
    label_age: "మీ వయస్సు (సంవత్సరాలు)",
    hint_age: "5 నుండి 100 సంవత్సరాల మధ్య",
    label_gender: "లింగం",
    select_option: "-- ఎంచుకోండి --",
    gender_female: "స్త్రీ",
    gender_male: "పురుషుడు",
    gender_trans: "ట్రాన్స్‌జెండర్",
    gender_other: "చెప్పడానికి ఇష్టపడలేదు",
    label_state: "రాష్ట్రం / కేంద్రపాలిత ప్రాంతం",
    select_state: "-- రాష్ట్రాన్ని ఎంచుకోండి --",
    btn_back: "వెనుకకు",
    btn_continue: "కొనసాగించండి",
    step2_heading: "మీ వృత్తి మరియు కుటుంబ వార్షిక ఆదాయం ఎంత?",
    step2_sub: "రైతులు, విద్యార్థులు, వ్యాపారులు మరియు ఆదాయ పరిమితుల ఆధారంగా పథకాలు ఉంటాయి.",
    label_occupation: "ప్రధాన వృత్తి",
    select_occupation: "-- వృత్తిని ఎంచుకోండి --",
    occ_farmer: "రైతు / వ్యవసాయ కూలీ",
    occ_student: "విద్యార్థి / పరిశోధకుడు",
    occ_business: "చిన్న వ్యాపారం / ఎంఎస్‌ఎంఈ",
    occ_vendor: "వీధి వ్యాపారి / చేతివృత్తులు",
    occ_unorganized: "భవన నిర్మాణ కార్మికుడు / దినసరి కూలీ",
    occ_salaried: "ఉద్యోగి / ప్రైవేట్ ఉద్యోగం",
    occ_senior: "సీనియర్ సిటిజన్ / పదవీ విరమణ",
    occ_unemployed: "నిరుద్యోగి / ఉద్యోగార్ధి",
    label_income: "కుటుంబ వార్షిక ఆదాయం",
    select_income: "-- ఆదాయ పరిమితి ఎంచుకోండి --",
    inc_below_1l: "₹1,00,000 కంటే తక్కువ (బిపిఎల్ వర్గం)",
    inc_1_25l: "₹1,00,000 నుండి ₹2,50,000 వరకు",
    inc_25_5l: "₹2,50,000 నుండి ₹5,00,000 వరకు",
    inc_5_8l: "₹5,00,000 నుండి ₹8,00,000 వరకు (EWS)",
    inc_above_8l: "₹8,00,000 కంటే ఎక్కువ",
    label_land: "వ్యవసాయ భూమి వివరాలు",
    land_none: "వ్యవసాయ భూమి లేదు",
    land_marginal: "సన్నకారు రైతు (2.5 ఎకరాల లోపు)",
    land_small: "చిన్నకారు రైతు (2.5 నుండి 5 ఎకరాలు)",
    land_large: "మధ్య తరహా లేదా పెద్ద రైతు (5 ఎకరాలకు పైగా)",
    hint_land: "పీఎం-కిసాన్ మరియు రైతు బంధు పథకాలకు అవసరం",
    step3_heading: "సామాజిక వర్గం & ప్రత్యేక అంశాలు",
    step3_sub: "కొన్ని పథకాల్లో మహిళలు, దివ్యాంగులు లేదా ప్రత్యేక వర్గాలకు అదనపు ప్రయోజనాలు ఉంటాయి.",
    label_category: "సామాజిక వర్గం (Category)",
    cat_general: "జనరల్ (General)",
    cat_obc: "ఓబీసీ (OBC)",
    cat_sc: "ఎస్సీ (SC)",
    cat_st: "ఎస్టీ (ST)",
    cat_ews: "ఈడబ్ల్యూఎస్ (EWS)",
    cat_minority: "మైనారిటీ కమ్యూనిటీ",
    label_disability: "దివ్యాంగులా (దివ్యాంగ్ జన్)?",
    opt_no: "కాదు",
    opt_yes: "అవును (40% లేదా అంతకంటే ఎక్కువ)",
    label_girl_child: "కుటుంబంలో 10 సంవత్సరాల లోపు ఆడపిల్ల ఉంది",
    desc_girl_child: "సుకున్య సమృద్ధి మరియు బాలికల విద్య పథకాలకు అర్హత",
    label_ration: "రేషన్ కార్డు / బిపిఎల్ కార్డు ఉంది",
    desc_ration: "ఆయుష్మాన్ భారత్ మరియు ఉచిత రేషన్ ప్రాధాన్యత",
    btn_review_match: "సమీక్షించి సరిపోలే పథకాలు చూడండి",
    step4_heading: "మీ ప్రొఫైల్ వివరాలను నిర్ధారించండి",
    step4_sub: "మీరు నమోదు చేసిన సమాచారాన్ని సరిచూసుకొని \"సరిపోలే పథకాలు కనుగొనండి\" పై క్లిక్ చేయండి.",
    rev_age: "వయస్సు & లింగం:",
    rev_state: "రాష్ట్రం:",
    rev_occ: "వృత్తి:",
    rev_income: "వార్షిక ఆదాయం:",
    rev_category: "సామాజిక వర్గం:",
    rev_special: "ప్రత్యేక అంశాలు:",
    privacy_note: "మీ సమాచారం మీ బ్రౌజర్‌లో మాత్రమే ఉంటుంది. ఎటువంటి సర్వర్‌లకు పంపబడదు.",
    btn_edit: "సవరించండి",
    btn_discover_benefits: "సరిపోలే పథకాలను కనుగొనండి",
    schemes_tag: "సంక్షేమ పథకాల జాబితా",
    schemes_title: "ప్రభుత్వ పథకాలను పరిశీలించండి",
    schemes_subtitle: "ఖచ్చితమైన అర్హత నిబంధనలు, అవసరమైన పత్రాలు మరియు అధికారిక పోర్టల్ లింకులు.",
    clear_profile: "ఫిల్టర్ తొలగించండి",
    search_schemes_ph: "పథకం పేరు, కీవర్డ్ లేదా ప్రయోజనం ఆధారంగా శోధించండి...",
    filter_all_states: "అన్ని రాష్ట్రాలు / కేంద్ర పథకాలు",
    sort_relevance: "అత్యధిక అర్హత % క్రమంలో",
    sort_amount: "అధిక ప్రయోజన విలువ క్రమంలో",
    sort_name: "పథకం పేరు (A-Z) క్రమంలో",
    cat_all: "అన్ని రకాలు",
    cat_agriculture: "వ్యవసాయం & రైతులు",
    cat_education: "విద్య & యువత",
    cat_health: "ఆరోగ్యం & వైద్యం",
    cat_business: "వ్యాపారం, రుణాలు & MSME",
    cat_women: "మహిళలు & శిశు సంక్షేమం",
    cat_social: "సామాజిక భద్రత & గృహనిర్మాణం",
    showing_schemes: "మొత్తం",
    schemes_found: "పథకాలు కనుగొనబడ్డాయి",
    sample_data_note: "ధృవీకరించబడిన ప్రామాణిక రికార్డులు • వాస్తవ నియమాలు",
    empty_title: "ఎటువంటి పథకాలు లభించలేదు",
    empty_desc: "శోధన పదాలను మార్చండి లేదా ఫిల్టర్లను తొలగించి మళ్లీ ప్రయత్నించండి.",
    btn_reset_filters: "అన్ని ఫిల్టర్లను రీసెట్ చేయండి",
    how_tag: "పారదర్శకమైన విధానం",
    how_title: "స్కీమ్‌ఫైండర్ ఎలా పనిచేస్తుంది?",
    how_subtitle: "పౌరులను సరైన ప్రభుత్వ సంక్షేమ పథకాలతో అనుసంధానించే మూడు సులభమైన దశలు.",
    how_step1_title: "మీ వివరాలను తెలపండి",
    how_step1_desc: "తెలుగులో మాట్లాడి లేదా 60 సెకన్ల అర్హత ఫారమ్ నింపి మీ అవసరాలను చెప్పండి. ఆధార్ నంబర్ అవసరం లేదు.",
    how_step1_link: "వాయిస్ శోధన ప్రయత్నించండి →",
    how_step2_title: "సరిపోలే పథకాలను గుర్తించండి",
    how_step2_desc: "మా స్మార్ట్ అల్గారిథమ్ మీ వయస్సు, వృత్తి మరియు ఆదాయాన్ని సరిచూసి అర్హత శాతం లెక్కిస్తుంది.",
    how_step2_link: "అన్ని పథకాలు చూడండి →",
    how_step3_title: "పత్రాలు & అధికారిక దరఖాస్తు",
    how_step3_desc: "అవసరమైన ధృవపత్రాల చెక్‌లిస్ట్ చూసుకొని నేరుగా అధికారిక .gov.in పోర్టల్‌లో దరఖాస్తు చేసుకోండి.",
    how_step3_link: "ఫారమ్ ప్రారంభించండి →",
    modal_benefit: "ఆర్థిక ప్రయోజనం",
    modal_match_score: "అర్హత శాతం",
    modal_scope: "పరిధి",
    modal_criteria_heading: "అర్హత నిబంధనల పోలిక",
    modal_criteria_sub: "పథకం నిబంధనలకు మీ వివరాలు ఎలా సరిపోలుతున్నాయో చూడండి:",
    th_rule: "నిబంధన",
    th_scheme_req: "పథకం అవసరం",
    th_your_info: "మీ వివరాలు",
    th_status: "స్థితి",
    modal_docs_heading: "అవసరమైన పత్రాల చెక్‌లిస్ట్",
    modal_docs_sub: "మీ వద్ద సిద్ధంగా ఉన్న పత్రాలను టిక్ చేయండి:",
    modal_steps_heading: "దరఖాస్తు చేసుకునే విధానం",
    disclaimer_heading: "ముఖ్యమైన పౌర గమనిక",
    disclaimer_body: "తుది అర్హత మరియు నిధుల విడుదల సంబంధిత ప్రభుత్వ శాఖ లేదా బ్యాంకుల ద్వారా మాత్రమే నిర్ణయించబడుతుంది. స్కీమ్‌ఫైండర్ సమాచార సేవా వేదిక మాత్రమే.",
    btn_print: "పత్రాల చెక్‌లిస్ట్ ప్రింట్ చేయండి",
    btn_close: "మూసివేయి",
    btn_visit_portal: "అధికారిక పోర్టల్ సందర్శించండి",
    saved_title: "భద్రపరిచిన పథకాలు",
    btn_clear_saved: "అన్నింటినీ తొలగించు",
    a11y_title: "యాక్సెసిబిలిటీ ఎంపికలు",
    a11y_contrast: "హై కాంట్రాస్ట్ మోడ్",
    a11y_contrast_sub: "చూపు స్పష్టత కోసం స్క్రీన్ కాంట్రాస్ట్ పెంచుతుంది.",
    a11y_text_size: "అక్షరాల పరిమాణం",
    a11y_text_sub: "యాప్‌లోని అక్షరాల పరిమాణాన్ని మార్చండి.",
    a11y_motion: "యానిమేషన్లను తగ్గించండి",
    a11y_motion_sub: "స్క్రీన్ కదలికలను తగ్గిస్తుంది.",
    btn_done: "భద్రపరచండి",
    footer_mission: "ప్రతి భారతీయ పౌరుడికి సులభంగా, సొంత భాషలో, వాయిస్ ద్వారా ప్రభుత్వ సంక్షేమ పథకాలను అందించే లక్ష్యంతో రూపొందించబడింది.",
    available_in: "అందుబాటులో ఉన్న భాషలు:",
    footer_nav: "నావిగేషన్",
    footer_portals: "అధికారిక వెబ్‌సైట్లు",
    footer_trust: "పౌర విశ్వసనీయత",
    trust_title: "ఓపెన్ డిస్కవరీ ప్రమాణాలు",
    trust_desc: "ఈ అప్లికేషన్ అధికారిక ప్రభుత్వ మార్గదర్శకాల ఆధారంగా పనిచేస్తుంది. అన్ని పేర్లు సంబంధిత మంత్రిత్వ శాఖల ఆధీనంలో ఉంటాయి.",
    footer_status: "జాతీయ స్థాయి హ్యాకథాన్ ప్రదర్శన ఎడిషన్"
  },

  hi: {
    skip_to_content: "मुख्य सामग्री पर जाएं",
    demo_badge: "प्रदर्शन प्रोटोटाइप",
    announcement_text: "सत्यापित सरकारी पोर्टलों के सीधे आधिकारिक लिंक। कोई आधार या संवेदनशील पासवर्ड नहीं मांगा जाता।",
    accessibility_nav: "सुलभता (Accessibility)",
    brand_subtitle: "नागरिक कल्याण योजना खोज",
    nav_home: "होम",
    nav_assistant: "वॉइस असिस्टेंट",
    nav_wizard: "पात्रता विज़ार्ड",
    nav_schemes: "योजनाएं खोजें",
    nav_how_it_works: "यह कैसे काम करता है",
    select_language: "भाषा चुनें",
    header_cta: "योजनाएं खोजें",
    hero_pill: "बहुभाषी • वॉइस-फर्स्ट • गोपनीयता सुरक्षित",
    hero_title: "सरकारी योजनाएं, अब आपके लिए आसान।",
    hero_desc: "अपनी आवश्यकताओं से मेल खाने वाली सरकारी योजनाओं की खोज करें, पात्रता समझें और अपनी पसंदीदा भाषा में आधिकारिक आवेदन लिंक प्राप्त करें।",
    cta_find_schemes: "मेरी योजनाएं खोजें",
    cta_explore: "जानें कैसे काम करता है",
    cta_talk_assistant: "एआई सहायक से बात करें",
    trust_privacy: "आधार या गोपनीय पासवर्ड कभी नहीं पूछा जाता",
    trust_speed: "60 सेकंड के भीतर तुरंत योजना मिलान",
    trust_official: "सत्यापित .gov.in आधिकारिक पोर्टल",
    hero_pill_match: "व्यक्तिगत योजना मिलान मिला",
    badge_match_pct: "96% पात्रता",
    assistant_tag: "वॉइस-फर्स्ट एआई खोज",
    assistant_title: "आइए अपनी योजनाएं खोजें",
    assistant_subtitle: "हिंदी, तेलुगु या अंग्रेजी में बोलें या टाइप करें। अपने व्यवसाय, परिवार, राज्य या आवश्यकता के बारे में बताएं, हमारा असिस्टेंट तुरंत सही योजनाएं खोजेगा।",
    agent_name: "मित्र एआई कल्याण सहायक",
    assistant_welcome_text: "नमस्ते! मैं आपका मित्र एआई कल्याण सहायक हूँ। अपने व्यवसाय, पारिवारिक आय, राज्य या वित्तीय आवश्यकता के बारे में हिंदी, तेलुगु या अंग्रेजी में बताएं। आप माइक से बोल सकते हैं या नीचे लिख सकते हैं।",
    agent_ready: "तैयार • ब्राउज़र वॉइस सक्षम",
    agent_listening: "आपकी आवाज़ सुन रहे हैं...",
    agent_processing: "विश्लेषण कर रहे हैं...",
    agent_analyzing: "सरकारी नियमों के आधार पर पात्रता का विश्लेषण कर रहे हैं...",
    speak_in: "भाषा:",
    tts_on: "वॉइस ऑडियो: ऑन",
    tts_off: "वॉइस ऑडियो: ऑफ",
    btn_stop_audio: "ऑडियो रोकें",
    btn_clear_chat: "चैट साफ़ करें",
    chat_user_you: "आप",
    live_listening: "लाइव सुन रहे हैं...",
    scheme_view_details: "पात्रता और विवरण देखें",
    official_portal_link: "आधिकारिक पोर्टल ↗",
    verified_record_tag: "सत्यापित सार्वजनिक रिकॉर्ड",
    docs_count_tag: "आवश्यक दस्तावेज़",
    mic_prompt: "माइक बटन पर क्लिक करें और बोलें, या नीचे दिए गए उदाहरणों में से चुनें।",
    mic_listening_prompt: "सुन रहे हैं... कृपया स्पष्ट आवाज़ में बोलें।",
    btn_start_listening: "बोलना शुरू करें",
    btn_stop_listening: "बोलना बंद करें",
    mic_active_instruction: "सुन रहे हैं... निरंतर बोलें। स्वाभाविक रूप से रुक सकते हैं। पूरा होने पर बंद करें।",
    mic_paused_instruction: "रिकॉर्डिंग बंद हुई। आप ऊपर टेक्स्ट संपादित कर सकते हैं या असिस्टेंट से पूछें।",
    mic_err_not_allowed: "माइक्रोफ़ोन की अनुमति अस्वीकृत है। कृपया ब्राउज़र में माइक की अनुमति दें।",
    mic_err_no_speech: "कोई आवाज़ नहीं मिली। कृपया माइक जांचें और फिर से बोलें।",
    mic_err_network: "वॉइस पहचान में नेटवर्क त्रुटि हुई। कृपया इंटरनेट कनेक्शन जांचें।",
    mic_err_unsupported: "इस ब्राउज़र में वॉइस पहचान समर्थित नहीं है। कृपया नीचे लिखकर खोजें।",
    assistant_placeholder: "उदा. तेलंगाना में 2 एकड़ का किसान, आय सहायता चाहिए...",
    btn_ask: "असिस्टेंट से पूछें",
    try_asking: "यह पूछकर देखें:",
    chip_farmer: "तेलंगाना में 2 एकड़ भूमि वाला किसान",
    chip_student: "छात्रवृत्ति चाहने वाला कॉलेज छात्र",
    chip_woman_business: "नया व्यवसाय शुरू करने वाली महिला उद्यमी",
    chip_health: "वरिष्ठ नागरिकों के लिए स्वास्थ्य बीमा",
    chip_vendor: "स्ट्रीट वेंडर कार्यशील पूंजी ऋण",
    btn_listen: "सुनें",
    btn_speaking: "बोल रहा है...",
    tts_err_te_missing: "इस डिवाइस/ब्राउज़र पर तेलुगु वॉइस उपलब्ध नहीं है। कृपया सिस्टम सेटिंग्स (Settings > Time & Language > Speech) में तेलुगु वॉइस पैक इंस्टॉल करें।",
    tts_err_hi_missing: "इस डिवाइस/ब्राउज़र पर हिंदी वॉइस उपलब्ध नहीं है। कृपया सिस्टम सेटिंग्स में हिंदी वॉइस पैक इंस्टॉल करें।",
    btn_sync_profile: "विज़ार्ड में जानकारी भरें",
    wizard_tag: "व्यक्तिगत पात्रता जांच",
    wizard_title: "अपनी सटीक पात्रता की जांच करें",
    wizard_subtitle: "4 आसान प्रश्नों के उत्तर दें। आपका डेटा आपके ब्राउज़र में सुरक्षित रहता है और नियमों से जांचा जाता है।",
    step_1_num: "चरण 1",
    step_1_name: "जनसांख्यिकी",
    step_2_num: "चरण 2",
    step_2_name: "व्यवसाय और आय",
    step_3_num: "चरण 3",
    step_3_name: "वर्ग और विशेष आवश्यकताएं",
    step_4_num: "चरण 4",
    step_4_name: "समीक्षा और मिलान",
    step1_heading: "अपनी आयु, लिंग और राज्य बताएं",
    step1_sub: "कई सरकारी योजनाएं आयु सीमा या गृह राज्य के आधार पर होती हैं।",
    label_age: "आपकी आयु (वर्ष)",
    hint_age: "5 से 100 वर्ष के बीच",
    label_gender: "लिंग",
    select_option: "-- विकल्प चुनें --",
    gender_female: "महिला",
    gender_male: "पुरुष",
    gender_trans: "ट्रांसजेंडर",
    gender_other: "बताना नहीं चाहते",
    label_state: "राज्य या केंद्र शासित प्रदेश",
    select_state: "-- राज्य चुनें --",
    btn_back: "पीछे",
    btn_continue: "आगे बढ़ें",
    step2_heading: "आपका प्राथमिक व्यवसाय और पारिवारिक आय क्या है?",
    step2_sub: "योजनाएं किसानों, छात्रों, उद्यमियों और विभिन्न आय वर्गों के अनुसार तैयार की जाती हैं।",
    label_occupation: "मुख्य व्यवसाय",
    select_occupation: "-- व्यवसाय चुनें --",
    occ_farmer: "किसान / खेतिहर मजदूर",
    occ_student: "छात्र / शोधार्थी",
    occ_business: "लघु व्यवसाय / एमएसएमई / व्यापारी",
    occ_vendor: "स्ट्रीट वेंडर / फेरीवाले / कारीगर",
    occ_unorganized: "दैनिक वेतनभोगी / निर्माण श्रमिक",
    occ_salaried: "निजी / वेतनभोगी कर्मचारी",
    occ_senior: "वरिष्ठ नागरिक / सेवानिवृत्त",
    occ_unemployed: "बेरोजगार / नौकरी की तलाश",
    label_income: "वार्षिक पारिवारिक आय",
    select_income: "-- आय सीमा चुनें --",
    inc_below_1l: "₹1,00,000 प्रति वर्ष से कम (BPL श्रेणी)",
    inc_1_25l: "₹1,00,000 से ₹2,50,000 प्रति वर्ष",
    inc_25_5l: "₹2,50,000 से ₹5,00,000 प्रति वर्ष",
    inc_5_8l: "₹5,00,000 से ₹8,00,000 प्रति वर्ष (EWS सीमा)",
    inc_above_8l: "₹8,00,000 प्रति वर्ष से अधिक",
    label_land: "कृषि भूमि स्वामित्व",
    land_none: "कोई कृषि भूमि नहीं है",
    land_marginal: "सीमांत किसान (2.5 एकड़ / 1 हेक्टेयर तक)",
    land_small: "लघु किसान (2.5 से 5 एकड़ तक)",
    land_large: "मध्यम या बड़े किसान (5 एकड़ से अधिक)",
    hint_land: "पीएम-किसान और राज्य कृषि योजनाओं के लिए आवश्यक",
    step3_heading: "सामाजिक वर्ग और विशेष श्रेणियां",
    step3_sub: "कई प्रमुख योजनाओं में महिलाओं, दिव्यांगों या विशेष वर्गों के लिए विशेष कोटा या छूट होती है।",
    label_category: "सामाजिक वर्ग (Category)",
    cat_general: "सामान्य (General)",
    cat_obc: "ओबीसी (OBC)",
    cat_sc: "एससी (SC)",
    cat_st: "एसटी (ST)",
    cat_ews: "ईडब्ल्यूएस (EWS)",
    cat_minority: "अल्पसंख्यक समुदाय",
    label_disability: "क्या आप दिव्यांगजन हैं?",
    opt_no: "नहीं",
    opt_yes: "हाँ (40% या अधिक बेंचमार्क दिव्यांगता)",
    label_girl_child: "परिवार में 10 वर्ष से कम आयु की बेटी है",
    desc_girl_child: "सुकन्या समृद्धि और बालिका शिक्षा योजनाओं के लिए पात्र",
    label_ration: "राशन कार्ड / बीपीएल / अंत्योदय कार्ड धारक",
    desc_ration: "आयुष्मान भारत स्वास्थ्य और खाद्य सुरक्षा को प्राथमिकता",
    btn_review_match: "समीक्षा करें और योजनाएं देखें",
    step4_heading: "अपने प्रोफाइल सारांश की पुष्टि करें",
    step4_sub: "अपने विवरण की समीक्षा करें और व्यक्तिगत मिलान स्कोर देखने के लिए \"योजनाएं खोजें\" पर क्लिक करें।",
    rev_age: "आयु और लिंग:",
    rev_state: "राज्य:",
    rev_occ: "व्यवसाय:",
    rev_income: "वार्षिक आय:",
    rev_category: "सामाजिक वर्ग:",
    rev_special: "विशेष कारक:",
    privacy_note: "आपका डेटा केवल आपके ब्राउज़र में रहता है। किसी भी सर्वर पर नहीं भेजा जाता।",
    btn_edit: "संशोधित करें",
    btn_discover_benefits: "पात्र योजनाएं खोजें",
    schemes_tag: "योजना सूची",
    schemes_title: "सरकारी योजनाएं देखें",
    schemes_subtitle: "सटीक पात्रता नियमों, आवश्यक दस्तावेजों और आधिकारिक आवेदन पोर्टलों के साथ सत्यापित योजनाएं।",
    clear_profile: "प्रोफाइल फ़िल्टर हटाएं",
    search_schemes_ph: "योजना का नाम, कीवर्ड या लाभ राशि से खोजें...",
    filter_all_states: "सभी राज्य / केंद्रीय योजनाएं",
    sort_relevance: "क्रम: उच्चतम मिलान %",
    sort_amount: "क्रम: अधिकतम लाभ राशि",
    sort_name: "क्रम: योजना का नाम (A-Z)",
    cat_all: "सभी श्रेणियां",
    cat_agriculture: "कृषि और किसान",
    cat_education: "शिक्षा और युवा",
    cat_health: "स्वास्थ्य और कल्याण",
    cat_business: "व्यापार, ऋण और MSME",
    cat_women: "महिला एवं बाल विकास",
    cat_social: "सामाजिक सुरक्षा एवं आवास",
    showing_schemes: "कुल",
    schemes_found: "योजनाएं मिलीं",
    sample_data_note: "सत्यापित प्रामाणिक रिकॉर्ड • वास्तविक मानदंड",
    empty_title: "कोई योजना नहीं मिली",
    empty_desc: "खोज शब्दों को बदलें या फ़िल्टर रीसेट करके पुनः प्रयास करें।",
    btn_reset_filters: "सभी फ़िल्टर रीसेट करें",
    how_tag: "पारदर्शी और सरल",
    how_title: "स्कीमफाइंडर कैसे काम करता है?",
    how_subtitle: "नागरिकों को सीधे योग्य सरकारी योजनाओं से जोड़ने वाले तीन सरल चरण।",
    how_step1_title: "अपनी ज़रूरतें बताएं",
    how_step1_desc: "हिंदी में बोलकर या 60 सेकंड का विज़ार्ड पूरा करके अपनी स्थिति बताएं। किसी आधार या संवेदनशील दस्तावेज़ की आवश्यकता नहीं।",
    how_step1_link: "वॉइस सर्च आज़माएं →",
    how_step2_title: "उपयुक्त योजनाएं खोजें",
    how_step2_desc: "हमारा स्मार्ट एल्गोरिदम आपकी आयु, व्यवसाय और आय की जांच कर पात्रता प्रतिशत की गणना करता है।",
    how_step2_link: "सभी योजनाएं देखें →",
    how_step3_title: "दस्तावेज़ और आधिकारिक आवेदन",
    how_step3_desc: "दस्तावेज़ चेकलिस्ट की समीक्षा करें और आधिकारिक .gov.in पोर्टल पर सीधे आवेदन करें।",
    how_step3_link: "विज़ार्ड शुरू करें →",
    modal_benefit: "लाभ राशि",
    modal_match_score: "मिलान स्कोर",
    modal_scope: "दायरा",
    modal_criteria_heading: "पात्रता मानदंड तुलना",
    modal_criteria_sub: "योजना के नियमों के साथ आपकी जानकारी की तुलना:",
    th_rule: "मानदंड",
    th_scheme_req: "योजना आवश्यकता",
    th_your_info: "आपकी जानकारी",
    th_status: "स्थिति",
    modal_docs_heading: "आवश्यक दस्तावेज़ चेकलिस्ट",
    modal_docs_sub: "जो दस्तावेज़ आपके पास तैयार हैं, उन्हें टिक करें:",
    modal_steps_heading: "आधिकारिक आवेदन प्रक्रिया",
    disclaimer_heading: "महत्वपूर्ण सार्वजनिक सूचना",
    disclaimer_body: "अंतिम पात्रता, सत्यापन और स्वीकृति केवल संबंधित सरकारी विभाग या बैंक द्वारा तय की जाती है। स्कीमफाइंडर केवल एक स्वतंत्र नागरिक खोज सेवा है।",
    btn_print: "चेकलिस्ट प्रिंट करें",
    btn_close: "बंद करें",
    btn_visit_portal: "आधिकारिक पोर्टल पर जाएं",
    saved_title: "सहेजी गई योजनाएं",
    btn_clear_saved: "सभी हटाएं",
    a11y_title: "सुलभता प्राथमिकताएं",
    a11y_contrast: "उच्च कंट्रास्ट मोड",
    a11y_contrast_sub: "कम दृष्टि वाले उपयोगकर्ताओं के लिए पठनीयता बढ़ाता है।",
    a11y_text_size: "टेक्स्ट का आकार",
    a11y_text_sub: "एप्लिकेशन में फ़ॉन्ट का आकार बदलें।",
    a11y_motion: "एनीमेशन कम करें",
    a11y_motion_sub: "स्क्रीन मूवमेंट और मोशन को कम करता है।",
    btn_done: "प्राथमिकताएं सहेजें",
    footer_mission: "प्रत्येक भारतीय नागरिक को आवाज़, अपनी भाषा और पारदर्शी पात्रता के माध्यम से कल्याणकारी योजनाओं तक आसानी से पहुंचाने का प्रयास।",
    available_in: "उपलब्ध भाषाएं:",
    footer_nav: "नेविगेशन",
    footer_portals: "आधिकारिक पोर्टल",
    footer_trust: "नागरिक विश्वास",
    trust_title: "ओपन डिस्कवरी मानक",
    trust_desc: "यह एप्लिकेशन सार्वजनिक सरकारी दिशानिर्देशों के आधार पर काम करता है। सभी नाम और ट्रेडमार्क संबंधित मंत्रालयों के कॉपीराइट हैं।",
    footer_status: "राष्ट्रीय हैकाथॉन प्रदर्शन संस्करण"
  }
};

/* ==========================================================================
   2. AUTHENTIC GOVERNMENT SCHEMES DATASET
   Accurate public criteria, real department names, official .gov.in links
   ========================================================================== */
const SCHEMES_DATA = [
  {
    id: "pm-kisan",
    title: "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
    acronym: "PM-KISAN",
    department: "Ministry of Agriculture & Farmers Welfare",
    category: "agriculture",
    scope: "Central (All States)",
    benefit: "₹6,000 / Year (₹2,000 in 3 installments)",
    benefitValue: 6000,
    description: "Direct income support transfer to all cultivable landholding farmer families across India, credited directly to DBT-linked bank accounts.",
    criteria: {
      minAge: 18,
      maxAge: 100,
      gender: "all",
      incomeMax: 2000000, // Open to all landholding farmers except institutional/taxpayers
      occupations: ["farmer"],
      states: ["all"],
      requiresLand: true,
      requiresGirlChild: false,
      requiresBpl: false,
      summary: "Cultivable agricultural landholding in own name; excludes institutional landholders, tax payers, and constitutional post holders."
    },
    documents: [
      "Aadhaar Card linked with mobile number",
      "Land Ownership Documents (RoR / Khatian / Patta)",
      "Bank Account Passbook (Aadhaar & NPCI linked)",
      "Active Mobile Number for OTP Verification"
    ],
    officialUrl: "https://pmkisan.gov.in/",
    applicationSteps: [
      { step: "Visit Official Portal", text: "Go to pmkisan.gov.in and click on 'New Farmer Registration'." },
      { step: "Aadhaar e-KYC Verification", text: "Enter your 12-digit Aadhaar number and verify using OTP received on linked mobile." },
      { step: "Enter Land & Bank Details", text: "Upload survey number, khata number, and bank account number for DBT clearance." },
      { step: "State Verification & Sanction", text: "District agriculture officer verifies the record; installments disburse quarterly." }
    ]
  },

  {
    id: "ayushman-bharat",
    title: "Ayushman Bharat PM-JAY (Pradhan Mantri Jan Arogya Yojana)",
    acronym: "PM-JAY",
    department: "National Health Authority (NHA) / Ministry of Health",
    category: "health",
    scope: "Central (All States)",
    benefit: "₹5,00,000 Free Health Cover per Family per Year",
    benefitValue: 500000,
    description: "World's largest government-funded healthcare assurance scheme offering cashless secondary and tertiary hospitalization to vulnerable families.",
    criteria: {
      minAge: 0,
      maxAge: 100,
      gender: "all",
      incomeMax: 250000,
      occupations: ["unorganized", "farmer", "vendor", "unemployed", "senior"],
      states: ["all"],
      requiresLand: false,
      requiresGirlChild: false,
      requiresBpl: true,
      summary: "Families identified in SECC 2011 deprivation criteria, active Ration card holders, or senior citizens aged 70+ (universal coverage)."
    },
    documents: [
      "Aadhaar Card or Valid Government Photo ID",
      "Ration Card / BPL Card / Family ID",
      "Active Mobile Number"
    ],
    officialUrl: "https://pmjay.gov.in/",
    applicationSteps: [
      { step: "Check SECC / Ration Card Eligibility", text: "Visit beneficiary.nha.gov.in and verify mobile number." },
      { step: "e-KYC Verification", text: "Authenticate via Aadhaar OTP or biometric at nearest Common Service Center (CSC)." },
      { step: "Download Ayushman PVC Card", text: "Generate digital Ayushman Card with unique ABHA number for cashless treatment." }
    ]
  },

  {
    id: "pm-mudra",
    title: "Pradhan Mantri MUDRA Yojana (PMMY)",
    acronym: "PMMY",
    department: "Department of Financial Services / Ministry of Finance",
    category: "business",
    scope: "Central (All States)",
    benefit: "Collateral-Free Business Loans up to ₹10,00,000",
    benefitValue: 1000000,
    description: "Refinance and credit delivery to micro and small non-corporate enterprise units across Shishu (up to ₹50k), Kishore (up to ₹5L), and Tarun (up to ₹10L) tiers.",
    criteria: {
      minAge: 18,
      maxAge: 65,
      gender: "all",
      incomeMax: 5000000,
      occupations: ["business", "vendor", "unorganized"],
      states: ["all"],
      requiresLand: false,
      requiresGirlChild: false,
      requiresBpl: false,
      summary: "Non-farm micro-enterprises, artisans, shopkeepers, service sector units, and food processing entrepreneurs with no bank default."
    },
    documents: [
      "Identity Proof (Aadhaar / Voter ID / PAN)",
      "Business Address Proof / Udyam MSME Registration",
      "Bank Account Statement for last 6 months",
      "Quotation of machinery / project report"
    ],
    officialUrl: "https://www.mudra.org.in/",
    applicationSteps: [
      { step: "Prepare Business Proposal", text: "Draft unit details, required equipment cost, and estimated working capital." },
      { step: "Apply Online via UdyamiMitra", text: "Register on udyamimitra.in or visit any scheduled commercial bank / RRB." },
      { step: "Loan Sanction & MUDRA Card", text: "Receive MUDRA RuPay debit card for working capital withdrawal." }
    ]
  },

  {
    id: "vidya-lakshmi",
    title: "Vidya Lakshmi Education Portal & CSIS Interest Subsidy",
    acronym: "Vidya Lakshmi",
    department: "Department of Higher Education / Ministry of Education",
    category: "education",
    scope: "Central (All States)",
    benefit: "Full Interest Subsidy on Education Loans up to ₹10,00,000",
    benefitValue: 750000,
    description: "Single window portal for students seeking educational loans from 44+ public and private banks with full moratorium interest subsidy for economically weaker families.",
    criteria: {
      minAge: 16,
      maxAge: 35,
      gender: "all",
      incomeMax: 450000,
      occupations: ["student"],
      states: ["all"],
      requiresLand: false,
      requiresGirlChild: false,
      requiresBpl: false,
      summary: "Enrolled in recognized technical or professional higher education course; family annual gross income must not exceed ₹4.50 Lakhs."
    },
    documents: [
      "Admission Letter & Fee Schedule from recognized institution",
      "10th, 12th, or Degree Marksheets",
      "Competent Authority Income Certificate (< ₹4.5 Lakhs)",
      "Student & Parent Aadhaar Card and PAN"
    ],
    officialUrl: "https://www.vidyalakshmi.co.in/",
    applicationSteps: [
      { step: "Register on Vidya Lakshmi", text: "Create single student account on vidyalakshmi.co.in." },
      { step: "Fill Common Education Loan Form (CELAF)", text: "Provide course fees, family income, and academic scorecards." },
      { step: "Search & Select Bank Loan Scheme", text: "Apply to up to 3 banks simultaneously with one profile." }
    ]
  },

  {
    id: "pm-svanidhi",
    title: "PM SVANidhi (Street Vendor's AtmaNirbhar Nidhi)",
    acronym: "PM SVANidhi",
    department: "Ministry of Housing and Urban Affairs",
    category: "business",
    scope: "Central (Urban / Peri-urban)",
    benefit: "₹10,000 to ₹50,000 Working Capital with 7% Interest Subsidy",
    benefitValue: 50000,
    description: "Micro-credit facility enabling urban street vendors and roadside sellers to resume livelihoods, with cashback incentives for digital UPI transactions.",
    criteria: {
      minAge: 18,
      maxAge: 70,
      gender: "all",
      incomeMax: 250000,
      occupations: ["vendor", "unorganized"],
      states: ["all"],
      requiresLand: false,
      requiresGirlChild: false,
      requiresBpl: false,
      summary: "Street vendors vending in urban areas on or before March 24, 2020 with Vending Certificate or Letter of Recommendation (LoR)."
    },
    documents: [
      "Aadhaar Card linked to Mobile",
      "Vending Certificate / Urban Local Body ID Card or LoR",
      "Bank Account Details with IFSC",
      "Digital UPI QR Code handle for cashback"
    ],
    officialUrl: "https://pmsvanidhi.mohua.gov.in/",
    applicationSteps: [
      { step: "Check ULB Vendor Listing", text: "Check vendor survey status on pmsvanidhi.mohua.gov.in." },
      { step: "Apply through Portal or CSC", text: "Fill online application with preferred lending institution." },
      { step: "Disbursal & UPI Cashback", text: "Sanctioned amount credited to account; ₹100/month digital cashback on UPI transactions." }
    ]
  },

  {
    id: "pmay-urban-gramin",
    title: "PMAY (Pradhan Mantri Awas Yojana - Housing for All)",
    acronym: "PMAY",
    department: "Ministry of Housing and Urban Affairs / Rural Development",
    category: "social",
    scope: "Central (All States)",
    benefit: "Up to ₹2,67,000 Interest Subsidy / ₹1.30 Lakh Direct Grant",
    benefitValue: 267000,
    description: "Credit-linked interest subsidy for first-time pucca home construction or direct financial grant for homeless and kutcha-house dwelling families.",
    criteria: {
      minAge: 18,
      maxAge: 75,
      gender: "all",
      incomeMax: 800000,
      occupations: ["unorganized", "farmer", "vendor", "salaried", "unemployed"],
      states: ["all"],
      requiresLand: false,
      requiresGirlChild: false,
      requiresBpl: false,
      summary: "Beneficiary family must not own a pucca house in any part of India; female family head co-ownership preferred."
    },
    documents: [
      "Aadhaar Cards of all adult family members",
      "Income Certificate / Self-Declaration",
      "Land Ownership / Patta Document (for rural construction)",
      "Bank Account Passbook"
    ],
    officialUrl: "https://pmaymis.gov.in/",
    applicationSteps: [
      { step: "Online Citizen Assessment", text: "Apply under 'Citizen Assessment' at pmaymis.gov.in or via Gram Panchayat." },
      { step: "Field Verification", text: "Geo-tagging and site physical verification by municipal/panchayat team." },
      { step: "Direct Subsidy Credit", text: "Direct Benefit Transfer credited in milestones linked to house construction stages." }
    ]
  },

  {
    id: "nsp-scholarship",
    title: "National Scholarship Portal - Central Sector College Scheme",
    acronym: "NSP CS",
    department: "Department of Higher Education / Ministry of Education",
    category: "education",
    scope: "Central (All States)",
    benefit: "₹12,000 to ₹20,000 per Year during Degree / Post-Graduation",
    benefitValue: 20000,
    description: "Merit-cum-means scholarship for top-percentile college students from low-income families pursuing regular graduate and post-graduate university degrees.",
    criteria: {
      minAge: 17,
      maxAge: 26,
      gender: "all",
      incomeMax: 450000,
      occupations: ["student"],
      states: ["all"],
      requiresLand: false,
      requiresGirlChild: false,
      requiresBpl: false,
      summary: "Scored above 80th percentile in relevant stream in Class 12 board examination; family annual income under ₹4.50 Lakhs."
    },
    documents: [
      "Class 12th Board Marksheet & Certificate",
      "Annual Family Income Certificate",
      "Bonafide Student Certificate from College / University",
      "Aadhaar Card & Bank Account linked to student"
    ],
    officialUrl: "https://scholarships.gov.in/",
    applicationSteps: [
      { step: "One-Time Registration (OTR)", text: "Register on scholarships.gov.in using Aadhaar OTP." },
      { step: "Fill Central Sector Scheme Form", text: "Select your college and upload board score details." },
      { step: "Institute Verification", text: "College Nodal Officer verifies bonafide admission online." }
    ]
  },

  {
    id: "sukanya-samriddhi",
    title: "Sukanya Samriddhi Yojana (Beti Bachao Beti Padhao)",
    acronym: "SSY",
    department: "Ministry of Finance / Dept of Posts",
    category: "women",
    scope: "Central (All States)",
    benefit: "8.2% Guaranteed Annual Interest + Section 80C Tax Exemption",
    benefitValue: 150000,
    description: "Small deposit savings scheme for girl children to finance higher education and marriage, offering superior compounding interest backed by sovereign guarantee.",
    criteria: {
      minAge: 0,
      maxAge: 10,
      gender: "female",
      incomeMax: 10000000,
      occupations: ["all"],
      states: ["all"],
      requiresLand: false,
      requiresGirlChild: true,
      requiresBpl: false,
      summary: "Account opened by biological parents or legal guardians for girl child aged below 10 years; max 2 accounts per family."
    },
    documents: [
      "Girl Child Birth Certificate",
      "Parent / Legal Guardian Identity Proof (Aadhaar / PAN)",
      "Residential Address Proof",
      "Passport size photographs"
    ],
    officialUrl: "https://www.indiapost.gov.in/",
    applicationSteps: [
      { step: "Download Form", text: "Obtain Form SSA-1 from India Post website or nearest post office / bank." },
      { step: "Deposit Initial Amount", text: "Deposit minimum ₹250 initial deposit along with birth certificate." },
      { step: "Passbook Issuance", text: "Receive dedicated passbook; earn 8.2% sovereign quarterly compounded interest." }
    ]
  },

  {
    id: "standup-india",
    title: "Stand-Up India Scheme for Women and SC/ST Entrepreneurs",
    acronym: "Stand-Up India",
    department: "Department of Financial Services / SIDBI",
    category: "business",
    scope: "Central (All States)",
    benefit: "Bank Loans between ₹10,00,000 and ₹1,00,00,000",
    benefitValue: 5000000,
    description: "Facilitates bank loans between ₹10 Lakh and ₹1 Crore to at least one Scheduled Caste (SC) or Scheduled Tribe (ST) borrower and at least one woman borrower per bank branch.",
    criteria: {
      minAge: 18,
      maxAge: 65,
      gender: "all",
      incomeMax: 10000000,
      occupations: ["business", "unemployed", "unorganized"],
      states: ["all"],
      requiresLand: false,
      requiresGirlChild: false,
      requiresBpl: false,
      summary: "Must be a Woman or SC/ST entrepreneur starting a greenfield (first-time venture) in manufacturing, services, or trading sector."
    },
    documents: [
      "Identity Proof & Caste Certificate (for SC/ST)",
      "Project Report & Quotation for Capital Machinery",
      "PAN Card & Partnership Deed / Company MOA if non-individual",
      "Last 3 years IT returns of promoters (if available)"
    ],
    officialUrl: "https://www.standupmitra.in/",
    applicationSteps: [
      { step: "Register on Stand-Up Portal", text: "Register on standupmitra.in as trainee or ready borrower." },
      { step: "Select Bank & Branch", text: "Choose preferred commercial bank and upload business proposal." },
      { step: "Sanction & Handholding", text: "Bank branch evaluates viability and disburses composite term loan." }
    ]
  },

  {
    id: "rythu-bharosa-bandhu",
    title: "Rythu Bharosa / Rythu Bandhu Agriculture Investment Support",
    acronym: "Rythu Support",
    department: "Department of Agriculture (Telangana / Andhra Pradesh)",
    category: "agriculture",
    scope: "Telangana & Andhra Pradesh",
    benefit: "₹10,000 to ₹15,000 per Acre per Year Direct Subsidy",
    benefitValue: 15000,
    description: "State direct investment support scheme providing financial grant to farmers every season for purchasing seeds, fertilizer, and agricultural inputs.",
    criteria: {
      minAge: 18,
      maxAge: 90,
      gender: "all",
      incomeMax: 2000000,
      occupations: ["farmer"],
      states: ["Telangana", "Andhra Pradesh"],
      requiresLand: true,
      requiresGirlChild: false,
      requiresBpl: false,
      summary: "Resident farmer holding valid Pattadar Passbook in Telangana or registered in AP e-Crop / Land records."
    },
    documents: [
      "Pattadar Passbook / Dharani 1B ROR Record",
      "Aadhaar Card",
      "Bank Account Passbook (NPCI linked)",
      "Survey Number Land Map"
    ],
    officialUrl: "https://dharani.telangana.gov.in/",
    applicationSteps: [
      { step: "Verification in Land Records", text: "Ensure land details reflect correctly in Dharani portal or Webland." },
      { step: "Agriculture Extension Officer (AEO) Inspection", text: "Local AEO verifies active farming cultivation status." },
      { step: "Direct Treasury Credit", text: "Amount credited into bank account at start of Kharif and Rabi seasons." }
    ]
  },

  {
    id: "pm-matsya-sampada",
    title: "Pradhan Mantri Matsya Sampada Yojana (PMMSY)",
    acronym: "PMMSY",
    department: "Department of Fisheries / Ministry of Fisheries & Animal Husbandry",
    category: "agriculture",
    scope: "Central (All States)",
    benefit: "40% to 60% Capital Subsidy for Aquaculture & Biofloc",
    benefitValue: 300000,
    description: "Flagship scheme for focused and sustainable development of the fisheries sector with substantial government financial assistance for pond construction, biofloc, and cold chains.",
    criteria: {
      minAge: 18,
      maxAge: 70,
      gender: "all",
      incomeMax: 5000000,
      occupations: ["farmer", "business", "unorganized"],
      states: ["all"],
      requiresLand: false,
      requiresGirlChild: false,
      requiresBpl: false,
      summary: "Fishers, fish farmers, fish workers, SHGs, and entrepreneurs; 60% subsidy for Women and SC/ST, 40% for General category."
    },
    documents: [
      "Aadhaar Card & PAN Card",
      "Land Ownership / Long-term Lease Agreement for water body",
      "Detailed Project Report (DPR) with technical layout",
      "Bank Account Details"
    ],
    officialUrl: "https://pmmsy.dof.gov.in/",
    applicationSteps: [
      { step: "Submit DPR to District Fisheries Office", text: "Formulate technical project report and submit to district nodal officer." },
      { step: "State Approval & Sanction", text: "State Level Approval Committee (SLAC) evaluates feasibility." },
      { step: "Phased Subsidy Release", text: "Subsidy released directly in bank account matching physical construction milestones." }
    ]
  },

  {
    id: "atal-pension-yojana",
    title: "Atal Pension Yojana (APY - Guaranteed Social Security)",
    acronym: "APY",
    department: "PFRDA / Ministry of Finance",
    category: "social",
    scope: "Central (All States)",
    benefit: "Guaranteed Monthly Pension of ₹1,000 to ₹5,000 for Life",
    benefitValue: 60000,
    description: "Guaranteed lifelong pension scheme targeted especially at workers in unorganized sectors, providing financial security after age 60 with spouse cover.",
    criteria: {
      minAge: 18,
      maxAge: 40,
      gender: "all",
      incomeMax: 1000000,
      occupations: ["unorganized", "vendor", "farmer", "business", "unemployed"],
      states: ["all"],
      requiresLand: false,
      requiresGirlChild: false,
      requiresBpl: false,
      summary: "Indian citizen aged between 18 and 40 years holding a savings bank account; must not be an income taxpayer."
    },
    documents: [
      "Aadhaar Card",
      "Savings Bank Account with Auto-Debit facility",
      "Nominee details and spouse Aadhaar"
    ],
    officialUrl: "https://www.npscra.nsdl.co.in/",
    applicationSteps: [
      { step: "Visit Bank or Netbanking", text: "Access APY enrollment form at your bank branch or via mobile banking app." },
      { step: "Choose Pension Slab (₹1k - ₹5k)", text: "Select desired monthly pension tier and monthly auto-debit date." },
      { step: "Receive PRAN Acknowledgement", text: "Permanent Retirement Account Number (PRAN) issued with guaranteed pension guarantee." }
    ]
  }
];

/* ==========================================================================
   3. APPLICATION STATE MANAGEMENT
   ========================================================================== */
const AppState = {
  currentLang: 'en',
  activeCategory: 'all',
  searchQuery: '',
  stateFilter: 'all',
  levelFilter: 'all',
  sortBy: 'relevance',
  currentPage: 1,
  itemsPerPage: 12,
  totalPages: 1,
  totalCount: 0,
  
  // User Profile from Wizard
  userProfile: {
    age: null,
    gender: null,
    state: null,
    occupation: null,
    income: null,
    land: 'none',
    category: 'General',
    disability: 'no',
    girlChild: false,
    bpl: false,
    isComplete: false
  },

  // Saved / Bookmarked Scheme IDs
  savedSchemeIds: new Set(),

  // Backend Integration State
  latestSearchResultsMap: new Map(),
  isBackendConnected: false,

  // Speech Recognition & TTS
  speechRecognition: null,
  isListening: false,
  ttsEnabled: true,

  // Accessibility Preferences
  accessibility: {
    highContrast: false,
    fontScale: 1,
    reduceMotion: false
  }
};

/* ==========================================================================
   4. INITIALIZATION & DOM READY
   ========================================================================== */
document.addEventListener('DOMContentLoaded', () => {
  initStorage();
  initI18n();
  initAccessibility();
  initHeaderNavigation();
  initVoiceAssistant();
  initEligibilityWizard();
  initSchemesDiscovery();
  initEligibilityModal();
  initSavedDrawer();
  
  // Render initial catalog
  renderSchemes();
});

/**
 * Load persisted settings from localStorage
 */
function initStorage() {
  try {
    const savedBookmarks = localStorage.getItem('scheme_finder_saved');
    if (savedBookmarks) {
      const ids = JSON.parse(savedBookmarks);
      if (Array.isArray(ids)) {
        AppState.savedSchemeIds = new Set(ids);
      }
    }

    const savedA11y = localStorage.getItem('scheme_finder_a11y');
    if (savedA11y) {
      const parsed = JSON.parse(savedA11y);
      AppState.accessibility = { ...AppState.accessibility, ...parsed };
    }

    const savedLang = localStorage.getItem('scheme_finder_lang');
    if (savedLang && ['en', 'te', 'hi'].includes(savedLang)) {
      AppState.currentLang = savedLang;
    }
  } catch (err) {
    console.warn("Storage access restricted or unavailable:", err);
  }
  updateBookmarkBadge();
}

/* ==========================================================================
   5. LOCALIZATION & TRANSLATIONS (i18n)
   ========================================================================== */
function initI18n() {
  const langSelect = document.getElementById('lang-select');
  if (langSelect) {
    langSelect.value = AppState.currentLang;
    langSelect.addEventListener('change', (e) => {
      setLanguage(e.target.value);
    });
  }

  // Mobile drawer pills
  document.querySelectorAll('.lang-pill-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang');
      setLanguage(lang);
      document.querySelectorAll('.lang-pill-btn').forEach(b => b.classList.toggle('active', b === btn));
    });
  });

  applyTranslations();
}

function setLanguage(lang) {
  if (!TRANSLATIONS[lang]) return;
  AppState.currentLang = lang;
  try {
    localStorage.setItem('scheme_finder_lang', lang);
  } catch(e) {}

  // Gracefully stop active speech recognition before changing language
  if (AppState.isListening && AppState.speechRecognition) {
    try {
      AppState.speechRecognition.stop();
    } catch(e) {}
  }

  const langSelect = document.getElementById('lang-select');
  if (langSelect) langSelect.value = lang;

  // Sync assistant voice buttons
  updateVoiceLangButtons(lang);

  applyTranslations();
  renderSchemes();
  showToast(lang === 'te' ? 'భాష విజయవంతంగా మార్చబడింది' : (lang === 'hi' ? 'भाषा सफलतापूर्वक बदली गई' : 'Language updated to English'));
}

function updateVoiceLangButtons(lang) {
  const codeMap = { en: 'en-IN', te: 'te-IN', hi: 'hi-IN' };
  const targetCode = codeMap[lang] || 'en-IN';
  AppState.voiceLang = targetCode;
  document.querySelectorAll('.btn-toggle').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-voice-lang') === targetCode);
  });
}

function applyTranslations() {
  const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
  
  // Replace text for elements with data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  // Replace placeholders
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.getAttribute('data-i18n-ph');
    if (dict[key]) {
      el.placeholder = dict[key];
    }
  });

  document.documentElement.lang = AppState.currentLang;
}

/* ==========================================================================
   6. ACCESSIBILITY CONTROLS
   ========================================================================== */
function initAccessibility() {
  const a11yModal = document.getElementById('accessibility-modal');
  const toggleBtn = document.getElementById('toggle-accessibility-btn');
  const mobileToggleBtn = document.getElementById('open-accessibility-mobile');
  const closeBtn = document.getElementById('close-a11y-modal');
  const saveBtn = document.getElementById('save-a11y-btn');
  const contrastToggle = document.getElementById('a11y-contrast-toggle');
  const motionToggle = document.getElementById('a11y-motion-toggle');

  // Apply loaded prefs
  applyA11yClasses();

  if (contrastToggle) contrastToggle.checked = AppState.accessibility.highContrast;
  if (motionToggle) motionToggle.checked = AppState.accessibility.reduceMotion;

  const openModal = () => {
    a11yModal.classList.add('open');
    a11yModal.setAttribute('aria-hidden', 'false');
  };
  const closeModal = () => {
    a11yModal.classList.remove('open');
    a11yModal.setAttribute('aria-hidden', 'true');
  };

  if (toggleBtn) toggleBtn.addEventListener('click', openModal);
  if (mobileToggleBtn) mobileToggleBtn.addEventListener('click', openModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (saveBtn) saveBtn.addEventListener('click', closeModal);

  // Backdrop click
  a11yModal.addEventListener('click', (e) => {
    if (e.target === a11yModal) closeModal();
  });

  // Toggle Contrast
  if (contrastToggle) {
    contrastToggle.addEventListener('change', (e) => {
      AppState.accessibility.highContrast = e.target.checked;
      applyA11yClasses();
      persistA11y();
    });
  }

  // Toggle Motion
  if (motionToggle) {
    motionToggle.addEventListener('change', (e) => {
      AppState.accessibility.reduceMotion = e.target.checked;
      applyA11yClasses();
      persistA11y();
    });
  }

  // Font Scale buttons
  document.querySelectorAll('.font-size-btn').forEach(btn => {
    const scale = parseFloat(btn.getAttribute('data-scale'));
    if (Math.abs(AppState.accessibility.fontScale - scale) < 0.05) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }

    btn.addEventListener('click', () => {
      document.querySelectorAll('.font-size-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      AppState.accessibility.fontScale = scale;
      applyA11yClasses();
      persistA11y();
    });
  });
}

function applyA11yClasses() {
  document.body.classList.toggle('high-contrast', AppState.accessibility.highContrast);
  document.body.classList.toggle('reduce-motion', AppState.accessibility.reduceMotion);
  document.documentElement.style.setProperty('--font-scale', AppState.accessibility.fontScale);
}

function persistA11y() {
  try {
    localStorage.setItem('scheme_finder_a11y', JSON.stringify(AppState.accessibility));
  } catch(e) {}
}

/* ==========================================================================
   7. NAVIGATION & HEADER CONTROLS
   ========================================================================== */
function initHeaderNavigation() {
  const header = document.getElementById('site-header');
  const menuToggle = document.getElementById('mobile-menu-toggle');
  const drawer = document.getElementById('mobile-nav-drawer');
  const drawerClose = document.getElementById('mobile-drawer-close');

  // Sticky header shadow on scroll
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }, { passive: true });

  // Mobile menu drawer
  if (menuToggle && drawer) {
    menuToggle.addEventListener('click', () => {
      drawer.classList.add('open');
      drawer.setAttribute('aria-hidden', 'false');
      menuToggle.setAttribute('aria-expanded', 'true');
    });
  }

  const closeDrawer = () => {
    if (!drawer) return;
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    if (menuToggle) menuToggle.setAttribute('aria-expanded', 'false');
  };

  if (drawerClose) drawerClose.addEventListener('click', closeDrawer);

  document.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', closeDrawer);
  });
}

/* ==========================================================================
   8. VOICE-FIRST INTERACTIVE ASSISTANT
   Web Speech Recognition + SpeechSynthesis + Natural Language Intent Matching
   ========================================================================== */
function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[m]);
}

/* ==========================================================================
   SPEECH SYNTHESIS & TTS AUDIO ENGINE
   - Chromium GC prevention via window._activeUtterance
   - Dynamic voice resolution for en-IN, te-IN, hi-IN with graceful fallbacks
   - Keep-alive heartbeat against Chromium 15-second speech cutoff
   - Visual speaking indicators on individual message buttons
   - Independent manual Listen clicks vs. AppState.ttsEnabled auto-speech
   ========================================================================== */

let activeSpeakingButton = null;
let speechHeartbeatTimer = null;
let cachedVoices = [];
let activeAudioElement = null;

function loadSpeechVoices() {
  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    cachedVoices = window.speechSynthesis.getVoices() || [];
  }
}

// Pre-load voices and listen to async voiceschanged event
if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
  loadSpeechVoices();
  window.speechSynthesis.onvoiceschanged = () => {
    loadSpeechVoices();
  };
}

/**
 * Find the most suitable dedicated SpeechSynthesisVoice for the target language.
 * Strictly avoids using English voices to speak Telugu or Hindi!
 */
function getBestVoiceForLang(langCode) {
  if (!('speechSynthesis' in window)) return null;
  const voices = window.speechSynthesis.getVoices() || cachedVoices;
  if (!voices || voices.length === 0) return null;

  const target = (langCode || 'en-IN').toLowerCase().replace('_', '-');
  const targetPrefix = target.split('-')[0];

  // 1. Exact match (e.g. te-in, hi-in, en-in, te, hi, en)
  let voice = voices.find(v => v.lang && v.lang.toLowerCase().replace('_', '-') === target);
  if (voice) return voice;

  // 2. Language prefix match (e.g. te-..., hi-..., en-...)
  voice = voices.find(v => v.lang && v.lang.toLowerCase().startsWith(targetPrefix));
  if (voice) return voice;

  // 3. Name-based match for Telugu / Hindi (e.g. "Microsoft Mohan - Telugu", "Google Telugu")
  if (targetPrefix === 'te') {
    voice = voices.find(v => (v.name || '').toLowerCase().includes('telugu'));
    if (voice) return voice;
  } else if (targetPrefix === 'hi') {
    voice = voices.find(v => (v.name || '').toLowerCase().includes('hindi'));
    if (voice) return voice;
  } else if (targetPrefix === 'en') {
    // English can match Indian English or any English
    voice = voices.find(v => {
      const l = (v.lang || '').toLowerCase();
      const n = (v.name || '').toLowerCase();
      return l.startsWith('en') && (l.includes('in') || n.includes('india'));
    }) || voices.find(v => (v.lang || '').toLowerCase().startsWith('en')) || voices.find(v => v.default) || voices[0];
    if (voice) return voice;
  }

  return null; // Return null if no matching voice exists for Telugu or Hindi!
}

/**
 * Stop any current speech playback and restore UI buttons to idle state.
 */
function stopSpeech() {
  if (typeof window !== 'undefined' && window.speechSynthesis) {
    try {
      window.speechSynthesis.cancel();
    } catch(e) {}
  }

  if (activeAudioElement) {
    try {
      activeAudioElement.pause();
      activeAudioElement.src = '';
    } catch(e) {}
    activeAudioElement = null;
  }

  if (speechHeartbeatTimer) {
    clearInterval(speechHeartbeatTimer);
    speechHeartbeatTimer = null;
  }

  if (activeSpeakingButton) {
    activeSpeakingButton.classList.remove('is-speaking');
    const label = activeSpeakingButton.querySelector('.listen-label');
    const icon = activeSpeakingButton.querySelector('.listen-icon');
    const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
    if (label) label.textContent = dict.btn_listen || 'Listen';
    if (icon) icon.textContent = '🔊';
    activeSpeakingButton = null;
  }

  const stopBtn = document.getElementById('stop-speech-btn');
  if (stopBtn) stopBtn.style.display = 'none';

  window._activeUtterance = null;
}

/**
 * Fallback streaming TTS playback when device browser lacks local Indic voice packs.
 * Uses lightweight backend neural streaming endpoint.
 */
function playStreamingTTS(cleanText, targetLang, triggerBtn = null) {
  stopSpeech();
  const langCode = targetLang.startsWith('te') ? 'te' : (targetLang.startsWith('hi') ? 'hi' : 'en');
  const streamUrl = `/api/tts/stream?text=${encodeURIComponent(cleanText.slice(0, 500))}&lang=${langCode}`;

  const audio = new Audio();
  activeAudioElement = audio;

  const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;

  audio.onplay = () => {
    const stopBtn = document.getElementById('stop-speech-btn');
    if (stopBtn) stopBtn.style.display = 'inline-flex';

    if (triggerBtn) {
      activeSpeakingButton = triggerBtn;
      triggerBtn.classList.add('is-speaking');
      const label = triggerBtn.querySelector('.listen-label');
      const icon = triggerBtn.querySelector('.listen-icon');
      if (label) label.textContent = dict.btn_speaking || 'Speaking...';
      if (icon) icon.textContent = '⏹';
    }
  };

  audio.onended = () => {
    stopSpeech();
  };

  audio.onerror = (e) => {
    console.warn('Backend TTS streaming audio error:', e);
    stopSpeech();
    const errMsg = (langCode === 'te')
      ? (dict.tts_err_te_missing || "Telugu speech voice is not installed on this device/browser. Please install a Telugu voice pack in Windows Settings (Settings > Time & Language > Speech) to enable Telugu speech.")
      : (dict.tts_err_hi_missing || "Hindi speech voice is not installed on this device/browser. Please install a Hindi voice pack in system settings.");
    showToast(errMsg, 'warning');
  };

  try {
    audio.src = streamUrl;
    const playPromise = audio.play();
    if (playPromise !== undefined) {
      playPromise.catch(err => {
        console.warn('Audio play was prevented or failed:', err);
        stopSpeech();
        const errMsg = (langCode === 'te')
          ? (dict.tts_err_te_missing || "Telugu speech voice is not installed on this device/browser. Please install a Telugu voice pack in Windows Settings (Settings > Time & Language > Speech) to enable Telugu speech.")
          : (dict.tts_err_hi_missing || "Hindi speech voice is not installed on this device/browser. Please install a Hindi voice pack in system settings.");
        showToast(errMsg, 'warning');
      });
    }
  } catch (err) {
    console.error('Failed to initialize Audio streaming:', err);
    stopSpeech();
  }
}

/**
 * Speak the provided text aloud using Web Speech API SpeechSynthesis or neural stream fallback.
 * @param {string} text The text to speak.
 * @param {HTMLElement|null} triggerBtn Optional Listen button element for visual state binding.
 */
function speakText(text, triggerBtn = null) {
  if (!text) return;

  // 11. Voice Audio OFF must disable automatic speech (when triggerBtn is null)
  // but must NOT disable manual Listen button clicks (when triggerBtn is provided)
  if (triggerBtn === null && !AppState.ttsEnabled) {
    return;
  }

  // If user clicked the button of a message that is currently speaking, stop it (toggle off)
  const isSpeaking = (typeof window !== 'undefined' && window.speechSynthesis && window.speechSynthesis.speaking) ||
                     (activeAudioElement && !activeAudioElement.paused);
  if (triggerBtn && activeSpeakingButton === triggerBtn && isSpeaking) {
    stopSpeech();
    return;
  }

  // Cancel any prior speech
  stopSpeech();

  // Strip Markdown, URLs, and asterisks for smooth human speech
  const cleanText = text
    .replace(/https?:\/\/\S+/gi, '')
    .replace(/[*_#`~[\]()]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  if (!cleanText) return;

  // Detect script / language of the cleanText
  const hasTeluguScript = /[\u0C00-\u0C7F]/.test(cleanText);
  const hasHindiScript = /[\u0900-\u097F]/.test(cleanText);

  let targetLang = 'en-IN';
  if (hasTeluguScript || (AppState.currentLang === 'te' && !hasHindiScript) || AppState.voiceLang === 'te-IN') {
    targetLang = 'te-IN';
  } else if (hasHindiScript || (AppState.currentLang === 'hi' && !hasTeluguScript) || AppState.voiceLang === 'hi-IN') {
    targetLang = 'hi-IN';
  }

  // Ensure fresh voices list if cached was empty
  if (!cachedVoices || cachedVoices.length === 0) {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      cachedVoices = window.speechSynthesis.getVoices() || [];
    }
  }

  const selectedVoice = getBestVoiceForLang(targetLang);

  // If local voice is missing for Telugu or Hindi, use neural streaming fallback
  // Strictly avoids using English voices to mangle Indic text!
  if ((targetLang === 'te-IN' || targetLang === 'hi-IN') && !selectedVoice) {
    playStreamingTTS(cleanText, targetLang, triggerBtn);
    return;
  }

  if (!('speechSynthesis' in window)) {
    console.warn('SpeechSynthesis is not supported by this browser.');
    playStreamingTTS(cleanText, targetLang, triggerBtn);
    return;
  }

  // Chromium deadlock guard: if paused, resume
  if (window.speechSynthesis.paused) {
    try {
      window.speechSynthesis.resume();
    } catch(e) {}
  }

  const utterance = new SpeechSynthesisUtterance(cleanText);
  // Store globally to prevent Chromium Garbage Collection bug cutting off mid-speech
  window._activeUtterance = utterance;

  if (selectedVoice) {
    utterance.voice = selectedVoice;
    utterance.lang = selectedVoice.lang || targetLang;
  } else {
    utterance.lang = targetLang;
  }

  utterance.rate = 1.0;
  utterance.pitch = 1.0;

  const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;

  // Visual State Handlers
  utterance.onstart = () => {
    const stopBtn = document.getElementById('stop-speech-btn');
    if (stopBtn) stopBtn.style.display = 'inline-flex';

    if (triggerBtn) {
      activeSpeakingButton = triggerBtn;
      triggerBtn.classList.add('is-speaking');
      const label = triggerBtn.querySelector('.listen-label');
      const icon = triggerBtn.querySelector('.listen-icon');
      if (label) label.textContent = dict.btn_speaking || 'Speaking...';
      if (icon) icon.textContent = '⏹';
    }

    // Keep-alive heartbeat: Chromium cuts off utterances longer than ~15 seconds without a heartbeat
    if (speechHeartbeatTimer) clearInterval(speechHeartbeatTimer);
    speechHeartbeatTimer = setInterval(() => {
      if (window.speechSynthesis && window.speechSynthesis.speaking) {
        window.speechSynthesis.pause();
        window.speechSynthesis.resume();
      } else {
        clearInterval(speechHeartbeatTimer);
        speechHeartbeatTimer = null;
      }
    }, 10000);
  };

  utterance.onend = () => {
    stopSpeech();
  };

  utterance.onerror = (e) => {
    console.warn('SpeechSynthesis utterance event error:', e);
    stopSpeech();
  };

  try {
    window.speechSynthesis.speak(utterance);
  } catch (err) {
    console.error('Error starting speech synthesis:', err);
    stopSpeech();
  }
}

// Expose globally so external scripts or event listeners can call speakText
window.speakText = speakText;
window.stopSpeech = stopSpeech;


function clearChatThread() {
  const chatThread = document.getElementById('assistant-chat-thread');
  if (!chatThread) return;
  const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
  chatThread.innerHTML = `
    <div class="chat-msg ai-msg" id="assistant-welcome-msg">
      <div class="chat-avatar" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="22"></line></svg>
      </div>
      <div class="chat-bubble ai-bubble">
        <div class="chat-sender-name">Mitra AI</div>
        <div class="chat-text" id="welcome-chat-text" data-i18n="assistant_welcome_text">
          ${dict.assistant_welcome_text || 'Hello! I am Mitra, your citizen benefit assistant. Tell me about your profession, family income, state, or financial need in Telugu, Hindi, or English. You can speak using the microphone or type below.'}
        </div>
        <div class="chat-msg-actions">
          <button type="button" class="btn-chat-action btn-listen-msg" title="Listen aloud">
            <span class="listen-icon">🔊</span> <span class="listen-label" data-i18n="btn_listen">${dict.btn_listen || 'Listen'}</span>
          </button>
        </div>
      </div>
    </div>
    <div class="chat-msg ai-msg typing-msg" id="assistant-typing-indicator" style="display:none;" aria-hidden="true">
      <div class="chat-avatar" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline></svg>
      </div>
      <div class="chat-bubble ai-bubble typing-bubble">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-text" data-i18n="agent_processing">${dict.agent_processing || 'Analyzing eligibility rules...'}</span>
      </div>
    </div>
  `;
  const respArea = document.getElementById('assistant-response-area');
  if (respArea) respArea.style.display = 'none';
  showToast(dict.btn_clear_chat || 'Chat history cleared', 'info');
}

function initVoiceAssistant() {
  const micBtn = document.getElementById('mic-btn');
  const voiceActionBtn = document.getElementById('voice-action-btn');
  const voiceBtnLabel = document.getElementById('voice-btn-label');
  const micInstruction = document.getElementById('mic-instruction');
  const micContainer = document.querySelector('.mic-button-container');
  const waveBars = document.getElementById('audio-wave-bars');
  const agentStatusText = document.getElementById('agent-status-text');
  const assistantForm = document.getElementById('assistant-form');
  const textInput = document.getElementById('assistant-text-input');
  const clearInputBtn = document.getElementById('clear-input-btn');
  const ttsToggleBtn = document.getElementById('tts-toggle-btn');
  const ttsLabel = document.getElementById('tts-label');
  const speakResponseBtn = document.getElementById('speak-response-btn');
  const applyWizardBtn = document.getElementById('apply-to-wizard-btn');
  const liveBadge = document.getElementById('live-transcript-badge');
  const liveText = document.getElementById('live-transcript-text');
  const stopSpeechBtn = document.getElementById('stop-speech-btn');
  const clearChatBtn = document.getElementById('clear-chat-btn');

  // Speech Recognition Setup
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recognition = null;
  let sessionBaseText = '';
  let sessionFinalTranscript = '';
  let hasPermissionDenied = false;
  let isTransitioning = false;

  // Visual & State Updater
  function updateVoiceUI(isListening) {
    AppState.isListening = isListening;
    const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;

    if (isListening) {
      if (micContainer) micContainer.classList.add('listening');
      if (waveBars) waveBars.classList.add('active');
      if (micBtn) {
        micBtn.setAttribute('aria-label', 'Stop voice input');
        micBtn.setAttribute('title', 'Click to stop listening');
      }
      if (voiceActionBtn) {
        voiceActionBtn.classList.add('is-listening');
        voiceActionBtn.setAttribute('aria-label', 'Stop Listening');
      }
      if (voiceBtnLabel) {
        voiceBtnLabel.textContent = dict.btn_stop_listening || 'Stop Listening';
      }
      if (micInstruction) {
        micInstruction.textContent = dict.mic_active_instruction || 'Listening... Speak continuously with natural pauses. Click Stop when finished.';
      }
      const langNames = { 'te-IN': 'తెలుగు (Telugu)', 'hi-IN': 'हिंदी (Hindi)', 'en-IN': 'English' };
      const currentLangCode = recognition ? recognition.lang : 'en-IN';
      const displayLang = langNames[currentLangCode] || currentLangCode;
      if (agentStatusText) {
        agentStatusText.textContent = `${dict.agent_listening || 'Listening to your voice...'} (${displayLang})`;
      }
    } else {
      if (micContainer) micContainer.classList.remove('listening');
      if (waveBars) waveBars.classList.remove('active');
      if (liveBadge) liveBadge.style.display = 'none';
      if (micBtn) {
        micBtn.setAttribute('aria-label', 'Start voice input');
        micBtn.setAttribute('title', 'Click to speak');
      }
      if (voiceActionBtn) {
        voiceActionBtn.classList.remove('is-listening');
        voiceActionBtn.setAttribute('aria-label', 'Start Listening');
      }
      if (voiceBtnLabel) {
        voiceBtnLabel.textContent = dict.btn_start_listening || 'Start Listening';
      }
      if (agentStatusText) {
        agentStatusText.textContent = dict.agent_ready || 'Ready • Browser Speech Enabled';
      }
    }
  }

  if (SpeechRec) {
    recognition = new SpeechRec();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 3;
    AppState.speechRecognition = recognition;

    recognition.onstart = () => {
      isTransitioning = false;
      updateVoiceUI(true);
      const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
      showToast(dict.agent_listening || 'Listening to your voice...', 'info');
    };

    recognition.onresult = (event) => {
      let currentFinal = '';
      let currentInterim = '';

      for (let i = 0; i < event.results.length; ++i) {
        const item = event.results[i];
        const piece = item[0] ? item[0].transcript : '';
        if (item.isFinal) {
          currentFinal += (currentFinal ? ' ' : '') + piece.trim();
        } else {
          currentInterim += (currentInterim ? ' ' : '') + piece.trim();
        }
      }

      sessionFinalTranscript = currentFinal;

      // Real-time live dictation pill display
      if (liveBadge && liveText) {
        liveBadge.style.display = 'inline-flex';
        liveText.textContent = currentInterim || currentFinal || 'Listening...';
      }

      // Preserve previously typed/spoken base text, and append active session final + interim
      const parts = [];
      if (sessionBaseText) parts.push(sessionBaseText);
      if (currentFinal) parts.push(currentFinal);
      if (currentInterim) parts.push(currentInterim);

      const liveTranscript = parts.join(' ').replace(/\s+/g, ' ').trim();

      if (textInput) {
        textInput.value = liveTranscript;
      }
      if (clearInputBtn) {
        clearInputBtn.style.display = liveTranscript.length > 0 ? 'block' : 'none';
      }
    };

    recognition.onerror = (event) => {
      console.warn("Speech Recognition Error:", event.error);
      isTransitioning = false;
      updateVoiceUI(false);
      if (liveBadge) liveBadge.style.display = 'none';

      const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
      let errMsg = "Speech recognition error: " + event.error;

      if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
        hasPermissionDenied = true;
        errMsg = dict.mic_err_not_allowed || "Microphone permission blocked. Please allow mic access in your browser settings.";
      } else if (event.error === 'no-speech') {
        errMsg = dict.mic_err_no_speech || "No speech detected. Please check your mic and try speaking again.";
      } else if (event.error === 'network') {
        errMsg = dict.mic_err_network || "Network error communicating with speech recognition service. Please check your internet connection.";
      } else if (event.error === 'audio-capture') {
        errMsg = "No microphone hardware detected. Please ensure your microphone is connected and enabled.";
      } else if (event.error === 'language-not-supported') {
        const currentLangCode = recognition.lang || 'en-IN';
        errMsg = `Speech recognition for ${currentLangCode} is not supported in this browser.`;
      } else if (event.error === 'aborted') {
        return;
      }

      showToast(errMsg, 'error');
    };

    recognition.onend = () => {
      isTransitioning = false;
      updateVoiceUI(false);
      if (liveBadge) liveBadge.style.display = 'none';

      // Consolidate final text cleanly
      const finalParts = [];
      if (sessionBaseText) finalParts.push(sessionBaseText);
      if (sessionFinalTranscript) finalParts.push(sessionFinalTranscript);
      const settledText = finalParts.join(' ').replace(/\s+/g, ' ').trim();

      if (textInput && settledText) {
        textInput.value = settledText;
      }

      // Provide clear guidance that transcript is ready to edit or submit
      if (textInput && textInput.value.trim().length > 0) {
        const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
        if (micInstruction) {
          micInstruction.textContent = dict.mic_paused_instruction || 'Listening stopped. You can edit your text above or click Ask Assistant.';
        }
      } else {
        const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
        if (micInstruction) {
          micInstruction.textContent = dict.mic_prompt || 'Click the microphone and speak your situation, or pick an example prompt below.';
        }
      }
    };
  } else {
    if (agentStatusText) {
      agentStatusText.textContent = "Text Assistant Active (Voice recognition not supported in this browser)";
    }
  }

  // Toggle listening logic
  function toggleVoiceRecognition() {
    if (!recognition) {
      const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
      showToast(dict.mic_err_unsupported || "Speech recognition is not supported in this browser. Please use text search below.", 'info');
      if (textInput) textInput.focus();
      return;
    }

    if (hasPermissionDenied) {
      const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
      showToast(dict.mic_err_not_allowed || "Microphone permission was denied. Please allow microphone access in your browser settings.", 'error');
      return;
    }

    if (isTransitioning) return;

    if (AppState.isListening) {
      isTransitioning = true;
      try {
        recognition.stop();
      } catch (err) {
        console.warn("Error stopping recognition:", err);
        updateVoiceUI(false);
        isTransitioning = false;
      }
    } else {
      // Dynamic language resolution
      const activeLangBtn = document.querySelector('.btn-toggle.active');
      let langCode = activeLangBtn ? activeLangBtn.getAttribute('data-voice-lang') : null;
      if (!langCode) {
        const langMap = { en: 'en-IN', te: 'te-IN', hi: 'hi-IN' };
        langCode = langMap[AppState.currentLang] || 'en-IN';
      }

      recognition.lang = langCode;

      // Preserve whatever text is currently inside text input as base
      sessionBaseText = textInput ? textInput.value.trim() : '';
      sessionFinalTranscript = '';

      isTransitioning = true;
      try {
        recognition.start();
      } catch (err) {
        console.warn("Could not start recognition:", err);
        isTransitioning = false;
        try {
          recognition.stop();
        } catch(e) {}
      }
    }
  }

  // Bind click handlers to both micBtn and voiceActionBtn
  if (micBtn) {
    micBtn.addEventListener('click', toggleVoiceRecognition);
  }
  if (voiceActionBtn) {
    voiceActionBtn.addEventListener('click', toggleVoiceRecognition);
  }

  // Voice Language Switcher Buttons
  document.querySelectorAll('.btn-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.btn-toggle').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const voiceLang = btn.getAttribute('data-voice-lang');

      // Stop current active session cleanly before switching
      if (AppState.isListening && recognition) {
        try {
          recognition.stop();
        } catch(e) {}
      }

      if (voiceLang.startsWith('te')) setLanguage('te');
      else if (voiceLang.startsWith('hi')) setLanguage('hi');
      else setLanguage('en');
    });
  });

  // TTS Toggle
  if (ttsToggleBtn) {
    ttsToggleBtn.addEventListener('click', () => {
      AppState.ttsEnabled = !AppState.ttsEnabled;
      ttsToggleBtn.setAttribute('aria-pressed', AppState.ttsEnabled ? 'true' : 'false');
      const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
      if (ttsLabel) ttsLabel.textContent = AppState.ttsEnabled ? dict.tts_on : dict.tts_off;
      if (!AppState.ttsEnabled) {
        stopSpeech();
      }
    });
  }

  // Stop Speech Button
  if (stopSpeechBtn) {
    stopSpeechBtn.addEventListener('click', stopSpeech);
  }

  // Clear Chat Button
  if (clearChatBtn) {
    clearChatBtn.addEventListener('click', async () => {
      stopSpeech();
      const oldSessionId = AppState.chatSessionId;
      AppState.chatSessionId = 'session_' + Date.now();
      AppState.conversationProfile = {};
      lastParsedProfile = null;
      if (oldSessionId && API_CLIENT && API_CLIENT.clearAssistant) {
        API_CLIENT.clearAssistant(oldSessionId);
      }
      clearChatThread();
    });
  }

  // Delegated click handler for Listen buttons inside the assistant chat thread
  const chatThread = document.getElementById('assistant-chat-thread');
  if (chatThread) {
    chatThread.addEventListener('click', (e) => {
      const listenBtn = e.target.closest('.btn-listen-msg');
      if (!listenBtn) return;
      const bubble = listenBtn.closest('.chat-bubble');
      if (!bubble) return;
      const textEl = bubble.querySelector('.chat-text');
      if (!textEl) return;
      const textToSpeak = textEl.textContent || textEl.innerText;
      speakText(textToSpeak, listenBtn);
    });
  }

  // Text input clear button
  if (textInput && clearInputBtn) {
    textInput.addEventListener('input', () => {
      clearInputBtn.style.display = textInput.value.length > 0 ? 'block' : 'none';
    });
    clearInputBtn.addEventListener('click', () => {
      textInput.value = '';
      clearInputBtn.style.display = 'none';
      textInput.focus();
    });
  }

  // Assistant Form Submit
  if (assistantForm) {
    assistantForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const query = textInput.value.trim();
      if (!query) return;
      processAssistantQuery(query);
    });
  }

  // Clickable Suggestion Chips
  document.querySelectorAll('.chip-btn').forEach(chip => {
    chip.addEventListener('click', () => {
      const query = chip.getAttribute('data-query');
      if (textInput) textInput.value = query;
      if (clearInputBtn) clearInputBtn.style.display = 'block';
      processAssistantQuery(query);
    });
  });

  // Replay voice button
  if (speakResponseBtn) {
    speakResponseBtn.addEventListener('click', () => {
      const respText = document.getElementById('response-text-content');
      if (respText) speakText(respText.textContent, speakResponseBtn);
    });
  }

  // Auto-fill wizard button
  if (applyWizardBtn) {
    applyWizardBtn.addEventListener('click', () => {
      applyExtractedIntentToWizard();
    });
  }
}

/**
 * Natural Language Query Parser & Conversational Intent Matcher
 */
let lastParsedProfile = null;

async function processAssistantQuery(query) {
  const q = query.toLowerCase();
  const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
  
  // 1. Append User Message Bubble to Conversational Chat Thread
  const chatThread = document.getElementById('assistant-chat-thread');
  const typingIndicator = document.getElementById('assistant-typing-indicator');

  if (chatThread) {
    const userBubbleHtml = `
      <div class="chat-msg user-msg animate-fade-in-up">
        <div class="chat-avatar user-avatar" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        </div>
        <div class="chat-bubble user-bubble">
          <div class="chat-sender-name">${dict.chat_user_you || 'You'}</div>
          <div class="chat-text">${escapeHtml(query)}</div>
        </div>
      </div>
    `;
    if (typingIndicator) {
      typingIndicator.insertAdjacentHTML('beforebegin', userBubbleHtml);
      typingIndicator.style.display = 'flex';
    } else {
      chatThread.insertAdjacentHTML('beforeend', userBubbleHtml);
    }
    chatThread.scrollTop = chatThread.scrollHeight;
  }

  // Clear text input field
  const textInput = document.getElementById('assistant-text-input');
  const clearInputBtn = document.getElementById('clear-input-btn');
  if (textInput) textInput.value = '';
  if (clearInputBtn) clearInputBtn.style.display = 'none';

  // Ensure multi-turn conversation session ID & profile
  if (!AppState.chatSessionId) {
    AppState.chatSessionId = 'session_' + Date.now();
  }
  if (!AppState.conversationProfile) {
    AppState.conversationProfile = {};
  }

  let responseText = "";
  let matchedRecords = [];
  let requiresSchemes = false;
  let followUpQuestion = null;

  // 2. Query Conversation Intelligence Backend
  const assistantPayload = {
    message: query,
    session_id: AppState.chatSessionId,
    current_profile: AppState.conversationProfile,
    language: AppState.currentLang
  };

  const apiRes = await API_CLIENT.chatAssistant(assistantPayload);

  if (apiRes && apiRes.status === 'success') {
    responseText = apiRes.message || "";
    followUpQuestion = apiRes.follow_up_question || null;
    requiresSchemes = apiRes.requires_schemes_display === true;
    AppState.conversationProfile = apiRes.updated_profile || AppState.conversationProfile;
    lastParsedProfile = AppState.conversationProfile;

    if (requiresSchemes && Array.isArray(apiRes.schemes) && apiRes.schemes.length > 0) {
      matchedRecords = apiRes.schemes;
      matchedRecords.forEach(s => {
        if (AppState.latestSearchResultsMap) {
          AppState.latestSearchResultsMap.set(s.id, s);
        }
      });
    }
  } else {
    // Client-side Fallback Engine if backend offline
    const isGreeting = /^(hi|hello|hey|namaste|namaskaram|నమస్కారం|నమస్తే|नमस्ते|హలో)\b/i.test(q);
    const isGeneral = /how are you|who are you|what can you do|ఎలా ఉన్నారు|आप कैसे हैं|capital of|weather|bake/i.test(q);
    const lang = AppState.currentLang;

    if (isGreeting) {
      requiresSchemes = false;
      if (lang === 'te') {
        responseText = "నమస్కారం! నేను మిత్ర, మీ ప్రభుత్వ సంక్షేమ సహాయకుడిని. మీకు సరిపోయే పథకాలను గుర్తించడంలో సహాయపడతాను. మీరు మీ రాష్ట్రం, వృత్తి లేదా అవసరాన్ని చెప్పండి.";
      } else if (lang === 'hi') {
        responseText = "नमस्ते! मैं मित्रा, आपका सरकारी योजना सहायक हूँ। आप अपना राज्य, व्यवसाय या आवश्यकता बता सकते हैं।";
      } else {
        responseText = "Hello! I am Mitra, your citizen benefit assistant. Tell me about your profession, family income, state, or financial need in Telugu, Hindi, or English.";
      }
    } else if (isGeneral) {
      requiresSchemes = false;
      if (lang === 'te') {
        responseText = "నేను చాలా బాగున్నాను, ధన్యవాదాలు! భారత ప్రభుత్వ మరియు రాష్ట్ర సంక్షేమ పథకాల గురించి మీ సందేహాలను నివృత్తి చేయడానికి సిద్ధంగా ఉన్నాను. మీకు ఎలా సహాయపడగలను?";
      } else if (lang === 'hi') {
        responseText = "मैं बिल्कुल ठीक हूँ, धन्यवाद! मैं भारत की सरकारी और राज्य कल्याणकारी योजनाओं को खोजने में आपकी मदद के लिए तैयार हूँ।";
      } else {
        responseText = "I am doing well, thank you! I specialize in helping citizens discover verified Indian central and state welfare programs, scholarships, and pensions.";
      }
    } else {
      // Check for occupation or category
      let occ = null;
      if (/farmer|రైతు|किसान|cultivator/i.test(q)) occ = 'farmer';
      else if (/student|scholarship|విద్యార్థి|छात्र|college/i.test(q)) occ = 'student';
      else if (/vendor|hawker|స్ట్రీట్|दुकान/i.test(q)) occ = 'vendor';
      else if (/pension|senior|వృద్ధు|बुजुर्ग/i.test(q)) occ = 'senior';

      if (occ && !AppState.conversationProfile.state) {
        requiresSchemes = false;
        if (lang === 'te') {
          responseText = "మీ అవసరాలకు సరైన పథకాన్ని గుర్తించడానికి మరికొంత సమాచారం అవసరం: మీరు ఏ రాష్ట్రంలో నివసిస్తున్నారు?";
        } else if (lang === 'hi') {
          responseText = "आपकी आवश्यकता के अनुसार सटीक योजना खोजने के लिए कुछ और जानकारी आवश्यक है: आप किस राज्य में रहते हैं?";
        } else {
          responseText = "To accurately identify eligible programs for you, I need a few additional details: Which State or Union Territory do you reside in?";
        }
      } else {
        // Filter SCHEMES_DATA deterministically
        const matched = SCHEMES_DATA.filter(s => {
          if (occ && !s.criteria.occupations.includes('all') && !s.criteria.occupations.includes(occ)) return false;
          return true;
        });
        if (matched.length > 0) {
          requiresSchemes = true;
          matchedRecords = matched.slice(0, 4);
          if (lang === 'te') {
            responseText = `మీ ప్రొఫైల్ వివరాలతో సరిపోలే ${matchedRecords.length} సంక్షేమ పథకాలను గుర్తించాము:`;
          } else if (lang === 'hi') {
            responseText = `आपकी स्थिति के अनुकूल ${matchedRecords.length} प्रामाणिक योजनाएं पाई गई हैं:`;
          } else {
            responseText = `Found ${matchedRecords.length} verified welfare programs matching your profile:`;
          }
        } else {
          requiresSchemes = true;
          if (lang === 'te') {
            responseText = "ప్రస్తుత సమాచారంతో సరిపోలే ప్రభుత్వ పథకాలు ఏవీ లభించలేదు. మీ రాష్ట్రం, వయస్సు లేదా ఆదాయ పరిమితులను సవరించి మళ్ళీ ప్రయత్నించండి.";
          } else if (lang === 'hi') {
            responseText = "वर्तमान जानकारी के साथ कोई प्रासंगिक योजना नहीं मिली। कृपया अपने राज्य, आयु या आय सीमा में बदलाव करके पुनः प्रयास करें।";
          } else {
            responseText = "No relevant schemes were found with the current information. Try relaxing search criteria or checking central pan-India options.";
          }
        }
      }
    }
  }

  // 3. Render AI Response Bubble in Thread
  if (typingIndicator) typingIndicator.style.display = 'none';

  // Matched scheme chips inside AI bubble ONLY when schemes display is required and schemes exist
  let matchedPillsHtml = '';
  if (requiresSchemes && matchedRecords.length > 0) {
    matchedPillsHtml = matchedRecords.map(s => {
      const acronym = s.acronym || (s.title.length > 28 ? s.title.slice(0, 26) + '...' : s.title);
      const statusLabel = s.eligibility_status || (s.matchScore ? `${s.matchScore}% Match` : 'Potential Match');
      return `<button type="button" class="chat-scheme-pill" onclick="openEligibilityModal('${s.id}')" title="${escapeHtml(s.title)}">
        <span class="pill-title">${escapeHtml(acronym)}</span>
        <span class="pill-meta"> • ${escapeHtml(statusLabel)}</span>
      </button>`;
    }).join('');
  }

  const aiBubbleHtml = `
    <div class="chat-msg ai-msg animate-fade-in-up">
      <div class="chat-avatar" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="22"></line></svg>
      </div>
      <div class="chat-bubble ai-bubble">
        <div class="chat-sender-name">Mitra AI</div>
        <div class="chat-text">${escapeHtml(responseText)}</div>
        ${matchedPillsHtml ? `<div class="chat-pills-row">${matchedPillsHtml}</div>` : ''}
        <div class="chat-msg-actions">
          <button type="button" class="btn-chat-action btn-listen-msg" title="Listen aloud">
            <span class="listen-icon">🔊</span> <span class="listen-label">${dict.btn_listen || 'Listen'}</span>
          </button>
          ${(AppState.conversationProfile && (AppState.conversationProfile.occupation || AppState.conversationProfile.state)) ? `
          <button type="button" class="btn-chat-action highlight" onclick="applyExtractedIntentToWizard()" title="Auto-fill Wizard">
            ⚡ ${dict.btn_sync_profile || 'Auto-fill Eligibility Wizard'}
          </button>` : ''}
        </div>
      </div>
    </div>
  `;

  if (chatThread) {
    if (typingIndicator) {
      typingIndicator.insertAdjacentHTML('beforebegin', aiBubbleHtml);
    } else {
      chatThread.insertAdjacentHTML('beforeend', aiBubbleHtml);
    }
    chatThread.scrollTop = chatThread.scrollHeight;
  }

  // Populate legacy response area for backward compatibility
  const respArea = document.getElementById('assistant-response-area');
  const respBody = document.getElementById('response-text-content');
  const respPills = document.getElementById('response-matched-pills');

  if (respArea && respBody && respPills) {
    respBody.textContent = responseText;
    if (requiresSchemes && matchedRecords.length > 0) {
      respPills.innerHTML = matchedRecords.map(s => {
        const acronym = s.acronym || s.title.slice(0, 24);
        return `<button type="button" class="badge badge-indigo" onclick="openEligibilityModal('${s.id}')">${escapeHtml(acronym)} — ${escapeHtml(s.benefit)}</button>`;
      }).join('');
    } else {
      respPills.innerHTML = '';
    }
  }

  // Speak aloud if TTS enabled (passing null ensures it respects AppState.ttsEnabled)
  if (AppState.ttsEnabled) {
    speakText(responseText, null);
  }

  // Synchronize state filter to catalog ONLY if schemes are being displayed and state is known
  if (requiresSchemes && AppState.conversationProfile && AppState.conversationProfile.state) {
    const stateFilterEl = document.getElementById('filter-state');
    if (stateFilterEl) stateFilterEl.value = AppState.conversationProfile.state;
    AppState.stateFilter = AppState.conversationProfile.state;
    AppState.currentPage = 1;
    renderSchemes();
  }
}

/**
 * Sync extracted voice intent to the Multi-Step Wizard
 */
function applyExtractedIntentToWizard() {
  const profile = AppState.conversationProfile || lastParsedProfile;
  if (!profile) return;

  const ageInput = document.getElementById('user-age');
  const genderSelect = document.getElementById('user-gender');
  const stateSelect = document.getElementById('user-state');
  const occSelect = document.getElementById('user-occupation');
  const incomeSelect = document.getElementById('user-income');
  const girlChildCheck = document.getElementById('user-girl-child');
  const bplCheck = document.getElementById('user-bpl');

  if (profile.occupation && occSelect) {
    occSelect.value = profile.occupation;
  }
  if (profile.state && stateSelect) {
    stateSelect.value = profile.state;
  }
  if (profile.gender && genderSelect) {
    genderSelect.value = profile.gender;
  }
  if (profile.has_girl_child && girlChildCheck) {
    girlChildCheck.checked = true;
  }
  if (profile.has_bpl && bplCheck) {
    bplCheck.checked = true;
  }
  if (profile.age && ageInput) {
    ageInput.value = profile.age;
  }
  if (profile.income && incomeSelect) {
    if (profile.income <= 100000) incomeSelect.value = '100000';
    else if (profile.income <= 250000) incomeSelect.value = '250000';
    else if (profile.income <= 500000) incomeSelect.value = '500000';
    else if (profile.income <= 800000) incomeSelect.value = '800000';
    else incomeSelect.value = '1500000';
  }

  // Scroll smoothly to Wizard
  const wizardSec = document.getElementById('profile-wizard');
  if (wizardSec) {
    wizardSec.scrollIntoView({ behavior: 'smooth' });
    showToast("Profile auto-filled from assistant! Review steps 1 through 4.", 'info');
  }
}

/* ==========================================================================
   9. USER PROFILE MULTI-STEP WIZARD
   Demographics -> Occupation -> Special Inclusion -> Review & Rank
   ========================================================================== */
function initEligibilityWizard() {
  const wizardForm = document.getElementById('wizard-form');
  const executeMatchBtn = document.getElementById('execute-match-btn');

  // Next Step Buttons
  document.querySelectorAll('.next-step-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const nextStep = parseInt(btn.getAttribute('data-next'), 10);
      const currentStep = nextStep - 1;
      
      if (validateStep(currentStep)) {
        goToStep(nextStep);
      }
    });
  });

  // Previous Step Buttons
  document.querySelectorAll('.prev-step-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const prevStep = parseInt(btn.getAttribute('data-prev'), 10);
      goToStep(prevStep);
    });
  });

  // Step 4 "Discover Matching Benefits Now"
  if (executeMatchBtn) {
    executeMatchBtn.addEventListener('click', () => {
      saveWizardProfile();
      applyProfileToSchemes();
      
      const schemesSec = document.getElementById('schemes');
      if (schemesSec) {
        schemesSec.scrollIntoView({ behavior: 'smooth' });
      }
      showToast("Personalized matches calculated! Ranked by eligibility score.", 'info');
    });
  }

  // Clear profile filter button
  const clearProfileBtn = document.getElementById('clear-profile-filter-btn');
  if (clearProfileBtn) {
    clearProfileBtn.addEventListener('click', () => {
      AppState.userProfile.isComplete = false;
      const banner = document.getElementById('active-profile-banner');
      if (banner) banner.style.display = 'none';
      renderSchemes();
      showToast("Profile filter reset to broad catalog view.");
    });
  }
}

function validateStep(step) {
  let isValid = true;

  if (step === 1) {
    const age = document.getElementById('user-age');
    const ageError = document.getElementById('user-age-error');
    const gender = document.getElementById('user-gender');
    const genderError = document.getElementById('user-gender-error');
    const state = document.getElementById('user-state');
    const stateError = document.getElementById('user-state-error');

    // Age validation
    if (!age.value || parseInt(age.value, 10) < 5 || parseInt(age.value, 10) > 105) {
      age.classList.add('is-invalid');
      ageError.textContent = "Please enter a valid age between 5 and 100.";
      isValid = false;
    } else {
      age.classList.remove('is-invalid');
      ageError.textContent = "";
    }

    // Gender validation
    if (!gender.value) {
      gender.classList.add('is-invalid');
      genderError.textContent = "Please select your gender.";
      isValid = false;
    } else {
      gender.classList.remove('is-invalid');
      genderError.textContent = "";
    }

    // State validation
    if (!state.value) {
      state.classList.add('is-invalid');
      stateError.textContent = "Please select your State or Union Territory.";
      isValid = false;
    } else {
      state.classList.remove('is-invalid');
      stateError.textContent = "";
    }
  }

  if (step === 2) {
    const occ = document.getElementById('user-occupation');
    const occError = document.getElementById('user-occupation-error');
    const income = document.getElementById('user-income');
    const incomeError = document.getElementById('user-income-error');

    if (!occ.value) {
      occ.classList.add('is-invalid');
      occError.textContent = "Please select your primary occupation.";
      isValid = false;
    } else {
      occ.classList.remove('is-invalid');
      occError.textContent = "";
    }

    if (!income.value) {
      income.classList.add('is-invalid');
      incomeError.textContent = "Please select your annual household income range.";
      isValid = false;
    } else {
      income.classList.remove('is-invalid');
      incomeError.textContent = "";
    }
  }

  return isValid;
}

function goToStep(stepNum) {
  // Update step indicators
  for (let i = 1; i <= 4; i++) {
    const indicator = document.getElementById(`step-indicator-${i}`);
    const panel = document.getElementById(`wizard-step-${i}`);

    if (i < stepNum) {
      indicator.className = 'step-indicator completed';
    } else if (i === stepNum) {
      indicator.className = 'step-indicator active';
    } else {
      indicator.className = 'step-indicator';
    }

    panel.classList.toggle('active', i === stepNum);
  }

  // If entering step 4, refresh summary
  if (stepNum === 4) {
    populateStep4Summary();
  }
}

function populateStep4Summary() {
  const age = document.getElementById('user-age').value || '--';
  const gender = document.getElementById('user-gender').value || '--';
  const state = document.getElementById('user-state').value || 'Pan India';
  const occ = document.getElementById('user-occupation').value || '--';
  const incomeVal = document.getElementById('user-income').value || '0';
  const category = document.getElementById('user-category').value || 'General';
  const land = document.getElementById('user-land').value || 'none';
  const hasGirlChild = document.getElementById('user-girl-child').checked;
  const hasBpl = document.getElementById('user-bpl').checked;

  const revAgeGender = document.getElementById('rev-age-gender');
  const revState = document.getElementById('rev-state');
  const revOcc = document.getElementById('rev-occupation');
  const revIncome = document.getElementById('rev-income');
  const revCategory = document.getElementById('rev-category');
  const revSpecial = document.getElementById('rev-special');

  if (revAgeGender) revAgeGender.textContent = `${age} yrs • ${capitalize(gender)}`;
  if (revState) revState.textContent = state;
  if (revOcc) revOcc.textContent = capitalize(occ);
  
  const incomeMap = {
    '100000': 'Below ₹1,00,000 / year (BPL)',
    '250000': '₹1,00,000 to ₹2,50,000 / year',
    '500000': '₹2,50,000 to ₹5,00,000 / year',
    '800000': '₹5,00,000 to ₹8,00,000 / year (EWS)',
    '1500000': 'Above ₹8,00,000 / year'
  };
  if (revIncome) revIncome.textContent = incomeMap[incomeVal] || `Up to ₹${parseInt(incomeVal).toLocaleString('en-IN')}`;
  if (revCategory) revCategory.textContent = category;

  const specials = [];
  if (land !== 'none') specials.push(`${capitalize(land)} Landowner`);
  if (hasGirlChild) specials.push('Girl Child under 10');
  if (hasBpl) specials.push('BPL / Ration Card');
  if (specials.length === 0) specials.push('Standard Inclusions');

  if (revSpecial) revSpecial.textContent = specials.join(' • ');
}

function saveWizardProfile() {
  AppState.userProfile = {
    age: parseInt(document.getElementById('user-age').value, 10) || 30,
    gender: document.getElementById('user-gender').value || 'any',
    state: document.getElementById('user-state').value || 'all',
    occupation: document.getElementById('user-occupation').value || 'farmer',
    income: parseInt(document.getElementById('user-income').value, 10) || 250000,
    land: document.getElementById('user-land').value || 'none',
    category: document.getElementById('user-category').value || 'General',
    disability: document.getElementById('user-disability').value || 'no',
    girlChild: document.getElementById('user-girl-child').checked,
    bpl: document.getElementById('user-bpl').checked,
    isComplete: true
  };
}

function applyProfileToSchemes() {
  const banner = document.getElementById('active-profile-banner');
  const bannerText = document.getElementById('banner-profile-text');
  
  if (banner && bannerText) {
    const prof = AppState.userProfile;
    bannerText.textContent = `Matched for: ${capitalize(prof.occupation)}, Age ${prof.age}, ${prof.state === 'all' ? 'All States' : prof.state}`;
    banner.style.display = 'flex';
  }

  renderSchemes();
}

/* ==========================================================================
   10. SCHEME DISCOVERY & FILTERING ENGINE
   Dynamic Match Score Algorithm + Category Filtering + Instant Search
   ========================================================================== */
function initSchemesDiscovery() {
  const searchInput = document.getElementById('scheme-search-input');
  const clearSearchBtn = document.getElementById('clear-search-btn');
  const stateFilter = document.getElementById('filter-state');
  const levelFilter = document.getElementById('filter-level');
  const sortFilter = document.getElementById('filter-sort');
  const resetFiltersBtn = document.getElementById('reset-filters-btn');
  const prevBtn = document.getElementById('btn-prev-page');
  const nextBtn = document.getElementById('btn-next-page');

  // Search input debounced
  let searchTimeout;
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimeout);
      const val = searchInput.value.trim();
      if (clearSearchBtn) clearSearchBtn.style.display = val.length > 0 ? 'block' : 'none';

      searchTimeout = setTimeout(() => {
        AppState.searchQuery = val.toLowerCase();
        AppState.currentPage = 1;
        renderSchemes(true);
      }, 250);
    });
  }

  if (clearSearchBtn) {
    clearSearchBtn.addEventListener('click', () => {
      searchInput.value = '';
      clearSearchBtn.style.display = 'none';
      AppState.searchQuery = '';
      AppState.currentPage = 1;
      renderSchemes();
    });
  }

  // Category Tabs
  document.querySelectorAll('.category-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.category-tab').forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');

      AppState.activeCategory = tab.getAttribute('data-category');
      AppState.currentPage = 1;
      renderSchemes(true);
    });
  });

  // State dropdown
  if (stateFilter) {
    stateFilter.addEventListener('change', (e) => {
      AppState.stateFilter = e.target.value;
      AppState.currentPage = 1;
      renderSchemes(true);
    });
  }

  // Government Level dropdown
  if (levelFilter) {
    levelFilter.addEventListener('change', (e) => {
      AppState.levelFilter = e.target.value;
      AppState.currentPage = 1;
      renderSchemes(true);
    });
  }

  // Sort dropdown
  if (sortFilter) {
    sortFilter.addEventListener('change', (e) => {
      AppState.sortBy = e.target.value;
      AppState.currentPage = 1;
      renderSchemes();
    });
  }

  // Prev / Next page buttons
  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (AppState.currentPage > 1) {
        goToSchemesPage(AppState.currentPage - 1);
      }
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (AppState.currentPage < AppState.totalPages) {
        goToSchemesPage(AppState.currentPage + 1);
      }
    });
  }

  // Reset filters
  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener('click', () => {
      AppState.activeCategory = 'all';
      AppState.searchQuery = '';
      AppState.stateFilter = 'all';
      AppState.levelFilter = 'all';
      AppState.sortBy = 'relevance';
      AppState.currentPage = 1;

      if (searchInput) searchInput.value = '';
      if (clearSearchBtn) clearSearchBtn.style.display = 'none';
      if (stateFilter) stateFilter.value = 'all';
      if (levelFilter) levelFilter.value = 'all';
      if (sortFilter) sortFilter.value = 'relevance';

      document.querySelectorAll('.category-tab').forEach(t => {
        t.classList.toggle('active', t.getAttribute('data-category') === 'all');
      });

      renderSchemes();
    });
  }
}

/**
 * Calculate dynamic match score (0-100%) against User Profile
 */
function calculateMatchScore(scheme, profile) {
  if (!profile || !profile.isComplete) {
    // Default demonstration scores if wizard not completed yet
    const defaults = {
      'pm-kisan': 96,
      'ayushman-bharat': 94,
      'pm-mudra': 90,
      'vidya-lakshmi': 88,
      'pm-svanidhi': 86,
      'pmay-urban-gramin': 85,
      'nsp-scholarship': 84,
      'sukanya-samriddhi': 82,
      'standup-india': 80,
      'rythu-bharosa-bandhu': 95,
      'pm-matsya-sampada': 78,
      'atal-pension-yojana': 83
    };
    return defaults[scheme.id] || 80;
  }

  let score = 0;
  const c = scheme.criteria;

  // 1. Occupation Match (30 pts)
  if (c.occupations.includes('all') || c.occupations.includes(profile.occupation)) {
    score += 30;
  } else {
    score += 5; // Partial compatibility
  }

  // 2. Age Suitability (20 pts)
  if (profile.age >= c.minAge && profile.age <= c.maxAge) {
    score += 20;
  } else if (Math.abs(profile.age - c.minAge) <= 3 || Math.abs(profile.age - c.maxAge) <= 3) {
    score += 8;
  }

  // 3. Income Threshold (20 pts)
  if (profile.income <= c.incomeMax) {
    score += 20;
  } else if (profile.income <= c.incomeMax * 1.25) {
    score += 10;
  }

  // 4. State Applicability (15 pts)
  if (c.states.includes('all') || c.states.includes(profile.state)) {
    score += 15;
  } else {
    score += 0;
  }

  // 5. Special Criteria & Boosts (15 pts)
  if (c.requiresLand) {
    if (profile.land !== 'none') score += 15;
  } else if (c.requiresGirlChild) {
    if (profile.girlChild) score += 15;
  } else if (c.requiresBpl) {
    if (profile.bpl) score += 15;
  } else {
    score += 12; // Baseline criteria fulfillment
  }

  return Math.min(Math.max(score, 35), 99);
}

/* ==========================================================================
   BACKEND REST API INTEGRATION SERVICE
   Connects seamlessly to Python Flask /api endpoints with automatic local fallback
   ========================================================================== */
const API_CLIENT = {
  get baseUrl() {
    if (window.location.protocol.startsWith('http') && !window.location.port.includes('8080') && !window.location.port.includes('5500')) {
      return `${window.location.origin}/api`;
    }
    return 'http://127.0.0.1:5000/api';
  },

  async fetchWithTimeout(url, options = {}, timeoutMs = 3000) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      return await fetch(url, { ...options, signal: controller.signal });
    } finally {
      clearTimeout(timer);
    }
  },

  async getSchemes(params = {}) {
    try {
      const url = new URL(`${this.baseUrl}/schemes`);
      if (params.category && params.category !== 'all') url.searchParams.set('category', params.category);
      if (params.state && params.state !== 'all') url.searchParams.set('state', params.state);
      if (params.level && params.level !== 'all') url.searchParams.set('level', params.level);
      if (params.search) url.searchParams.set('search', params.search);
      if (params.sort) url.searchParams.set('sort', params.sort);
      if (params.page) url.searchParams.set('page', params.page);
      if (params.limit !== undefined) url.searchParams.set('limit', params.limit);

      const res = await this.fetchWithTimeout(url.toString(), {
        headers: { 'Accept': 'application/json' }
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      AppState.isBackendConnected = true;
      updateBackendStatusBadge(true);
      return json;
    } catch (e) {
      AppState.isBackendConnected = false;
      updateBackendStatusBadge(false);
      return null;
    }
  },

  async getStats() {
    try {
      const res = await this.fetchWithTimeout(`${this.baseUrl}/schemes/stats`, {
        headers: { 'Accept': 'application/json' }
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      return null;
    }
  },

  async searchSchemes(profilePayload) {
    try {
      const res = await this.fetchWithTimeout(`${this.baseUrl}/schemes/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(profilePayload)
      }, 4000);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      AppState.isBackendConnected = true;
      updateBackendStatusBadge(true);
      return json;
    } catch (e) {
      AppState.isBackendConnected = false;
      updateBackendStatusBadge(false);
      return null;
    }
  },

  async chatAssistant(payload) {
    try {
      // First try /api/assistant/chat
      let res = await this.fetchWithTimeout(`${this.baseUrl}/assistant/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      }, 12000);

      // Fallback to /api/schemes/assistant if not found
      if (!res.ok && res.status === 404) {
        res = await this.fetchWithTimeout(`${this.baseUrl}/schemes/assistant`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(payload)
        }, 12000);
      }

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      AppState.isBackendConnected = true;
      updateBackendStatusBadge(true);
      return json;
    } catch (e) {
      console.warn("API_CLIENT.chatAssistant error:", e);
      return null;
    }
  },

  async clearAssistant(sessionId) {
    try {
      await this.fetchWithTimeout(`${this.baseUrl}/assistant/clear`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
      }, 3000);
    } catch (e) {
      // Non-fatal
    }
  },

  async getAssistantStatus() {
    try {
      const res = await this.fetchWithTimeout(`${this.baseUrl}/assistant/status`, {
        headers: { 'Accept': 'application/json' }
      }, 3000);
      if (res.ok) return await res.json();
    } catch (e) {}
    return null;
  },

  async getSchemeById(id) {
    try {
      const res = await this.fetchWithTimeout(`${this.baseUrl}/schemes/${encodeURIComponent(id)}`, {
        headers: { 'Accept': 'application/json' }
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      AppState.isBackendConnected = true;
      return json.data || null;
    } catch (e) {
      return null;
    }
  }
};

function updateBackendStatusBadge(connected) {
  const noteEl = document.querySelector('.sample-data-tag');
  if (!noteEl) return;
  if (connected) {
    noteEl.textContent = 'REST API Connected • SQLite Database';
    noteEl.style.backgroundColor = '#ECFDF5';
    noteEl.style.color = '#065F46';
    noteEl.style.borderColor = '#A7F3D0';
  } else {
    const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
    noteEl.textContent = dict.sample_data_note || 'Verified Demonstration Records • Real Criteria';
    noteEl.style.backgroundColor = '#F1F5F9';
    noteEl.style.color = '#475569';
    noteEl.style.borderColor = '#CBD5E1';
  }
}

/* ==========================================================================
   PAGINATION CONTROLS
   ========================================================================== */
function renderPaginationControls() {
  const toolbar = document.getElementById('schemes-pagination-toolbar');
  const prevBtn = document.getElementById('btn-prev-page');
  const nextBtn = document.getElementById('btn-next-page');
  const pageNumbersGroup = document.getElementById('page-numbers-group');
  const rangeEl = document.getElementById('pagination-range');
  const totalEl = document.getElementById('pagination-total');

  if (!toolbar) return;

  const total = AppState.totalCount;
  const page = AppState.currentPage;
  const totalPages = AppState.totalPages || 1;

  if (total === 0 || totalPages <= 1) {
    toolbar.style.display = 'none';
    return;
  }

  toolbar.style.display = 'flex';

  const startIdx = (page - 1) * AppState.itemsPerPage + 1;
  const endIdx = Math.min(page * AppState.itemsPerPage, total);

  if (rangeEl) rangeEl.textContent = `${startIdx}-${endIdx}`;
  if (totalEl) totalEl.textContent = total;

  if (prevBtn) {
    prevBtn.disabled = page <= 1;
  }
  if (nextBtn) {
    nextBtn.disabled = page >= totalPages;
  }

  if (pageNumbersGroup) {
    let pagesHtml = '';
    for (let p = 1; p <= totalPages; p++) {
      if (p === 1 || p === totalPages || (p >= page - 1 && p <= page + 1)) {
        pagesHtml += `<button type="button" class="page-btn ${p === page ? 'active' : ''}" onclick="goToSchemesPage(${p})" aria-label="Go to page ${p}">${p}</button>`;
      } else if (p === page - 2 || p === page + 2) {
        pagesHtml += `<span class="page-ellipsis">...</span>`;
      }
    }
    pageNumbersGroup.innerHTML = pagesHtml;
  }
}

window.goToSchemesPage = function(pageNumber) {
  if (pageNumber < 1 || pageNumber > AppState.totalPages || pageNumber === AppState.currentPage) return;
  AppState.currentPage = pageNumber;
  renderSchemes(true);
  const schemesSec = document.getElementById('schemes');
  if (schemesSec) {
    schemesSec.scrollIntoView({ behavior: 'smooth' });
  }
};

/**
 * Filter & Render Scheme Cards into DOM
 * Connects to Python Flask backend when available, with automatic local fallback
 */
async function renderSchemes(showSkeleton = false) {
  const grid = document.getElementById('schemes-grid');
  const skeleton = document.getElementById('schemes-skeleton');
  const emptyState = document.getElementById('empty-state');
  const countEl = document.getElementById('results-count');
  if (!grid) return;

  if (showSkeleton && skeleton) {
    skeleton.style.display = 'grid';
    grid.style.display = 'none';
  }

  let filtered = null;
  const backendMap = new Map();

  // If user profile from wizard is complete, query POST /api/schemes/search
  if (AppState.userProfile && AppState.userProfile.isComplete) {
    const profilePayload = {
      age: AppState.userProfile.age,
      gender: AppState.userProfile.gender,
      state: AppState.userProfile.state,
      occupation: AppState.userProfile.occupation,
      income: AppState.userProfile.income,
      land: AppState.userProfile.land,
      category: AppState.userProfile.category,
      disability: AppState.userProfile.disability,
      girl_child: AppState.userProfile.girlChild,
      bpl: AppState.userProfile.bpl
    };

    const searchResponse = await API_CLIENT.searchSchemes(profilePayload);
    if (searchResponse && searchResponse.status === 'success' && Array.isArray(searchResponse.results)) {
      let results = searchResponse.results.map(item => {
        backendMap.set(item.id, item);
        return {
          ...item,
          matchScore: item.match_score || item.matchScore,
          matchLabel: item.match_label || 'High Potential Match',
          ruleBreakdown: item.rule_breakdown
        };
      });

      // Apply category/state/level/search filters on top
      if (AppState.activeCategory !== 'all') {
        results = results.filter(s => s.category === AppState.activeCategory);
      }
      if (AppState.stateFilter !== 'all') {
        results = results.filter(s => {
          const st = s.states || (s.criteria && s.criteria.states) || ['all'];
          return st.includes('all') || st.includes(AppState.stateFilter);
        });
      }
      if (AppState.levelFilter !== 'all') {
        results = results.filter(s => {
          const lvl = s.government_level || s.governmentLevel || '';
          return lvl.toLowerCase() === AppState.levelFilter.toLowerCase();
        });
      }
      if (AppState.searchQuery) {
        const q = AppState.searchQuery.toLowerCase();
        results = results.filter(s => {
          const txt = `${s.title} ${s.acronym || ''} ${s.department} ${s.benefit} ${s.description}`.toLowerCase();
          return txt.includes(q);
        });
      }
      if (AppState.sortBy === 'amount') {
        results.sort((a, b) => (b.benefit_value || b.benefitValue) - (a.benefit_value || a.benefitValue));
      } else if (AppState.sortBy === 'name') {
        results.sort((a, b) => a.title.localeCompare(b.title));
      }

      AppState.totalCount = results.length;
      AppState.totalPages = Math.max(1, Math.ceil(results.length / AppState.itemsPerPage));
      const start = (AppState.currentPage - 1) * AppState.itemsPerPage;
      filtered = results.slice(start, start + AppState.itemsPerPage);
    }
  } else {
    // Standard browsing: Call GET /api/schemes
    const apiRes = await API_CLIENT.getSchemes({
      category: AppState.activeCategory,
      state: AppState.stateFilter,
      level: AppState.levelFilter,
      search: AppState.searchQuery,
      sort: AppState.sortBy,
      page: AppState.currentPage,
      limit: AppState.itemsPerPage
    });

    if (apiRes && Array.isArray(apiRes.data)) {
      AppState.totalCount = apiRes.total_count !== undefined ? apiRes.total_count : apiRes.data.length;
      AppState.totalPages = apiRes.total_pages || 1;
      AppState.currentPage = apiRes.page || 1;

      filtered = apiRes.data.map(s => {
        backendMap.set(s.id, s);
        return {
          ...s,
          matchScore: calculateMatchScore(s, AppState.userProfile)
        };
      });
      if (AppState.sortBy === 'relevance') {
        filtered.sort((a, b) => b.matchScore - a.matchScore);
      }
    }
  }

  // Fallback to local client dataset if API is offline or returns empty
  if (!filtered) {
    let offlineAll = SCHEMES_DATA.filter(scheme => {
      if (AppState.activeCategory !== 'all' && scheme.category !== AppState.activeCategory) return false;
      if (AppState.stateFilter !== 'all') {
        const matchesState = scheme.criteria.states.includes('all') || scheme.criteria.states.includes(AppState.stateFilter);
        if (!matchesState) return false;
      }
      if (AppState.levelFilter !== 'all') {
        const lvl = scheme.government_level || scheme.scope || '';
        if (!lvl.toLowerCase().includes(AppState.levelFilter.toLowerCase())) return false;
      }
      if (AppState.searchQuery) {
        const query = AppState.searchQuery;
        const textToSearch = `${scheme.title} ${scheme.acronym || ''} ${scheme.department} ${scheme.benefit} ${scheme.description}`.toLowerCase();
        if (!textToSearch.includes(query)) return false;
      }
      return true;
    }).map(scheme => ({
      ...scheme,
      matchScore: calculateMatchScore(scheme, AppState.userProfile)
    }));

    if (AppState.sortBy === 'relevance') {
      offlineAll.sort((a, b) => b.matchScore - a.matchScore);
    } else if (AppState.sortBy === 'amount') {
      offlineAll.sort((a, b) => b.benefitValue - a.benefitValue);
    } else if (AppState.sortBy === 'name') {
      offlineAll.sort((a, b) => a.title.localeCompare(b.title));
    }

    AppState.totalCount = offlineAll.length;
    AppState.totalPages = Math.max(1, Math.ceil(offlineAll.length / AppState.itemsPerPage));
    const start = (AppState.currentPage - 1) * AppState.itemsPerPage;
    filtered = offlineAll.slice(start, start + AppState.itemsPerPage);
  }

  AppState.latestSearchResultsMap = backendMap;

  if (skeleton) skeleton.style.display = 'none';
  grid.style.display = 'grid';

  if (countEl) countEl.textContent = AppState.totalCount;

  // Empty State
  if (AppState.totalCount === 0 || filtered.length === 0) {
    grid.innerHTML = '';
    if (emptyState) emptyState.style.display = 'block';
    renderPaginationControls();
    return;
  }

  if (emptyState) emptyState.style.display = 'none';

  // Category SVG icons for visual recognition
  const categoryIcons = {
    agriculture: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>`,
    health: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>`,
    education: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>`,
    business: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`,
    women: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="5"/><path d="M12 13v8M9 18h6"/></svg>`,
    social: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`
  };

  const dict = TRANSLATIONS[AppState.currentLang] || TRANSLATIONS.en;
  const viewEligibilityText = dict.scheme_view_details || 'View Details & Eligibility';
  const officialPortalText = dict.official_portal_link || 'Official Portal ↗';
  const verifiedRecordText = dict.verified_record_tag || 'Verified Public Record';
  const docsTagLabel = dict.docs_count_tag || 'Documents';

  // Render Cards
  grid.innerHTML = filtered.map(scheme => {
    const isSaved = AppState.savedSchemeIds.has(scheme.id);
    const score = scheme.matchScore || calculateMatchScore(scheme, AppState.userProfile);
    const matchBadgeClass = score >= 85 ? 'high' : (score >= 65 ? 'medium' : 'low');
    const minAge = scheme.min_age !== undefined ? scheme.min_age : (scheme.criteria ? scheme.criteria.minAge : 18);
    const maxAge = scheme.max_age !== undefined ? scheme.max_age : (scheme.criteria ? scheme.criteria.maxAge : 70);
    const incMax = scheme.income_max !== undefined ? scheme.income_max : (scheme.criteria ? scheme.criteria.incomeMax : 500000);
    const officialUrl = scheme.official_url || scheme.officialUrl;
    const catIcon = categoryIcons[scheme.category] || categoryIcons.social;
    const docs = scheme.documents || [];
    const docCount = docs.length;
    const docPreview = docCount > 0 
      ? docs.slice(0, 2).map(d => d.split('(')[0].trim()).join(', ') + (docCount > 2 ? ` +${docCount - 2} more` : '')
      : 'Standard KYC';

    return `
      <article class="scheme-card" data-scheme-id="${scheme.id}">
        <div class="scheme-card-header">
          <div class="scheme-card-badges">
            <span class="badge-category cat-${scheme.category}">${catIcon} ${capitalize(scheme.category)}</span>
            <span class="badge-scope">${escapeHtml(scheme.scope)}</span>
            <span class="badge-verified" title="Official public record verified from government portal">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              <span>${verifiedRecordText}</span>
            </span>
          </div>
          <div class="scheme-card-top-actions">
            <span class="badge-match ${matchBadgeClass}">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
              <span>${score}% Match</span>
            </span>
            <button 
              type="button" 
              class="card-bookmark-btn ${isSaved ? 'saved' : ''}" 
              onclick="toggleBookmark('${scheme.id}')"
              aria-label="${isSaved ? 'Remove Bookmark' : 'Save Scheme'}"
              title="${isSaved ? 'Remove from Saved' : 'Save Scheme'}"
            >
              <svg width="17" height="17" viewBox="0 0 24 24" fill="${isSaved ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
              </svg>
            </button>
          </div>
        </div>

        <h3 class="scheme-title">${escapeHtml(scheme.title)}</h3>
        <div class="scheme-dept">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M3 10h18M5 6l7-3 7 3M4 10v11M20 10v11M8 14v4M12 14v4M16 14v4"/></svg>
          <span>${escapeHtml(scheme.department)}</span>
        </div>

        <p class="scheme-desc">${escapeHtml(scheme.description)}</p>

        <div class="scheme-benefit-highlight">
          <span class="benefit-label">Entitlement Benefit</span>
          <div class="benefit-value">${escapeHtml(scheme.benefit)}</div>
        </div>

        <div class="criteria-tags-row">
          <span class="criteria-tag">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
            Age: ${minAge} - ${maxAge} yrs
          </span>
          <span class="criteria-tag">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>
            Cap: ₹${(incMax / 100000).toFixed(1)}L
          </span>
        </div>

        <!-- Documents Readiness Pill -->
        <div class="scheme-docs-preview" title="${escapeHtml(docs.join(', '))}">
          <span class="docs-preview-label">📋 ${docsTagLabel} (${docCount}):</span>
          <span class="docs-preview-list">${escapeHtml(docPreview)}</span>
        </div>

        <div class="scheme-card-actions">
          <button type="button" class="btn btn-secondary btn-sm" onclick="openEligibilityModal('${scheme.id}')">
            <span>${viewEligibilityText}</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
          </button>
          <a href="${officialUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm btn-official-link" title="Open verified official government portal in new tab">
            <span>${officialPortalText}</span>
          </a>
        </div>
      </article>
    `;
  }).join('');

  renderPaginationControls();
}

function filterSchemesByMatchedIds(ids) {
  const schemesSec = document.getElementById('schemes');
  if (schemesSec) schemesSec.scrollIntoView({ behavior: 'smooth' });
}

/* ==========================================================================
   11. DETAILED ELIGIBILITY COMPARISON MODAL
   Side-by-side rule comparison + Document checklist + Official guidance
   ========================================================================== */
function initEligibilityModal() {
  const modal = document.getElementById('eligibility-modal');
  const closeBtn = document.getElementById('modal-close-btn');
  const cancelBtn = document.getElementById('modal-cancel-btn');
  const printBtn = document.getElementById('print-checklist-btn');

  const closeModal = () => {
    if (!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
  };

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  // Print Document Checklist
  if (printBtn) {
    printBtn.addEventListener('click', () => {
      window.print();
    });
  }
}

// Global modal trigger called from card HTML
window.openEligibilityModal = async function(schemeId) {
  let scheme = AppState.latestSearchResultsMap ? AppState.latestSearchResultsMap.get(schemeId) : null;
  if (!scheme) {
    scheme = SCHEMES_DATA.find(s => s.id === schemeId);
  }
  if (!scheme && API_CLIENT) {
    scheme = await API_CLIENT.getSchemeById(schemeId);
  }
  if (!scheme) return;

  // Normalize criteria sub-object if missing
  if (!scheme.criteria) {
    scheme.criteria = {
      minAge: scheme.min_age !== undefined ? scheme.min_age : 0,
      maxAge: scheme.max_age !== undefined ? scheme.max_age : 100,
      gender: scheme.gender || 'all',
      incomeMax: scheme.income_max !== undefined ? scheme.income_max : 10000000,
      occupations: scheme.occupations || [],
      states: scheme.states || ['all'],
      requiresLand: Boolean(scheme.requires_land),
      requiresGirlChild: Boolean(scheme.requires_girl_child),
      requiresBpl: Boolean(scheme.requires_bpl),
      summary: scheme.criteria_summary || ''
    };
  }
  if (!Array.isArray(scheme.documents)) {
    scheme.documents = [];
  }
  if (!Array.isArray(scheme.applicationSteps)) {
    scheme.applicationSteps = scheme.application_steps || [
      { step: "Visit Official Portal", text: `Apply directly at ${scheme.officialUrl || scheme.official_url || 'official government portal'}.` },
      { step: "Complete KYC & Verification", text: "Submit required identity documents and verify mobile via OTP." }
    ];
  }
  if (!scheme.officialUrl && scheme.official_url) scheme.officialUrl = scheme.official_url;

  const modal = document.getElementById('eligibility-modal');
  const title = document.getElementById('modal-scheme-title');
  const dept = document.getElementById('modal-scheme-dept');
  const benefitAmt = document.getElementById('modal-benefit-amt');
  const matchScoreEl = document.getElementById('modal-match-score');
  const scopeEl = document.getElementById('modal-scope');
  const descEl = document.getElementById('modal-scheme-desc');
  const tbody = document.getElementById('criteria-comparison-tbody');
  const missingWarn = document.getElementById('missing-info-warning');
  const docContainer = document.getElementById('doc-checklist-container');
  const docProgressTag = document.getElementById('doc-readiness-pct');
  const stepsList = document.getElementById('modal-app-steps');
  const officialLink = document.getElementById('modal-official-link');

  const prof = AppState.userProfile;
  const matchScore = calculateMatchScore(scheme, prof);

  if (title) title.textContent = scheme.title;
  if (dept) dept.textContent = scheme.department;
  if (benefitAmt) benefitAmt.textContent = scheme.benefit;
  if (matchScoreEl) matchScoreEl.textContent = `${matchScore}% Match Score`;
  if (scopeEl) scopeEl.textContent = scheme.scope;
  if (descEl) descEl.textContent = scheme.description;

  // 1. Populate Rule Comparison Matrix Table (from backend evaluation if present, otherwise local)
  const backendItem = AppState.latestSearchResultsMap ? AppState.latestSearchResultsMap.get(schemeId) : null;
  const rb = backendItem ? (backendItem.rule_breakdown || backendItem.ruleBreakdown) : null;

  if (rb && rb.age && rb.occupation && rb.income && rb.state) {
    const ageStatus = rb.age.status || 'neutral';
    const occStatus = rb.occupation.status || 'neutral';
    const incStatus = rb.income.status || 'neutral';
    const stateStatus = rb.state.status || 'neutral';

    tbody.innerHTML = `
      <tr>
        <td><strong>Age Criteria</strong></td>
        <td>${rb.age.requirement}</td>
        <td>${rb.age.user_value}</td>
        <td><span class="status-pill ${ageStatus}">${ageStatus === 'matched' ? '✓ Matched' : (ageStatus === 'unmet' ? '✗ Unmet' : '• Pending')}</span></td>
      </tr>
      <tr>
        <td><strong>Eligible Occupation</strong></td>
        <td>${rb.occupation.requirement}</td>
        <td>${rb.occupation.user_value}</td>
        <td><span class="status-pill ${occStatus}">${occStatus === 'matched' ? '✓ Matched' : (occStatus === 'unmet' ? '✗ Ineligible' : '• Pending')}</span></td>
      </tr>
      <tr>
        <td><strong>Family Income Cap</strong></td>
        <td>${rb.income.requirement}</td>
        <td>${rb.income.user_value}</td>
        <td><span class="status-pill ${incStatus}">${incStatus === 'matched' ? '✓ Within Limit' : (incStatus === 'unmet' ? '✗ Exceeds Cap' : '• Pending')}</span></td>
      </tr>
      <tr>
        <td><strong>State Domicile</strong></td>
        <td>${rb.state.requirement}</td>
        <td>${rb.state.user_value}</td>
        <td><span class="status-pill ${stateStatus}">${stateStatus === 'matched' ? '✓ Eligible' : (stateStatus === 'unmet' ? '✗ State Excluded' : '• Pending')}</span></td>
      </tr>
    `;
  } else {
    const userAge = prof.isComplete ? `${prof.age} years` : 'Not specified';
    const ageStatus = !prof.isComplete ? 'neutral' : (prof.age >= scheme.criteria.minAge && prof.age <= scheme.criteria.maxAge ? 'matched' : 'unmet');

    const userOcc = prof.isComplete ? capitalize(prof.occupation) : 'Not specified';
    const occStatus = !prof.isComplete ? 'neutral' : (scheme.criteria.occupations.includes('all') || scheme.criteria.occupations.includes(prof.occupation) ? 'matched' : 'unmet');

    const userIncome = prof.isComplete ? `₹${(prof.income).toLocaleString('en-IN')}` : 'Not specified';
    const incStatus = !prof.isComplete ? 'neutral' : (prof.income <= scheme.criteria.incomeMax ? 'matched' : 'unmet');

    const userState = prof.isComplete ? (prof.state === 'all' ? 'Any State' : prof.state) : 'Not specified';
    const stateStatus = !prof.isComplete ? 'neutral' : (scheme.criteria.states.includes('all') || scheme.criteria.states.includes(prof.state) ? 'matched' : 'unmet');

    tbody.innerHTML = `
      <tr>
        <td><strong>Age Criteria</strong></td>
        <td>${scheme.criteria.minAge} to ${scheme.criteria.maxAge} years</td>
        <td>${userAge}</td>
        <td><span class="status-pill ${ageStatus}">${ageStatus === 'matched' ? '✓ Matched' : (ageStatus === 'unmet' ? '✗ Unmet' : '• Pending')}</span></td>
      </tr>
      <tr>
        <td><strong>Eligible Occupation</strong></td>
        <td>${scheme.criteria.occupations.map(capitalize).join(', ')}</td>
        <td>${userOcc}</td>
        <td><span class="status-pill ${occStatus}">${occStatus === 'matched' ? '✓ Matched' : (occStatus === 'unmet' ? '✗ Ineligible' : '• Pending')}</span></td>
      </tr>
      <tr>
        <td><strong>Family Income Cap</strong></td>
        <td>Up to ₹${(scheme.criteria.incomeMax).toLocaleString('en-IN')} / year</td>
        <td>${userIncome}</td>
        <td><span class="status-pill ${incStatus}">${incStatus === 'matched' ? '✓ Within Limit' : (incStatus === 'unmet' ? '✗ Exceeds Cap' : '• Pending')}</span></td>
      </tr>
      <tr>
        <td><strong>State Domicile</strong></td>
        <td>${scheme.criteria.states.join(', ')}</td>
        <td>${userState}</td>
        <td><span class="status-pill ${stateStatus}">${stateStatus === 'matched' ? '✓ Eligible' : (stateStatus === 'unmet' ? '✗ State Excluded' : '• Pending')}</span></td>
      </tr>
    `;
  }

  if (missingWarn) {
    missingWarn.style.display = prof.isComplete ? 'none' : 'flex';
  }

  // 2. Populate Interactive Document Checklist
  let checkedCount = 0;
  const updateDocProgress = () => {
    const total = scheme.documents.length;
    const pct = Math.round((checkedCount / total) * 100);
    if (docProgressTag) {
      docProgressTag.textContent = `${checkedCount} / ${total} Ready (${pct}%)`;
    }
  };

  docContainer.innerHTML = scheme.documents.map((doc, idx) => `
    <label class="doc-check-item">
      <input type="checkbox" class="doc-cb" data-idx="${idx}">
      <span class="doc-title">${doc}</span>
    </label>
  `).join('');

  document.querySelectorAll('.doc-cb').forEach(cb => {
    cb.addEventListener('change', () => {
      checkedCount = document.querySelectorAll('.doc-cb:checked').length;
      updateDocProgress();
    });
  });
  updateDocProgress();

  // 3. Populate Application Steps
  stepsList.innerHTML = scheme.applicationSteps.map((s, idx) => `
    <div class="app-step-item">
      <div class="app-step-num">${idx + 1}</div>
      <div class="app-step-text">
        <strong>${s.step}</strong>
        <p>${s.text}</p>
      </div>
    </div>
  `).join('');

  // 4. Update Official Portal Link
  if (officialLink) {
    officialLink.href = scheme.officialUrl;
  }

  // Open Modal
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
};

/* ==========================================================================
   12. SAVED SCHEMES DRAWER & BOOKMARKS
   ========================================================================= */
function initSavedDrawer() {
  const savedBtn = document.getElementById('saved-schemes-btn');
  const drawer = document.getElementById('saved-drawer');
  const closeBtn = document.getElementById('close-saved-drawer');
  const clearAllBtn = document.getElementById('clear-all-saved-btn');

  const openDrawer = () => {
    renderSavedList();
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
  };

  const closeDrawer = () => {
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
  };

  if (savedBtn) savedBtn.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);

  if (drawer) {
    drawer.addEventListener('click', (e) => {
      if (e.target === drawer) closeDrawer();
    });
  }

  if (clearAllBtn) {
    clearAllBtn.addEventListener('click', () => {
      AppState.savedSchemeIds.clear();
      persistBookmarks();
      updateBookmarkBadge();
      renderSavedList();
      renderSchemes();
      showToast("Cleared all bookmarked schemes.");
    });
  }
}

window.toggleBookmark = function(schemeId) {
  if (AppState.savedSchemeIds.has(schemeId)) {
    AppState.savedSchemeIds.delete(schemeId);
    showToast("Scheme removed from saved list.");
  } else {
    AppState.savedSchemeIds.add(schemeId);
    showToast("Scheme saved to your bookmarks!", 'info');
  }

  persistBookmarks();
  updateBookmarkBadge();
  renderSchemes();
};

function persistBookmarks() {
  try {
    localStorage.setItem('scheme_finder_saved', JSON.stringify([...AppState.savedSchemeIds]));
  } catch(e) {}
}

function updateBookmarkBadge() {
  const badge = document.getElementById('bookmark-badge');
  if (badge) {
    badge.textContent = AppState.savedSchemeIds.size;
  }
}

function renderSavedList() {
  const container = document.getElementById('saved-schemes-list');
  if (!container) return;

  if (AppState.savedSchemeIds.size === 0) {
    container.innerHTML = `
      <div class="empty-results-state" style="padding: 30px 10px;">
        <p class="text-muted" style="margin-bottom:0;">You have not saved any schemes yet. Click the bookmark icon on any scheme card to save it here.</p>
      </div>
    `;
    return;
  }

  const savedList = [];
  AppState.savedSchemeIds.forEach(id => {
    let item = AppState.latestSearchResultsMap ? AppState.latestSearchResultsMap.get(id) : null;
    if (!item) item = SCHEMES_DATA.find(s => s.id === id);
    if (item) savedList.push(item);
  });
  container.innerHTML = savedList.map(scheme => `
    <div class="saved-item-card">
      <h4 class="saved-item-title">${scheme.title}</h4>
      <div class="text-sm text-teal font-weight-bold">${scheme.benefit}</div>
      <div class="saved-item-actions">
        <button type="button" class="btn-text-sm" onclick="openEligibilityModal('${scheme.id}')">View Details</button>
        <button type="button" class="btn-text-sm text-muted" onclick="toggleBookmark('${scheme.id}'); renderSavedList();">Remove ✕</button>
      </div>
    </div>
  `).join('');
}

/* ==========================================================================
   13. TOAST NOTIFICATIONS UTILITY
   ========================================================================== */
function showToast(message, type = 'normal') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type === 'error' ? 'toast-error' : (type === 'info' ? 'toast-info' : '')}`;
  
  let icon = 'ℹ️';
  if (type === 'error') icon = '⚠️';
  else if (type === 'info') icon = '💡';
  else icon = '✓';

  toast.innerHTML = `
    <span>${icon}</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

/**
 * Utility helper
 */
function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}
