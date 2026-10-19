"""
Command-line utility for importing government schemes into Government Scheme Finder.
Usage:
  python import_schemes.py --file backend/data/expanded_schemes.json
  python import_schemes.py --file path/to/schemes.csv
  python import_schemes.py --stats
  python import_schemes.py --export-json output.json
"""
import sys
import os
import argparse
import pprint
from backend.importer import (
    import_from_json,
    import_from_csv,
    export_to_json,
    get_scheme_statistics
)

def main():
    parser = argparse.ArgumentParser(description="Government Scheme Finder - Scheme Import & Export CLI")
    parser.add_argument("--file", "-f", help="Path to JSON or CSV file to import")
    parser.add_argument("--no-update", action="store_true", help="Do not update existing records, only insert new")
    parser.add_argument("--stats", "-s", action="store_true", help="Display live repository statistics")
    parser.add_argument("--export-json", help="Export all database schemes to a JSON file")

    args = parser.parse_args()

    if args.stats:
        print("\n======================================================================")
        print("  GOVERNMENT SCHEME FINDER - REPOSITORY STATISTICS")
        print("======================================================================")
        stats = get_scheme_statistics()
        pprint.pprint(stats)
        return

    if args.export_json:
        count = export_to_json(args.export_json)
        print(f"Exported {count} schemes to {args.export_json}")
        return

    if args.file:
        file_path = args.file
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            sys.exit(1)

        update_existing = not args.no_update
        print(f"Ingesting '{file_path}' (update_existing={update_existing})...")

        if file_path.lower().endswith(".json"):
            summary = import_from_json(file_path, update_existing=update_existing)
        elif file_path.lower().endswith(".csv"):
            summary = import_from_csv(file_path, update_existing=update_existing)
        else:
            print("Error: Unsupported file format. Please specify a .json or .csv file.")
            sys.exit(1)

        print("\n======================================================================")
        print("  IMPORT OPERATION SUMMARY")
        print("======================================================================")
        print(f"  * Records Processed:           {summary.get('records_processed', 0)}")
        print(f"  * Records Inserted:            {summary.get('records_inserted', 0)}")
        print(f"  * Records Updated:             {summary.get('records_updated', 0)}")
        print(f"  * Duplicate Records Skipped:   {summary.get('duplicate_records_skipped', 0)}")
        print(f"  * Invalid Records Rejected:    {summary.get('invalid_records_rejected', 0)}")
        print(f"  * Records Requiring Review:    {summary.get('records_requiring_verification', 0)}")
        if summary.get("errors"):
            print(f"  * Errors Encountered ({len(summary['errors'])}):")
            for err in summary["errors"][:10]:
                print(f"    - {err}")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
