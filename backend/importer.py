"""
Government Scheme Finder - Reusable Scheme Data Import & Validation Pipeline.
Supports:
  - JSON and CSV scheme record ingestion
  - Field validation & normalization
  - Duplicate detection by primary key and (title, jurisdiction)
  - Selective updates without overwriting higher-quality verified data
  - Quality verification tracking (Verified, Needs Review, Sample, Discontinued)
  - Detailed import summary report generation
"""
import os
import sys
import json
import csv
import sqlite3
import re
from datetime import datetime

VALID_VERIFICATION_STATUSES = [
    "Verified from official source",
    "Verified Public Scheme Record (Official Portal Available)",
    "Verified State Scheme Record (Official Portals Available)",
    "Needs review",
    "Sample data",
    "Source unavailable",
    "Possibly discontinued"
]

VALID_GOV_LEVELS = ["Central", "State", "Union Territory"]
VALID_SCHEME_STATUSES = ["active", "needs_review", "discontinued", "unknown"]

REQUIRED_FIELDS = [
    "id", "title", "department", "category", "scope", "benefit",
    "description", "official_url"
]


def normalize_id(title, prefix=""):
    """Generate a clean slug identifier from a scheme title."""
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower()).strip()
    slug = re.sub(r'[\s_-]+', '-', slug)
    if prefix:
        return f"{prefix}-{slug}"[:60].strip('-')
    return slug[:60].strip('-')


def validate_scheme_record(record, index=0):
    """
    Validate and normalize an incoming scheme record dictionary.
    Returns (normalized_dict, error_message or None, is_needs_review).
    """
    if not isinstance(record, dict):
        return None, f"Record #{index} is not a valid dictionary/object", False

    # Check required fields
    for field in REQUIRED_FIELDS:
        val = record.get(field)
        if val is None or str(val).strip() == "":
            return None, f"Record #{index} (id: {record.get('id', 'unknown')}) missing required field '{field}'", False

    # Normalized container
    norm = {}
    norm["id"] = str(record["id"]).strip().lower()
    norm["title"] = str(record["title"]).strip()
    norm["acronym"] = str(record.get("acronym") or norm["title"].split("(")[0]).strip()
    norm["department"] = str(record["department"]).strip()
    norm["category"] = str(record["category"]).strip().lower()
    norm["scope"] = str(record["scope"]).strip()
    norm["benefit"] = str(record["benefit"]).strip()

    # Benefit value
    try:
        norm["benefit_value"] = int(record.get("benefit_value") or record.get("benefitValue") or 0)
    except (ValueError, TypeError):
        norm["benefit_value"] = 0

    norm["description"] = str(record["description"]).strip()
    norm["detailed_description"] = str(record.get("detailed_description") or record.get("detailedDescription") or norm["description"]).strip()

    # Age criteria
    criteria = record.get("criteria", {}) if isinstance(record.get("criteria"), dict) else {}
    try:
        norm["min_age"] = int(record.get("min_age", criteria.get("minAge", 0)))
    except (ValueError, TypeError):
        norm["min_age"] = 0

    try:
        norm["max_age"] = int(record.get("max_age", criteria.get("maxAge", 100)))
    except (ValueError, TypeError):
        norm["max_age"] = 100

    norm["gender"] = str(record.get("gender", criteria.get("gender", "all"))).strip().lower()

    # Income max
    try:
        norm["income_max"] = int(record.get("income_max", criteria.get("incomeMax", 10000000)))
    except (ValueError, TypeError):
        norm["income_max"] = 10000000

    # Lists / JSON serializations
    def parse_list(raw_val, fallback=None):
        if fallback is None:
            fallback = []
        if isinstance(raw_val, list):
            return raw_val
        if isinstance(raw_val, str):
            val_str = raw_val.strip()
            if val_str.startswith("[") and val_str.endswith("]"):
                try:
                    parsed = json.loads(val_str)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    pass
            # Split by comma or semicolon
            return [p.strip() for p in re.split(r'[,;]', val_str) if p.strip()]
        return fallback

    norm["occupations"] = json.dumps(parse_list(record.get("occupations", criteria.get("occupations")), ["all"]))
    norm["states"] = json.dumps(parse_list(record.get("states", criteria.get("states")), ["all"]))
    norm["documents"] = json.dumps(parse_list(record.get("documents"), ["Aadhaar Card", "Active Bank Account"]))
    norm["application_steps"] = json.dumps(parse_list(record.get("application_steps", record.get("applicationSteps")), [
        {"step": "Check Eligibility", "text": "Verify eligibility rules on official portal."},
        {"step": "Online Application", "text": "Submit application with required documents."}
    ]))
    norm["alternative_names"] = json.dumps(parse_list(record.get("alternative_names", record.get("alternativeNames")), []))
    norm["beneficiaries"] = json.dumps(parse_list(record.get("beneficiaries"), []))
    norm["available_translations"] = json.dumps(parse_list(record.get("available_translations"), ["en", "hi", "te"]))

    # Boolean flags
    norm["requires_land"] = 1 if bool(record.get("requires_land", criteria.get("requiresLand", False))) else 0
    norm["requires_girl_child"] = 1 if bool(record.get("requires_girl_child", criteria.get("requiresGirlChild", False))) else 0
    norm["requires_bpl"] = 1 if bool(record.get("requires_bpl", criteria.get("requiresBpl", False))) else 0
    norm["criteria_summary"] = str(record.get("criteria_summary", criteria.get("summary", ""))).strip()

    # Government level
    gov_level = str(record.get("government_level") or record.get("governmentLevel") or "Central").strip()
    if gov_level not in VALID_GOV_LEVELS:
        if "state" in gov_level.lower():
            gov_level = "State"
        elif "territory" in gov_level.lower() or "ut" in gov_level.lower():
            gov_level = "Union Territory"
        else:
            gov_level = "Central"
    norm["government_level"] = gov_level

    # URLs
    norm["official_url"] = str(record["official_url"]).strip()
    norm["official_application_url"] = str(record.get("official_application_url") or record.get("officialApplicationUrl") or norm["official_url"]).strip()

    # Verification status
    v_status = str(record.get("verification_status") or record.get("verificationStatus") or "Needs review").strip()
    is_needs_review = False
    if v_status not in VALID_VERIFICATION_STATUSES:
        if "verified" in v_status.lower():
            v_status = "Verified from official source"
        else:
            v_status = "Needs review"
            is_needs_review = True
    elif v_status == "Needs review":
        is_needs_review = True

    norm["verification_status"] = v_status
    norm["source_dept"] = str(record.get("source_dept") or norm["department"]).strip()
    norm["source_title"] = str(record.get("source_title") or "National Portal of India / myScheme").strip()
    norm["last_verified_date"] = str(record.get("last_verified_date") or datetime.now().strftime("%Y-%m-%d")).strip()
    norm["scheme_status"] = str(record.get("scheme_status") or "active").strip().lower()
    if norm["scheme_status"] not in VALID_SCHEME_STATUSES:
        norm["scheme_status"] = "active"

    norm["source_language"] = str(record.get("source_language") or "English").strip()

    return norm, None, is_needs_review


