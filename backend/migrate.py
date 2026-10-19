"""
Migration script for Government Scheme Finder database.
Adds schema extensions for pan-India scheme repository with performance indexes.
Preserves 100% of existing valid scheme records.
"""
import sqlite3
import os
import sys

def migrate_database(db_path="backend/schemes.db"):
    if not os.path.exists(db_path):
        print(f"[Migration Error] Database not found at {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    try:
        # 1. Inspect existing columns
        cur.execute("PRAGMA table_info(schemes)")
        existing_cols = {row[1] for row in cur.fetchall()}

        new_columns = [
            ("alternative_names", "TEXT NOT NULL DEFAULT '[]'"),
            ("detailed_description", "TEXT DEFAULT ''"),
            ("government_level", "TEXT NOT NULL DEFAULT 'Central'"),
            ("beneficiaries", "TEXT NOT NULL DEFAULT '[]'"),
            ("official_application_url", "TEXT DEFAULT ''"),
            ("source_title", "TEXT DEFAULT 'National Portal of India / myScheme'"),
            ("last_verified_date", "TEXT DEFAULT '2026-10-15'"),
            ("updated_at", "TIMESTAMP DEFAULT '2026-10-15 00:00:00'"),
            ("scheme_status", "TEXT NOT NULL DEFAULT 'active'"),
            ("source_language", "TEXT NOT NULL DEFAULT 'English'"),
            ("available_translations", "TEXT NOT NULL DEFAULT '[\"en\", \"hi\", \"te\"]'")
        ]

        added = []
        for col_name, col_def in new_columns:
            if col_name not in existing_cols:
                cur.execute(f"ALTER TABLE schemes ADD COLUMN {col_name} {col_def}")
                added.append(col_name)

        # 2. Create performance indexes
        indexes = [
            ("idx_schemes_category", "category"),
            ("idx_schemes_level", "government_level"),
            ("idx_schemes_status", "scheme_status"),
            ("idx_schemes_verification", "verification_status"),
            ("idx_schemes_age", "min_age, max_age"),
            ("idx_schemes_income", "income_max")
        ]

        for idx_name, col_list in indexes:
            cur.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON schemes({col_list})")

        # 3. Update existing 12 schemes metadata
        cur.execute("""
            UPDATE schemes 
            SET government_level = CASE 
                WHEN id = 'rythu-bharosa-bandhu' THEN 'State'
                ELSE 'Central'
            END,
            scheme_status = 'active',
            last_verified_date = '2026-10-15',
            source_title = 'Official Portal of India / myScheme'
        """)
        conn.commit()

        cur.execute("SELECT count(*) FROM schemes")
        count = cur.fetchone()[0]

        print(f"[Migration Success] Added columns: {added}")
        print(f"[Migration Success] Total existing schemes preserved: {count}")
        return True

    except Exception as e:
        conn.rollback()
        print(f"[Migration Error] {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    db_file = sys.argv[1] if len(sys.argv) > 1 else "backend/schemes.db"
    migrate_database(db_file)
