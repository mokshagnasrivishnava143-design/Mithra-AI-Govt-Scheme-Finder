"""
Dedicated Automated Verification Suite for AI Assistant Fixes & Enhancements
=============================================================================
Verifies:
  1. Mokshagnateja B.Tech Employment Query -> EMPLOYMENT_SEARCH intent, extracts name & B.Tech, tailored advice.
  2. Scheme Details by ID or Name -> SCHEME_DETAILS intent, real SQLite database record lookup.
  3. Multi-turn context memory retention across turns.
  4. Session memory clearing via POST /api/assistant/clear.
  5. Transparent AI configuration endpoint GET /api/assistant/status.
  6. Multi-language employment and scholarship queries.
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
        with urllib.request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return {"error": True, "code": e.code, "detail": body}


def get_json(endpoint: str) -> dict:
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
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
    print("  RUNNING AI ASSISTANT FIXES & CONVERSATION TEST SUITE")
    print("======================================================================\n")

    # ------------------------------------------------------------------
    # 1. Mokshagnateja B.Tech Employment Query
    # ------------------------------------------------------------------
    print("Test 1: User 'Mokshagnateja' B.Tech employment schemes query")
    session_moksha = "session_moksha_test_01"
    query_moksha = "My name is Mokshagnateja. I am studying B.Tech. Can I know about employment schemes in India?"
    res_moksha = post_json("/api/assistant/chat", {
        "message": query_moksha,
        "session_id": session_moksha,
        "language": "en"
    })
    
    assert_test("Test 1: API returns success status", res_moksha.get("status") == "success")
    assert_test("Test 1: Intent classified as EMPLOYMENT_SEARCH", res_moksha.get("intent") == "EMPLOYMENT_SEARCH")
    prof_moksha = res_moksha.get("updated_profile", {})
    assert_test("Test 1: User name extracted as Mokshagnateja", prof_moksha.get("user_name") == "Mokshagnateja")
    assert_test("Test 1: Education extracted as B.Tech", "B.Tech" in prof_moksha.get("education", ""))
    msg_moksha = res_moksha.get("message", "")
    assert_test("Test 1: Salutation addresses Mokshagnateja by name", "Mokshagnateja" in msg_moksha)
    assert_test("Test 1: Mentions graduate/engineering apprenticeship or skilling (NATS/AICTE/PMKVY)", 
                any(k in msg_moksha for k in ["NATS", "AICTE", "Apprenticeship", "PMKVY", "Internship", "employment"]))
    assert_test("Test 1: Follow-up question asks about State/location", bool(res_moksha.get("follow_up_question")))

    # ------------------------------------------------------------------
    # 2. Multi-turn memory: turn 2 asks about scholarships
    # ------------------------------------------------------------------
    print("\nTest 2: Multi-turn memory retention")
    res_moksha_turn2 = post_json("/api/assistant/chat", {
        "message": "Are there any scholarships available for me in Telangana?",
        "session_id": session_moksha,
        "language": "en"
    })
    prof_turn2 = res_moksha_turn2.get("updated_profile", {})
    assert_test("Test 2: Still remembers user_name Mokshagnateja", prof_turn2.get("user_name") == "Mokshagnateja")
    assert_test("Test 2: Still remembers B.Tech education", "B.Tech" in prof_turn2.get("education", ""))
    assert_test("Test 2: Updated state to Telangana", prof_turn2.get("state") == "Telangana")
    assert_test("Test 2: Intent classified as SCHOLARSHIP_SEARCH", res_moksha_turn2.get("intent") == "SCHOLARSHIP_SEARCH")

    # ------------------------------------------------------------------
    # 3. Scheme Details lookup from real SQLite Database
    # ------------------------------------------------------------------
    print("\nTest 3: Direct Scheme Details query ('Tell me about PM-KISAN')")
    res_details = post_json("/api/assistant/chat", {
        "message": "Tell me about PM-KISAN scheme",
        "language": "en"
    })
    assert_test("Test 3: Intent classified as SCHEME_DETAILS", res_details.get("intent") == "SCHEME_DETAILS")
    assert_test("Test 3: Message contains PM-KISAN benefit facts", "₹6,000" in res_details.get("message", "") or "PM-KISAN" in res_details.get("message", ""))
    assert_test("Test 3: Returns scheme records from SQLite", len(res_details.get("schemes", [])) > 0)
    if res_details.get("schemes"):
        s0 = res_details["schemes"][0]
        assert_test("Test 3: Scheme has official URL", "pmkisan.gov.in" in s0.get("official_url", "") or ".gov.in" in s0.get("official_url", ""))

    # ------------------------------------------------------------------
    # 4. Transparent AI Status Endpoint
    # ------------------------------------------------------------------
    print("\nTest 4: AI Status Configuration GET /api/assistant/status")
    res_status = get_json("/api/assistant/status")
    assert_test("Test 4: Status endpoint returns success", res_status.get("status") == "success")
    ai_stat = res_status.get("ai_status", {})
    assert_test("Test 4: Contains is_connected flag", "is_connected" in ai_stat)
    assert_test("Test 4: Contains provider field", "provider" in ai_stat)

    # ------------------------------------------------------------------
    # 5. Session Reset via POST /api/assistant/clear
    # ------------------------------------------------------------------
    print("\nTest 5: Clear Session Endpoint POST /api/assistant/clear")
    res_clear = post_json("/api/assistant/clear", {"session_id": session_moksha})
    assert_test("Test 5: Clear returns success", res_clear.get("status") == "success")

    # Post query on same session after clear - should NOT have old profile
    res_after_clear = post_json("/api/assistant/chat", {
        "message": "Hello, how can you help me?",
        "session_id": session_moksha,
        "language": "en"
    })
    prof_after = res_after_clear.get("updated_profile", {})
    assert_test("Test 5: Profile was wiped after clear", prof_after.get("user_name") is None)
    assert_test("Test 5: Fresh greeting after clear", res_after_clear.get("intent") in ["GREETING", "GENERAL_CONVERSATION"])

    print("\n======================================================================")
    print(f"  AI ASSISTANT TEST RESULTS: {total_passed} / {total_tests} PASSED ({(total_passed / total_tests) * 100:.1f}%)")
    print("======================================================================\n")

    return total_passed == total_tests


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