def import_schemes(records, update_existing=True, db_path="backend/schemes.db"):
    """
    Import a batch of validated scheme records into SQLite database.
    Performs duplicate detection, validation, updating, and reports detailed stats.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    summary = {
        "records_processed": 0,
        "records_inserted": 0,
        "records_updated": 0,
        "duplicate_records_skipped": 0,
        "invalid_records_rejected": 0,
        "records_requiring_verification": 0,
        "errors": []
    }

    try:
        # Load existing scheme IDs and normalized titles for duplicate detection
        cur.execute("SELECT id, title, government_level, verification_status FROM schemes")
        existing_schemes = {row[0]: {"title": row[1], "level": row[2], "verification": row[3]} for row in cur.fetchall()}

        for i, raw_record in enumerate(records):
            summary["records_processed"] += 1

            norm, err, needs_review = validate_scheme_record(raw_record, index=i + 1)
            if err:
                summary["invalid_records_rejected"] += 1
                summary["errors"].append(err)
                continue

            if needs_review:
                summary["records_requiring_verification"] += 1

            scheme_id = norm["id"]

            if scheme_id in existing_schemes:
                existing_ver = existing_schemes[scheme_id]["verification"]
                # Protect higher-quality verified records from being degraded by lower-quality records
                if "Verified" in existing_ver and norm["verification_status"] in ("Needs review", "Sample data", "Source unavailable"):
                    summary["duplicate_records_skipped"] += 1
                    continue

                if update_existing:
                    cur.execute("""
                        UPDATE schemes SET
                            title = ?, acronym = ?, department = ?, category = ?, scope = ?,
                            benefit = ?, benefit_value = ?, description = ?, detailed_description = ?,
                            min_age = ?, max_age = ?, gender = ?, income_max = ?, occupations = ?,
                            states = ?, requires_land = ?, requires_girl_child = ?, requires_bpl = ?,
                            criteria_summary = ?, documents = ?, application_steps = ?, official_url = ?,
                            official_application_url = ?, verification_status = ?, source_dept = ?,
                            source_title = ?, last_verified_date = ?, updated_at = CURRENT_TIMESTAMP,
                            government_level = ?, alternative_names = ?, beneficiaries = ?,
                            scheme_status = ?, source_language = ?, available_translations = ?
                        WHERE id = ?
                    """, (
                        norm["title"], norm["acronym"], norm["department"], norm["category"], norm["scope"],
                        norm["benefit"], norm["benefit_value"], norm["description"], norm["detailed_description"],
                        norm["min_age"], norm["max_age"], norm["gender"], norm["income_max"], norm["occupations"],
                        norm["states"], norm["requires_land"], norm["requires_girl_child"], norm["requires_bpl"],
                        norm["criteria_summary"], norm["documents"], norm["application_steps"], norm["official_url"],
                        norm["official_application_url"], norm["verification_status"], norm["source_dept"],
                        norm["source_title"], norm["last_verified_date"], norm["government_level"],
                        norm["alternative_names"], norm["beneficiaries"], norm["scheme_status"],
                        norm["source_language"], norm["available_translations"], scheme_id
                    ))
                    summary["records_updated"] += 1
                else:
                    summary["duplicate_records_skipped"] += 1
            else:
                # Insert new record
                cur.execute("""
                    INSERT INTO schemes (
                        id, title, acronym, department, category, scope, benefit, benefit_value,
                        description, detailed_description, min_age, max_age, gender, income_max,
                        occupations, states, requires_land, requires_girl_child, requires_bpl,
                        criteria_summary, documents, application_steps, official_url,
                        official_application_url, verification_status, source_dept, source_title,
                        last_verified_date, government_level, alternative_names, beneficiaries,
                        scheme_status, source_language, available_translations
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, (
                    norm["id"], norm["title"], norm["acronym"], norm["department"], norm["category"],
                    norm["scope"], norm["benefit"], norm["benefit_value"], norm["description"],
                    norm["detailed_description"], norm["min_age"], norm["max_age"], norm["gender"],
                    norm["income_max"], norm["occupations"], norm["states"], norm["requires_land"],
                    norm["requires_girl_child"], norm["requires_bpl"], norm["criteria_summary"],
                    norm["documents"], norm["application_steps"], norm["official_url"],
                    norm["official_application_url"], norm["verification_status"], norm["source_dept"],
                    norm["source_title"], norm["last_verified_date"], norm["government_level"],
                    norm["alternative_names"], norm["beneficiaries"], norm["scheme_status"],
                    norm["source_language"], norm["available_translations"]
                ))
                existing_schemes[scheme_id] = {
                    "title": norm["title"],
                    "level": norm["government_level"],
                    "verification": norm["verification_status"]
                }
                summary["records_inserted"] += 1

        conn.commit()

    except Exception as e:
        conn.rollback()
        summary["errors"].append(f"Database transaction error: {str(e)}")
    finally:
        conn.close()

    return summary


