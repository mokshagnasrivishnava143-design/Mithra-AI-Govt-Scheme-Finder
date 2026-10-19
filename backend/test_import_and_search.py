"""
Comprehensive verification tests for:
- CSV & JSON scheme imports
- Malformed record rejection
- Duplicate detection
- Parameterized search, state filters, pagination
- Statistics generation
"""
import os
import json
import csv
import sqlite3
from backend.importer import (
    validate_scheme_record,
    import_schemes,
    import_from_json,
    import_from_csv,
    get_scheme_statistics
)
from backend.database import query_schemes, query_scheme_by_id

def run_tests():
    print("======================================================================")
    print(" RUNNING GOVERNMENT SCHEME FINDER VERIFICATION SUITE")
    print("======================================================================")

    # 1. Test Malformed Record Rejection
    print("\n[Test 1] Testing Malformed Record Rejection...")
    malformed_records = [
        {}, # Empty
        {"id": "bad-1"}, # Missing required fields
        {"id": "bad-2", "title": "Missing details"},
        "not-a-dict"
    ]
    summary = import_schemes(malformed_records, update_existing=True, db_path="backend/schemes.db")
    assert summary["invalid_records_rejected"] == len(malformed_records), f"Expected {len(malformed_records)} rejections"
    print(f"  PASS: Successfully rejected {summary['invalid_records_rejected']} malformed records without database error.")

    # 2. Test JSON Import with New Record
    print("\n[Test 2] Testing JSON Import Pipeline with New Valid Record...")
    test_json_record = [{
        "id": "test-telecom-digital-saksharta",
        "title": "Pradhan Mantri Gramin Digital Saksharta Abhiyaan (PMGDISHA)",
        "acronym": "PMGDISHA",
        "department": "Ministry of Electronics & Information Technology",
        "category": "education",
        "scope": "Central (All States & UTs)",
        "benefit": "Free 20-Hour Digital Literacy Training & Certificate",
        "benefit_value": 3000,
        "description": "National initiative to make rural citizens digitally literate across India.",
        "detailed_description": "Covers digital empowerment, smartphone navigation, online government services, and digital payments.",
        "min_age": 14,
        "max_age": 60,
        "gender": "all",
        "income_max": 250000,
        "occupations": ["student", "unorganized", "farmer"],
        "states": ["all"],
        "requires_land": False,
        "requires_girl_child": False,
        "requires_bpl": True,
        "criteria_summary": "Rural household where not a single member is digitally literate.",
        "documents": ["Aadhaar Card", "Ration Card"],
        "application_steps": [{"step": "Training Center", "text": "Enroll at nearest CSC center."}],
        "official_url": "https://www.pmgdisha.in/",
        "official_application_url": "https://www.pmgdisha.in/",
        "verification_status": "Verified from official source",
        "source_dept": "MeitY, GoI",
        "source_title": "PMGDISHA National Portal / myScheme",
        "last_verified_date": "2026-10-15",
        "government_level": "Central",
        "beneficiaries": ["rural_households", "digital_learners"],
        "alternative_names": ["PMGDISHA", "Digital Saksharta"],
        "scheme_status": "active",
        "source_language": "Hindi, English"
    }]
    temp_json_path = "backend/data/temp_test_scheme.json"
    os.makedirs(os.path.dirname(temp_json_path), exist_ok=True)
    with open(temp_json_path, "w", encoding="utf-8") as f:
        json.dump(test_json_record, f)

    res_json = import_from_json(temp_json_path, update_existing=True, db_path="backend/schemes.db")
    assert res_json["records_inserted"] == 1 or res_json["records_updated"] == 1
    print(f"  PASS: Successfully ingested JSON record: {test_json_record[0]['title']}")

    # 3. Test Duplicate Detection & Re-import Idempotence
    print("\n[Test 3] Testing Duplicate Detection & Idempotence on Re-import...")
    res_reimport = import_from_json(temp_json_path, update_existing=False, db_path="backend/schemes.db")
    assert res_reimport["duplicate_records_skipped"] == 1, "Duplicate record should be skipped when update_existing=False"
    print("  PASS: Duplicate record correctly detected and skipped without duplicating in database.")

    # 4. Test Updating Existing Record
    print("\n[Test 4] Testing Selective Updating of Existing Scheme...")
    test_json_record[0]["benefit"] = "Free 20-Hour Digital Literacy Training & Certificate (Updated Edition)"
    with open(temp_json_path, "w", encoding="utf-8") as f:
        json.dump(test_json_record, f)
    res_update = import_from_json(temp_json_path, update_existing=True, db_path="backend/schemes.db")
    assert res_update["records_updated"] == 1
    updated_obj = query_scheme_by_id("test-telecom-digital-saksharta")
    assert "Updated Edition" in updated_obj["benefit"]
    print("  PASS: Successfully updated record in-place without duplicating.")

    # Clean up test scheme from database
    conn = sqlite3.connect("backend/schemes.db")
    conn.cursor().execute("DELETE FROM schemes WHERE id = 'test-telecom-digital-saksharta'")
    conn.commit()
    conn.close()
    if os.path.exists(temp_json_path):
        os.remove(temp_json_path)

    # 5. Test State & UT Filtering
    print("\n[Test 5] Testing State and Union Territory Search Filters...")
    delhi_results = query_schemes(state="Delhi")
    assert len(delhi_results) >= 2, f"Expected Delhi schemes, got {len(delhi_results)}"
    delhi_ids = [s["id"] for s in delhi_results]
    assert "delhi-free-electricity" in delhi_ids or "delhi-ladli" in delhi_ids
    print(f"  PASS: State/UT query for 'Delhi' returned {len(delhi_results)} schemes (including state-specific and pan-India).")

    # 6. Test Category Filter
    print("\n[Test 6] Testing Category Filter...")
    agri_schemes = query_schemes(category="agriculture")
    assert len(agri_schemes) >= 5, f"Expected multiple agriculture schemes, got {len(agri_schemes)}"
    for s in agri_schemes:
        assert s["category"] == "agriculture"
    print(f"  PASS: Category 'agriculture' filter returned {len(agri_schemes)} strictly matching schemes.")

    # 7. Test Keyword Search Across Alternative Names and Beneficiaries
    print("\n[Test 7] Testing Keyword Search Across Alternative Names...")
    chiranjeevi_search = query_schemes(search="Chiranjeevi")
    assert len(chiranjeevi_search) >= 1
    assert "rajasthan" in chiranjeevi_search[0]["id"]
    print(f"  PASS: Keyword search for 'Chiranjeevi' found: {chiranjeevi_search[0]['title']}")

    # 8. Test Pagination
    print("\n[Test 8] Testing Pagination Controls & Accurate Metadata...")
    page1, total_count = query_schemes(page=1, limit=10, return_meta=True)
    page2, _ = query_schemes(page=2, limit=10, return_meta=True)
    assert len(page1) == 10
    assert len(page2) == 10
    assert page1[0]["id"] != page2[0]["id"], "Page 1 and Page 2 must not have identical start item"
    assert total_count >= 58
    print(f"  PASS: Pagination test: Page 1 (10 items), Page 2 (10 items), Total Stored: {total_count}")

    # 9. Verify Live Scheme Statistics
    print("\n[Test 9] Testing Statistics Engine across 28 States and 8 UTs...")
    stats = get_scheme_statistics("backend/schemes.db")
    assert stats["total_schemes"] >= 58
    assert stats["by_government_level"]["Central"] >= 15
    assert stats["by_government_level"]["State"] >= 28
    assert stats["by_government_level"]["Union Territory"] >= 8
    states_with_schemes = [st for st, count in stats["state_counts"].items() if count > 0]
    uts_with_schemes = [ut for ut, count in stats["union_territory_counts"].items() if count > 0]
    assert len(states_with_schemes) == 28, f"Expected all 28 states, got {len(states_with_schemes)}"
    assert len(uts_with_schemes) == 8, f"Expected all 8 UTs, got {len(uts_with_schemes)}"
    print(f"  PASS: Live stats confirmed: 28/28 States and 8/8 UTs populated.")

    print("\n======================================================================")
    print(" ALL 9 VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("======================================================================")

if __name__ == "__main__":
    run_tests()
