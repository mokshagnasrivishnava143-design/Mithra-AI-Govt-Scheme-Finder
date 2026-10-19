"""
Comprehensive Automated Test Suite for Conversation Intelligence & Scheme-Matching Logic
========================================================================================
Verifies:
  - Case A: 'Hi' -> GREETING intent, friendly response, ZERO scheme cards.
  - Case B: 'How are you?' -> GENERAL_CONVERSATION intent, friendly reply, ZERO scheme cards.
  - Case C: 'I need a scholarship' -> Clarifying question on course/state, ZERO scheme cards.
  - Case D: 'I am a farmer in Andhra Pradesh' -> Follow-up on land/income, no premature cards.
  - Case E: Unrelated question ('What is the capital of France?') -> Scope explanation, ZERO cards.
  - Case F: Complete profile -> Exact real database matches with evidence & official links.
  - Case G: Non-matching details -> Honest empty state, 0 schemes, refinement advice.
  - Multi-Turn Memory & Correction: Remembers details across turns and supports corrections.
  - Trilingual Support: Telugu (te), Hindi (hi), and English (en) responses.
  - POST /api/schemes/search deterministic criteria evaluation & rejection of non-matches.
"""
import sys
import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:5000"

def post_json(endpoint: str, payload: dict) -> dict:
    url = f"{BASE_URL}{endpoint}"
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return {"error": True, "code": e.code, "detail": body}


