"""
Configuration module for Government Scheme Finder backend.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))

# Load .env file if present in project root
env_file = os.path.join(PROJECT_ROOT, '.env')
if os.path.exists(env_file):
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    k_str = k.strip()
                    v_str = v.strip()
                    if k_str and v_str and k_str not in os.environ:
                        os.environ[k_str] = v_str
    except Exception:
        pass

class Config:
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or os.path.join(BASE_DIR, 'schemes.db')
    FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')
    PORT = int(os.environ.get('PORT', 5000))
    HOST = os.environ.get('HOST', '127.0.0.1')
    DISCLAIMER = (
        "Preliminary eligibility match only. Final approval and disbursement are determined "
        "exclusively by the respective government ministry, nodal agency, or bank. This service "
        "does not guarantee sanction."
    )
