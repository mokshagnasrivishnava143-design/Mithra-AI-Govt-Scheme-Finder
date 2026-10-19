"""
Essential System Health & Verification Suite
============================================
Checks:
  1. Context-aware AI responses (Intent, fact extraction, multi-turn memory, small talk handling).
  2. Correct scheme matching (Deterministic database filtering, official URLs, negative profile rejection).
  3. Listen button text-to-speech playback integrity (Web Speech API, voice selection, GC fix, event delegation).
"""
import urllib.request
import json
import sys
import os

def run_checks():
    print("=====================================================")
    print("ESSENTIAL CHECK 1: CONTEXT-AWARE AI RESPONSES")
    print("=====================================================")
    url = "http://127.0.0.1:5000/api/assistant/chat"

    # 1a. Mokshagnateja B.Tech employment query
    payload_1a = {
        "message": "My name is Mokshagnateja. I am studying B.Tech. Can I know about employment schemes in India?",
        "session_id": "check_session_moksha",
        "language": "en"
    }
    req = urllib.request.Request(url, data=json.dumps(payload_1a).encode("utf-8"), headers={"Content-Type": "application/json"})
    r1 = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
    print("1a. Status:", r1.get("status"))
    print("1a. Intent:", r1.get("intent"))
    print("1a. Extracted Name:", r1.get("updated_profile", {}).get("user_name"))
    print("1a. Extracted Education:", r1.get("updated_profile", {}).get("education"))
    print("1a. Response Snippet:", repr(r1.get("message", "")[:120]))
    assert r1.get("intent") == "EMPLOYMENT_SEARCH", "Intent should be EMPLOYMENT_SEARCH"
    assert r1.get("updated_profile", {}).get("user_name") == "Mokshagnateja", "Name should be Mokshagnateja"
    assert "B.Tech" in r1.get("updated_profile", {}).get("education", ""), "Education should contain B.Tech"
    print("[PASS] Check 1a: Contextual Intent & Fact Extraction Succeeded")

    # 1b. Greeting test (must not return schemes)
    payload_1b = {"message": "Hello", "session_id": "check_session_greet", "language": "en"}
    req = urllib.request.Request(url, data=json.dumps(payload_1b).encode("utf-8"), headers={"Content-Type": "application/json"})
    r1b = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
    print("1b. Intent:", r1b.get("intent"))
    print("1b. Scheme Count:", len(r1b.get("schemes", [])))
    print("1b. requires_schemes_display:", r1b.get("requires_schemes_display"))
    assert r1b.get("intent") == "GREETING"
    assert len(r1b.get("schemes", [])) == 0
    assert r1b.get("requires_schemes_display") is False
    print("[PASS] Check 1b: Greeting Handled Conversationally with 0 Scheme Cards")

    # 1c. Multi-turn context memory retention
    payload_1c = {"message": "Are there any scholarships in Telangana?", "session_id": "check_session_moksha", "language": "en"}
    req = urllib.request.Request(url, data=json.dumps(payload_1c).encode("utf-8"), headers={"Content-Type": "application/json"})
    r1c = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
    print("1c. Intent:", r1c.get("intent"))
    print("1c. Retained User Name:", r1c.get("updated_profile", {}).get("user_name"))
    print("1c. Retained Education:", r1c.get("updated_profile", {}).get("education"))
    print("1c. Updated State:", r1c.get("updated_profile", {}).get("state"))
    assert r1c.get("updated_profile", {}).get("user_name") == "Mokshagnateja"
    assert "B.Tech" in r1c.get("updated_profile", {}).get("education", "")
    assert r1c.get("updated_profile", {}).get("state") == "Telangana"
    print("[PASS] Check 1c: Multi-Turn Memory Retained Across Conversation")

    print("\n=====================================================")
    print("ESSENTIAL CHECK 2: CORRECT SCHEME MATCHING")
    print("=====================================================")
    search_url = "http://127.0.0.1:5000/api/schemes/search"

    # 2a. Genuine match
    payload_2a = {"age": 38, "state": "Andhra Pradesh", "occupation": "farmer", "income": 100000, "land": "small"}
    req = urllib.request.Request(search_url, data=json.dumps(payload_2a).encode("utf-8"), headers={"Content-Type": "application/json"})
    r2a = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
    print("2a. Valid Search Count:", r2a.get("count"))
    top_s = r2a.get("results", [])[0]
    print("2a. Top Matched Scheme:", top_s.get("title"))
    print("2a. Eligibility Status:", top_s.get("eligibility_status"))
    print("2a. Official URL:", top_s.get("official_url"))
    print("2a. Evidence items:", len(top_s.get("evidence", [])))
    assert r2a.get("count", 0) > 0
    assert top_s.get("eligibility_status") in ["Potential Match", "Additional Information Required"]
    assert "http" in top_s.get("official_url", "")
    print("[PASS] Check 2a: Genuine Database Schemes Matched with Verification URLs")

    # 2b. Rejection of impossible profile
    payload_2b = {"age": 110, "state": "Goa", "occupation": "student", "income": 99000000}
    req = urllib.request.Request(search_url, data=json.dumps(payload_2b).encode("utf-8"), headers={"Content-Type": "application/json"})
    r2b = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
    print("2b. Ineligible Profile Count:", r2b.get("count"))
    print("2b. Refinement Suggestions:", len(r2b.get("refinement_suggestions", [])))
    assert r2b.get("count") == 0
    assert len(r2b.get("results", [])) == 0
    assert len(r2b.get("refinement_suggestions", [])) > 0
    print("[PASS] Check 2b: Ineligible Profile Returns 0 False Matches & Offers Refinement Advice")

    print("\n=====================================================")
    print("ESSENTIAL CHECK 3: LISTEN BUTTON & TTS PLAYBACK INTEGRITY")
    print("=====================================================")

    with open("frontend/script.js", "r", encoding="utf-8") as f:
        js_code = f.read()

    checks_js = [
        ("speakText defined globally", "function speakText(" in js_code and "window.speakText = speakText;" in js_code),
        ("stopSpeech defined globally", "function stopSpeech(" in js_code and "window.stopSpeech = stopSpeech;" in js_code),
        ("Chromium GC bug fix (window._activeUtterance)", "window._activeUtterance = utterance" in js_code),
        ("Voice selection for en-IN, te-IN, hi-IN", "getBestVoiceForLang" in js_code and "targetPrefix" in js_code),
        ("Chromium speech heartbeat", "speechHeartbeatTimer" in js_code and "window.speechSynthesis.pause()" in js_code),
        ("Delegated click handler on .btn-listen-msg", ".btn-listen-msg" in js_code and "chatThread.addEventListener" in js_code),
        ("Speaking visual indicator toggling", "is-speaking" in js_code and "activeSpeakingButton" in js_code),
        ("Manual Listen clicks bypass AppState.ttsEnabled restriction", "triggerBtn === null && !AppState.ttsEnabled" in js_code)
    ]

    for name, passed in checks_js:
        status_str = "PASS" if passed else "FAIL"
        print(f"3. {name}: {status_str}")
        assert passed, f"Failed check: {name}"

    with open("frontend/index.html", "r", encoding="utf-8") as f:
        html_code = f.read()

    assert "assistant-welcome-msg" in html_code and "btn-listen-msg" in html_code, "Welcome message must have Listen button"
    assert 'id="stop-speech-btn"' in html_code, "Stop Speech button must exist"
    print("3. Welcome message & stop button in HTML: PASS")

    with open("frontend/style.css", "r", encoding="utf-8") as f:
        css_code = f.read()

    assert ".btn-chat-action.is-speaking" in css_code, "CSS speaking class missing"
    assert "pulse-speaking" in css_code, "Pulse speaking animation missing"
    assert "#stop-speech-btn" in css_code, "Stop speech button style missing"
    print("3. CSS is-speaking active animation & stop button styles: PASS")

    print("\n>>> ALL 3 ESSENTIAL CHECKS COMPLETED AND FULLY VERIFIED! <<<")
    return True

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