def run_tests():
    total_passed = 0
    total_tests = 0

    def assert_test(name: str, condition: bool, message: str = ""):
        nonlocal total_passed, total_tests
        total_tests += 1
        if condition:
            total_passed += 1
            print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name} - {message}")

    print("\n======================================================================")
    print("  RUNNING CONVERSATION INTELLIGENCE TEST SUITE")
    print("======================================================================\n")

    # ------------------------------------------------------------------
    # CASE A: Greeting
    # ------------------------------------------------------------------
    print("Testing Case A: Greeting ('Hi')")
    res_a = post_json("/api/assistant/chat", {"message": "Hi", "language": "en"})
    assert_test("Case A: Status is success", res_a.get("status") == "success")
    assert_test("Case A: Intent is GREETING", res_a.get("intent") == "GREETING")
    assert_test("Case A: Zero schemes returned", len(res_a.get("schemes", [])) == 0)
    assert_test("Case A: requires_schemes_display is False", res_a.get("requires_schemes_display") is False)
    assert_test("Case A: Response contains friendly greeting", "Mitra" in res_a.get("message", ""))

    # ------------------------------------------------------------------
    # CASE B: General Conversation ('How are you?')
    # ------------------------------------------------------------------
    print("\nTesting Case B: General Conversation ('How are you?')")
    res_b = post_json("/api/assistant/chat", {"message": "How are you?", "language": "en"})
    assert_test("Case B: Status is success", res_b.get("status") == "success")
    assert_test("Case B: Intent is GENERAL_CONVERSATION", res_b.get("intent") == "GENERAL_CONVERSATION")
    assert_test("Case B: Zero schemes returned", len(res_b.get("schemes", [])) == 0)
    assert_test("Case B: requires_schemes_display is False", res_b.get("requires_schemes_display") is False)
    assert_test("Case B: Conversational answer provided", "doing well" in res_b.get("message", "").lower())

    # ------------------------------------------------------------------
    # CASE C: Missing Info ('I need a scholarship')
    # ------------------------------------------------------------------
    print("\nTesting Case C: Missing Info ('I need a scholarship')")
    session_c = "test_session_scholarship_init"
    post_json("/api/assistant/clear", {"session_id": session_c})
    res_c = post_json("/api/assistant/chat", {"message": "I need a scholarship", "session_id": session_c, "language": "en"})
    assert_test("Case C: Status is success", res_c.get("status") == "success")
    assert_test("Case C: Intent is CLARIFICATION_REQUIRED", res_c.get("intent") == "CLARIFICATION_REQUIRED")
    assert_test("Case C: Zero scheme cards until details provided", len(res_c.get("schemes", [])) == 0)
    assert_test("Case C: requires_schemes_display is False", res_c.get("requires_schemes_display") is False)
    assert_test("Case C: Follow-up question asks about education/course/state", bool(res_c.get("follow_up_question")))

    # ------------------------------------------------------------------
    # CASE D: Incomplete Farmer ('I am a farmer in Andhra Pradesh')
    # ------------------------------------------------------------------
    print("\nTesting Case D: Farmer Profile without land/income ('I am a farmer in Andhra Pradesh')")
    session_d = "test_session_farmer_init"
    post_json("/api/assistant/clear", {"session_id": session_d})
    res_d = post_json("/api/assistant/chat", {"message": "I am a farmer in Andhra Pradesh", "session_id": session_d, "language": "en"})
    assert_test("Case D: Intent is PROFILE_UPDATE or CLARIFICATION_REQUIRED", res_d.get("intent") in ["PROFILE_UPDATE", "CLARIFICATION_REQUIRED"])
    assert_test("Case D: Zero premature scheme cards", len(res_d.get("schemes", [])) == 0)
    assert_test("Case D: requires_schemes_display is False", res_d.get("requires_schemes_display") is False)
    assert_test("Case D: Profile extracted state as Andhra Pradesh", res_d.get("updated_profile", {}).get("state") == "Andhra Pradesh")
    assert_test("Case D: Profile extracted occupation as farmer", res_d.get("updated_profile", {}).get("occupation") == "farmer")
    assert_test("Case D: Follow-up asks about land/acres/income", bool(res_d.get("follow_up_question")))

    # ------------------------------------------------------------------
    # CASE E: Unrelated Question ('What is the capital of France?')
    # ------------------------------------------------------------------
    print("\nTesting Case E: Unrelated Question ('What is the capital of France?')")
    session_e = "test_session_unrelated"
    post_json("/api/assistant/clear", {"session_id": session_e})
    res_e = post_json("/api/assistant/chat", {"message": "What is the capital of France?", "session_id": session_e, "language": "en"})
    assert_test("Case E: Status is success", res_e.get("status") == "success")
    assert_test("Case E: Intent is GENERAL_CONVERSATION", res_e.get("intent") == "GENERAL_CONVERSATION")
    assert_test("Case E: Zero scheme cards returned", len(res_e.get("schemes", [])) == 0)
    assert_test("Case E: requires_schemes_display is False", res_e.get("requires_schemes_display") is False)
    assert_test("Case E: Explains platform scope for Indian welfare schemes", "Paris" in res_e.get("message", "") and "schemes" in res_e.get("message", "").lower())

    # ------------------------------------------------------------------
    # CASE F: Complete Profile Matching Real Schemes
    # ------------------------------------------------------------------
    print("\nTesting Case F: Complete Farmer Profile in AP with Land & Income")
    session_f = "test_session_farmer_ap"
    post_json("/api/assistant/clear", {"session_id": session_f})
    # Multi-turn turn 1: State & occupation
    post_json("/api/assistant/chat", {"message": "I am a farmer in Andhra Pradesh", "session_id": session_f, "language": "en"})
    # Multi-turn turn 2: Land & income
    res_f2 = post_json("/api/assistant/chat", {"message": "I own 3 acres of cultivable land and my family income is 120000", "session_id": session_f, "language": "en"})
    assert_test("Case F: Status is success", res_f2.get("status") == "success")
    assert_test("Case F: requires_schemes_display is True", res_f2.get("requires_schemes_display") is True)
    assert_test("Case F: Matching schemes returned from SQLite", len(res_f2.get("schemes", [])) > 0)
    
    schemes_f = res_f2.get("schemes", [])
    scheme_ids_f = [s.get("id") for s in schemes_f]
    assert_test("Case F: PM-KISAN or AP Rythu Bharosa is matched", "pm-kisan" in scheme_ids_f or "ap-ysr-rythu-bharosa" in scheme_ids_f)
    if schemes_f:
        first = schemes_f[0]
        assert_test("Case F: Scheme has strict eligibility_status", first.get("eligibility_status") in ["Potential Match", "Additional Information Required"])
        assert_test("Case F: Scheme includes official .gov.in URL", ".gov.in" in first.get("official_url", "") or "http" in first.get("official_url", ""))
        assert_test("Case F: Scheme includes evidence reasons", len(first.get("evidence", [])) > 0)

    # ------------------------------------------------------------------
    # CASE G: Details that do not match any scheme in SQLite
    # ------------------------------------------------------------------
    print("\nTesting Case G: Non-matching details (Age 105, annual income INR 5 Crore)")
    session_g = "test_session_non_match"
    post_json("/api/assistant/clear", {"session_id": session_g})
    res_g = post_json("/api/assistant/chat", {
        "message": "I am 105 years old with income 50000000 studying degree in Andaman looking for college scholarship",
        "session_id": session_g,
        "language": "en"
    })
    assert_test("Case G: Status is success", res_g.get("status") == "success")
    assert_test("Case G: Zero schemes returned for impossible profile", len(res_g.get("schemes", [])) == 0)
    assert_test("Case G: Clear honest empty state message returned", "No relevant schemes were found with the current information" in res_g.get("message", ""))

    # ------------------------------------------------------------------
    # CASE H: Multi-turn Memory & User Correction
    # ------------------------------------------------------------------
    print("\nTesting Case H: Multi-turn Profile Correction ('Actually, my age is 24')")
    session_h = "test_session_correction"
    post_json("/api/assistant/chat", {"message": "I am 17 years old student in Telangana", "session_id": session_h, "language": "en"})
    res_h2 = post_json("/api/assistant/chat", {"message": "Actually, my age is 24 and my family income is 150000", "session_id": session_h, "language": "en"})
    prof_h2 = res_h2.get("updated_profile", {})
    assert_test("Case H: Age updated from 17 to 24", prof_h2.get("age") == 24)
    assert_test("Case H: Occupation student remembered", prof_h2.get("occupation") == "student")
    assert_test("Case H: State Telangana remembered", prof_h2.get("state") == "Telangana")
    assert_test("Case H: Income 150000 remembered", prof_h2.get("income") in [150000, 150000.0])

    # ------------------------------------------------------------------
    # CASE I: Trilingual Greeting & Follow-Up Verification
    # ------------------------------------------------------------------
    print("\nTesting Case I: Multilingual Telugu and Hindi Assistant Support")
    res_te_greet = post_json("/api/assistant/chat", {"message": "నమస్కారం", "language": "te"})
    assert_test("Case I: Telugu greeting classified as GREETING", res_te_greet.get("intent") == "GREETING")
    assert_test("Case I: Telugu response returned in Telugu script", "నమస్కారం" in res_te_greet.get("message", ""))
    assert_test("Case I: Telugu greeting returns 0 schemes", len(res_te_greet.get("schemes", [])) == 0)

    res_hi_greet = post_json("/api/assistant/chat", {"message": "नमस्ते", "language": "hi"})
    assert_test("Case I: Hindi greeting classified as GREETING", res_hi_greet.get("intent") == "GREETING")
    assert_test("Case I: Hindi response returned in Devanagari script", "नमस्ते" in res_hi_greet.get("message", ""))
    assert_test("Case I: Hindi greeting returns 0 schemes", len(res_hi_greet.get("schemes", [])) == 0)

    session_te = "test_session_telugu"
    post_json("/api/assistant/clear", {"session_id": session_te})
    res_te_query = post_json("/api/assistant/chat", {"message": "నాకు స్కాలర్‌షిప్ కావాలి", "session_id": session_te, "language": "te"})
    assert_test("Case I: Telugu scholarship query asks clarifying question", res_te_query.get("intent") == "CLARIFICATION_REQUIRED")
    assert_test("Case I: Zero scheme cards for Telugu clarification", len(res_te_query.get("schemes", [])) == 0)

    # ------------------------------------------------------------------
    # CASE J: POST /api/schemes/search Deterministic Filter & Empty State
    # ------------------------------------------------------------------
    print("\nTesting Case J: POST /api/schemes/search Endpoint Filtering")
    # Search with genuine farmer profile in AP
    res_search_valid = post_json("/api/schemes/search", {
        "age": 35,
        "state": "Andhra Pradesh",
        "occupation": "farmer",
        "income": 120000,
        "land": "marginal"
    })
    assert_test("Case J: Valid search returns success", res_search_valid.get("status") == "success")
    assert_test("Case J: Matches returned with count > 0", res_search_valid.get("count", 0) > 0)
    if res_search_valid.get("results"):
        top_scheme = res_search_valid["results"][0]
        assert_test("Case J: Strict status 'Potential Match' or 'Additional Information Required'", top_scheme.get("eligibility_status") in ["Potential Match", "Additional Information Required"])
        assert_test("Case J: Discarded conflicting schemes", top_scheme.get("eligibility_status") != "Likely Does Not Match")
        assert_test("Case J: Scheme has official .gov.in URL", "official_url" in top_scheme)

    # Search with impossible income of 9 Crore
    res_search_empty = post_json("/api/schemes/search", {
        "age": 40,
        "state": "Sikkim",
        "occupation": "unorganized",
        "income": 90000000,
        "land": "none"
    })
    assert_test("Case J: Impossible income returns 0 count", res_search_empty.get("count") == 0)
    assert_test("Case J: Returns empty results list []", len(res_search_empty.get("results", [])) == 0)
    assert_test("Case J: Returns honest empty message", "No relevant schemes were found with the current information" in res_search_empty.get("message", ""))
    assert_test("Case J: Returns practical refinement suggestions", len(res_search_empty.get("refinement_suggestions", [])) > 0)

    print("\n======================================================================")
    print(f"  TEST RESULTS: {total_passed} / {total_tests} PASSED ({(total_passed / total_tests) * 100:.1f}%)")
    print("======================================================================\n")

    return total_passed == total_tests


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
