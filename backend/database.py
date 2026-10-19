"""
Database module for Government Scheme Finder.
Manages SQLite connection, table schema creation, data seeding, and safe parameterized queries.
"""
import sqlite3
import json
import os
from .config import Config
from .seed_data import INITIAL_SCHEMES


def get_db_connection():
    """
    Establish a thread-safe connection to the SQLite database.
    Enables Row factory for dictionary-like column access.
    """
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initialize SQLite database tables and seed initial records if empty.
    """
    db_dir = os.path.dirname(Config.DATABASE_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create schemes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schemes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                acronym TEXT NOT NULL,
                department TEXT NOT NULL,
                category TEXT NOT NULL,
                scope TEXT NOT NULL,
                benefit TEXT NOT NULL,
                benefit_value INTEGER NOT NULL DEFAULT 0,
                description TEXT NOT NULL,
                min_age INTEGER NOT NULL DEFAULT 0,
                max_age INTEGER NOT NULL DEFAULT 100,
                gender TEXT NOT NULL DEFAULT 'all',
                income_max INTEGER NOT NULL DEFAULT 10000000,
                occupations TEXT NOT NULL DEFAULT '["all"]',
                states TEXT NOT NULL DEFAULT '["all"]',
                requires_land INTEGER NOT NULL DEFAULT 0,
                requires_girl_child INTEGER NOT NULL DEFAULT 0,
                requires_bpl INTEGER NOT NULL DEFAULT 0,
                criteria_summary TEXT,
                documents TEXT NOT NULL DEFAULT '[]',
                application_steps TEXT NOT NULL DEFAULT '[]',
                official_url TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                source_dept TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Check existing count
        cursor.execute("SELECT COUNT(*) FROM schemes")
        count = cursor.fetchone()[0]

        if count == 0:
            print("[Database] Seeding authentic government scheme records into SQLite...")
            for s in INITIAL_SCHEMES:
                cursor.execute("""
                    INSERT INTO schemes (
                        id, title, acronym, department, category, scope, benefit, benefit_value,
                        description, min_age, max_age, gender, income_max, occupations, states,
                        requires_land, requires_girl_child, requires_bpl, criteria_summary,
                        documents, application_steps, official_url, verification_status, source_dept
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, (
                    s["id"],
                    s["title"],
                    s["acronym"],
                    s["department"],
                    s["category"],
                    s["scope"],
                    s["benefit"],
                    s["benefit_value"],
                    s["description"],
                    s["min_age"],
                    s["max_age"],
                    s["gender"],
                    s["income_max"],
                    json.dumps(s["occupations"]),
                    json.dumps(s["states"]),
                    s["requires_land"],
                    s["requires_girl_child"],
                    s["requires_bpl"],
                    s["criteria_summary"],
                    json.dumps(s["documents"]),
                    json.dumps(s["application_steps"]),
                    s["official_url"],
                    s["verification_status"],
                    s["source_dept"]
                ))
            conn.commit()
            print(f"[Database] Successfully seeded {len(INITIAL_SCHEMES)} schemes.")
        else:
            print(f"[Database] Database already initialized with {count} scheme records.")


