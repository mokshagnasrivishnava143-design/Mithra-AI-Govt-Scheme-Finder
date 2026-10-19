"""
Test script to verify all backend API endpoints and SQLite database operations.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app

def run_tests():
    app = create_app()
    client = app.test_client()

    print("\n--- 1. Testing GET /api/health ---")
    res = client.get('/api/health')
    print("Status:", res.status_code)
    print("Response:", res.get_json())
    assert res.status_code == 200

    print("\n--- 2. Testing GET /api/schemes ---")
    res = client.get('/api/schemes')
    print("Status:", res.status_code)
    data = res.get_json()
    print("Count:", data.get('count'))
    assert res.status_code == 200
    assert data.get('count') >= 12

    print("\n--- 3. Testing GET /api/schemes?category=agriculture ---")
    res = client.get('/api/schemes?category=agriculture')
    print("Status:", res.status_code)
    data = res.get_json()
    print("Agri Schemes Count:", data.get('count'))
    assert res.status_code == 200
    assert data.get('count') >= 3

    print("\n--- 4. Testing GET /api/schemes/pm-kisan ---")
    res = client.get('/api/schemes/pm-kisan')
    print("Status:", res.status_code)
    data = res.get_json()
    print("Title:", data.get('data', {}).get('title'))
    print("Department:", data.get('data', {}).get('department'))
    assert res.status_code == 200
    assert data.get('data', {}).get('acronym') == 'PM-KISAN'

    print("\n--- 5. Testing GET /api/schemes/invalid-id (404 expected) ---")
    res = client.get('/api/schemes/non-existent-scheme')
    print("Status:", res.status_code)
    assert res.status_code == 404

    print("\n--- 6. Testing POST /api/schemes/search (Farmer in Telangana) ---")
    search_payload = {
        "age": 28,
        "gender": "male",
        "state": "Telangana",
        "occupation": "farmer",
        "income": 150000,
        "land": "marginal",
        "category": "OBC",
        "girl_child": False,
        "bpl": False
    }
    res = client.post('/api/schemes/search', json=search_payload)
    print("Status:", res.status_code)
    data = res.get_json()
    print("Matches Count:", data.get('count'))
    top_match = data.get('results', [])[0]
    print("Top Match:", top_match.get('title'), f"({top_match.get('match_score')}% - {top_match.get('match_label')})")
    assert res.status_code == 200
    assert top_match.get('match_score') >= 80

    print("\n--- 7. Testing POST /api/schemes/search with invalid age (400 expected) ---")
    bad_payload = {"age": "invalid_age_str"}
    res = client.post('/api/schemes/search', json=bad_payload)
    print("Status:", res.status_code)
    print("Response:", res.get_json())
    assert res.status_code == 400

    print(" [PASS] ALL BACKEND & DATABASE TESTS PASSED SUCCESSFULLY!")
    print("=" * 50)

if __name__ == '__main__':
    run_tests()