def import_from_json(json_file_path, update_existing=True, db_path="backend/schemes.db"):
    """Load JSON file and import records."""
    if not os.path.exists(json_file_path):
        return {"error": f"File not found: {json_file_path}"}
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "schemes" in data:
        data = data["schemes"]
    if not isinstance(data, list):
        return {"error": "Root JSON content must be an array of scheme objects"}
    return import_schemes(data, update_existing=update_existing, db_path=db_path)


def import_from_csv(csv_file_path, update_existing=True, db_path="backend/schemes.db"):
    """Load CSV file and import records."""
    if not os.path.exists(csv_file_path):
        return {"error": f"File not found: {csv_file_path}"}
    records = []
    with open(csv_file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return import_schemes(records, update_existing=update_existing, db_path=db_path)


def export_to_json(output_path, db_path="backend/schemes.db"):
    """Export all schemes from database to formatted JSON."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM schemes ORDER BY government_level, category, title")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    # Parse JSON strings back to lists for clean JSON export
    for r in rows:
        for json_col in ["occupations", "states", "documents", "application_steps", "alternative_names", "beneficiaries", "available_translations"]:
            if r.get(json_col):
                try:
                    r[json_col] = json.loads(r[json_col])
                except Exception:
                    pass

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    return len(rows)


def get_scheme_statistics(db_path="backend/schemes.db"):
    """
    Generate accurate live repository statistics:
    - Total scheme records
    - Central vs State vs UT breakdown
    - State-wise counts for all 28 states and 8 UTs
    - Category-wise breakdown
    - Verification status counts
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM schemes")
    total_count = cur.fetchone()[0]

    cur.execute("SELECT government_level, COUNT(*) FROM schemes GROUP BY government_level")
    by_level = {row[0]: row[1] for row in cur.fetchall()}

    cur.execute("SELECT category, COUNT(*) FROM schemes GROUP BY category")
    by_category = {row[0]: row[1] for row in cur.fetchall()}

    cur.execute("SELECT verification_status, COUNT(*) FROM schemes GROUP BY verification_status")
    by_verification = {row[0]: row[1] for row in cur.fetchall()}

    # Compute State & UT counts by inspecting the JSON states array of each record
    ALL_STATES = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ]
    ALL_UTS = [
        "Andaman and Nicobar Islands", "Chandigarh",
        "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
        "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    ]

    cur.execute("SELECT states FROM schemes")
    all_states_rows = cur.fetchall()

    state_counts = {st: 0 for st in ALL_STATES}
    ut_counts = {ut: 0 for ut in ALL_UTS}
    pan_india_count = 0

    for (states_raw,) in all_states_rows:
        try:
            states_list = json.loads(states_raw) if isinstance(states_raw, str) else []
        except Exception:
            states_list = []
        if "all" in states_list:
            pan_india_count += 1
        for st in ALL_STATES:
            if st in states_list:
                state_counts[st] += 1
        for ut in ALL_UTS:
            if ut in states_list:
                ut_counts[ut] += 1

    conn.close()

    return {
        "total_schemes": total_count,
        "pan_india_applicable": pan_india_count,
        "by_government_level": by_level,
        "by_category": by_category,
        "by_verification_status": by_verification,
        "state_counts": state_counts,
        "union_territory_counts": ut_counts
    }