def row_to_dict(row):
    """
    Convert a sqlite3.Row object to a clean Python dictionary,
    safely parsing JSON strings back into Python arrays/objects.
    """
    if not row:
        return None
    d = dict(row)
    
    # Safe JSON parsing for list fields
    json_columns = [
        "occupations", "states", "documents", "application_steps",
        "alternative_names", "beneficiaries", "available_translations"
    ]
    for col in json_columns:
        if col in d:
            try:
                d[col] = json.loads(d[col])
            except (TypeError, json.JSONDecodeError):
                d[col] = []
        else:
            d[col] = []

    # Criteria sub-object for frontend compatibility
    d["criteria"] = {
        "minAge": d.get("min_age", 0),
        "maxAge": d.get("max_age", 100),
        "gender": d.get("gender", "all"),
        "incomeMax": d.get("income_max", 10000000),
        "occupations": d.get("occupations", []),
        "states": d.get("states", []),
        "requiresLand": bool(d.get("requires_land", 0)),
        "requiresGirlChild": bool(d.get("requires_girl_child", 0)),
        "requiresBpl": bool(d.get("requires_bpl", 0)),
        "summary": d.get("criteria_summary", "")
    }

    # CamelCase aliases for seamless frontend compatibility
    d["benefitValue"] = d.get("benefit_value", 0)
    d["officialUrl"] = d.get("official_url", "")
    d["officialApplicationUrl"] = d.get("official_application_url") or d.get("official_url", "")
    d["verificationStatus"] = d.get("verification_status", "Verified from official source")
    d["sourceDept"] = d.get("source_dept", d.get("department", ""))
    d["sourceTitle"] = d.get("source_title", "National Portal of India / myScheme")
    d["lastVerifiedDate"] = d.get("last_verified_date", "2026-10-15")
    d["governmentLevel"] = d.get("government_level", "Central")
    d["schemeStatus"] = d.get("scheme_status", "active")
    d["detailedDescription"] = d.get("detailed_description") or d.get("description", "")
    d["alternativeNames"] = d.get("alternative_names", [])
    d["applicationSteps"] = d.get("application_steps", [])

    return d


def query_schemes(category=None, state=None, search=None, sort=None,
                  government_level=None, scheme_status=None,
                  verification_status=None, page=None, limit=None, return_meta=False):
    """
    Safely query schemes with filters, case-insensitive keyword search, and pagination.
    If return_meta=True, returns (results, total_matching_count).
    Otherwise returns results list for direct backward compatibility.
    """
    where_clauses = ["1=1"]
    params = []

    if category and category.lower() != 'all':
        where_clauses.append("LOWER(category) = ?")
        params.append(category.lower())

    if government_level and government_level.lower() != 'all':
        where_clauses.append("LOWER(government_level) = ?")
        params.append(government_level.lower())

    if scheme_status and scheme_status.lower() != 'all':
        where_clauses.append("LOWER(scheme_status) = ?")
        params.append(scheme_status.lower())

    if verification_status and verification_status.lower() != 'all':
        where_clauses.append("LOWER(verification_status) LIKE ?")
        params.append(f"%{verification_status.lower()}%")

    if search:
        search_term = f"%{search.strip().lower()}%"
        where_clauses.append("""(
            LOWER(title) LIKE ? OR
            LOWER(acronym) LIKE ? OR
            LOWER(department) LIKE ? OR
            LOWER(benefit) LIKE ? OR
            LOWER(description) LIKE ? OR
            LOWER(detailed_description) LIKE ? OR
            LOWER(criteria_summary) LIKE ? OR
            LOWER(alternative_names) LIKE ? OR
            LOWER(beneficiaries) LIKE ?
        )""")
        params.extend([search_term] * 9)

    where_sql = " AND ".join(where_clauses)

    # Determine sorting
    order_sql = "ORDER BY id ASC"
    if sort == 'amount':
        order_sql = "ORDER BY benefit_value DESC, title ASC"
    elif sort == 'name':
        order_sql = "ORDER BY title ASC"
    elif sort == 'recent':
        order_sql = "ORDER BY created_at DESC"
    elif sort == 'relevance':
        order_sql = "ORDER BY CASE WHEN verification_status LIKE '%Verified%' THEN 0 ELSE 1 END, benefit_value DESC"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM schemes WHERE {where_sql} {order_sql}"
        cursor.execute(query, params)
        rows = cursor.fetchall()

        matched = []
        for r in rows:
            scheme = row_to_dict(r)
            if state and state.lower() != 'all':
                scope_states = [s.lower() for s in scheme.get("states", [])]
                if 'all' not in scope_states and state.lower() not in scope_states:
                    continue
            matched.append(scheme)

        total_count = len(matched)

        # Apply pagination if requested
        if limit is not None and limit > 0:
            current_page = page if (page is not None and page > 0) else 1
            offset = (current_page - 1) * limit
            paginated = matched[offset:offset + limit]
        else:
            paginated = matched

        if return_meta:
            return paginated, total_count
        return paginated


def query_scheme_by_id(scheme_id):
    """
    Retrieve single scheme by primary key ID.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schemes WHERE id = ?", (scheme_id,))
        row = cursor.fetchone()
        return row_to_dict(row)

