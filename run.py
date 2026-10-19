#!/usr/bin/env python3
"""
Main entry point script to run Government Scheme Finder Backend & Application.
Usage:
    python run.py
"""
import os
import sys

# Ensure backend package can be imported from root directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.config import Config

if __name__ == '__main__':
    app = create_app()
    print("=" * 70)
    print("  GOVERNMENT SCHEME FINDER - BACKEND & API SERVICE")
    print("=" * 70)
    print(f" * Server Running at: http://{Config.HOST}:{Config.PORT}")
    print(f" * Web Interface at:  http://{Config.HOST}:{Config.PORT}/")
    print(f" * Schemes REST API:  http://{Config.HOST}:{Config.PORT}/api/schemes")
    print(f" * API Healthcheck:   http://{Config.HOST}:{Config.PORT}/api/health")
    print(f" * SQLite Database:   {Config.DATABASE_PATH}")
    print("=" * 70)
    print(" Press CTRL+C to stop the server.")
    print("=" * 70)
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
