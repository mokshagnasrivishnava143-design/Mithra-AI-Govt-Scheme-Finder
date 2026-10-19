"""
API routes for Government Scheme Finder.
Implements:
  - GET /api/schemes
  - GET /api/schemes/<id>
  - POST /api/schemes/search
"""
import math
from flask import Blueprint, request, jsonify
from ..database import query_schemes, query_scheme_by_id
from ..importer import get_scheme_statistics
from ..config import Config
from ..conversation_engine import (
    evaluate_scheme,
    find_relevant_schemes_from_db,
    get_cached_active_schemes,
    process_chat_message,
    clear_session,
    EligibilityStatus,
    IntentType
)

schemes_bp = Blueprint('schemes', __name__, url_prefix='/api/schemes')


@schemes_bp.route('', methods=['GET'])
def get_all_schemes():
    """
    Retrieve government schemes with optional filters and pagination.
    Query parameters:
      - category: Filter by category (e.g. agriculture, education, health, business, women, social, housing, energy)
      - state: Filter by applicable state/UT (e.g. Telangana, Andhra Pradesh, Maharashtra, Delhi, or 'all')
      - level or government_level: 'Central', 'State', 'Union Territory', or 'all'
      - search or q: Keyword search term across scheme titles, descriptions, benefits, alternative names
      - sort: Sort by 'amount', 'name', 'relevance', or 'recent'
      - page: 1-indexed page number (default 1)
      - limit: items per page (default 12; set to 'all' or 0 for unpaginated)
      - status: 'active', 'needs_review', or 'all'
      - verification: 'verified', 'all'
    """
    try:
        category = request.args.get('category', 'all').strip()
        state = request.args.get('state', 'all').strip()
        level = (request.args.get('level') or request.args.get('government_level') or 'all').strip()
        search = (request.args.get('search') or request.args.get('q') or '').strip()
        sort = request.args.get('sort', 'relevance').strip()
        status = request.args.get('status', 'active').strip()
        verification = request.args.get('verification', 'all').strip()

        # Handle page & limit
        page_raw = request.args.get('page', '1')
        try:
            page = max(1, int(page_raw))
        except (ValueError, TypeError):
            page = 1

        limit_raw = request.args.get('limit', '12').strip().lower()
        if limit_raw in ('all', '0', 'none', '-1'):
            limit = 0
        else:
            try:
                limit = max(1, int(limit_raw))
            except (ValueError, TypeError):
                limit = 12

        paginated_schemes, total_count = query_schemes(
            category=category,
            state=state,
            search=search,
            sort=sort,
            government_level=level,
            scheme_status=status,
            verification_status=verification,
            page=page,
            limit=limit,
            return_meta=True
        )

        total_pages = math.ceil(total_count / limit) if limit > 0 else 1

        return jsonify({
            "status": "success",
            "count": len(paginated_schemes),
            "total_count": total_count,
            "page": page,
            "limit": limit if limit > 0 else total_count,
            "total_pages": total_pages,
            "filters": {
                "category": category,
                "state": state,
                "government_level": level,
                "search": search,
                "sort": sort,
                "status": status,
                "verification": verification
            },
            "data": paginated_schemes,
            "disclaimer": Config.DISCLAIMER
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch schemes from database.",
            "detail": str(e)
        }), 500


@schemes_bp.route('/stats', methods=['GET'])
def get_repository_stats():
    """
    Retrieve repository-wide statistics:
    - Total scheme counts
    - Central vs State vs UT distribution
    - State-wise counts for all 28 states and 8 UTs
    - Category-wise distribution
    - Verification status counts
    """
    try:
        stats = get_scheme_statistics()
        return jsonify({
            "status": "success",
            "data": stats,
            "disclaimer": Config.DISCLAIMER
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to compute repository statistics.",
            "detail": str(e)
        }), 500


@schemes_bp.route('/<scheme_id>', methods=['GET'])
def get_scheme_by_id(scheme_id):
    """
    Retrieve full details for a single government scheme by ID.
    """
    try:
        scheme_id = scheme_id.strip()
        scheme = query_scheme_by_id(scheme_id)

        if not scheme:
            return jsonify({
                "status": "error",
                "message": f"Scheme not found with ID '{scheme_id}'."
            }), 404

        return jsonify({
            "status": "success",
            "data": scheme,
            "disclaimer": Config.DISCLAIMER
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Database query error while retrieving scheme.",
            "detail": str(e)
        }), 500


@schemes_bp.route('/search', methods=['POST'])
def search_matching_schemes():
    """
    Evaluate user profile parameters against government scheme eligibility rules.
    Input JSON payload:
      - age (int, optional, 0 to 120)
      - state (str, optional, defaults to 'all')
      - occupation (str, optional, e.g. farmer, student, vendor, business, unorganized, senior)
      - income (int/float, optional, family annual income in INR)
      - gender (str, optional: female, male, transgender, any)
      - land (str, optional: none, marginal, small, large)
      - category (str, optional: General, OBC, SC, ST, EWS, Minority)
      - disability (str, optional: yes, no)
      - girl_child (bool, optional)
      - bpl (bool, optional)
    """
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request payload must be formatted as application/json."
        }), 400

    data = request.get_json() or {}
    errors = []

    # 1. Input Validation
    age_raw = data.get('age')
    age = None
    if age_raw is not None and str(age_raw).strip() != '':
        try:
            age = int(age_raw)
            if age < 0 or age > 120:
                errors.append("Field 'age' must be an integer between 0 and 120.")
        except (ValueError, TypeError):
            errors.append("Field 'age' must be a valid number.")

    income_raw = data.get('income')
    income = None
    if income_raw is not None and str(income_raw).strip() != '':
        try:
            income = float(income_raw)
            if income < 0:
                errors.append("Field 'income' cannot be negative.")
        except (ValueError, TypeError):
            errors.append("Field 'income' must be a valid number.")

    gender = str(data.get('gender', 'any')).strip().lower()
    state = str(data.get('state', 'all')).strip()
    occupation = str(data.get('occupation', 'any')).strip().lower()
    land = str(data.get('land', 'none')).strip().lower()
    social_category = str(data.get('category', 'General')).strip()
    disability = str(data.get('disability', 'no')).strip().lower()
    has_girl_child = bool(data.get('girl_child', data.get('girlChild', False)))
    has_bpl = bool(data.get('bpl', False))

    if errors:
        return jsonify({
            "status": "error",
            "message": "Invalid input parameters.",
            "errors": errors
        }), 400

    try:
        user_profile = {
            "age": age,
            "gender": gender if gender != 'any' else None,
            "state": state if state.lower() != 'all' else None,
            "occupation": occupation if occupation != 'any' else None,
            "income": income,
            "land": land if land != 'none' else None,
            "social_category": social_category,
            "disability": disability,
            "has_girl_child": has_girl_child,
            "has_bpl": has_bpl
        }

        # Retrieve all candidate schemes with sub-millisecond in-memory cache
        schemes = get_cached_active_schemes()
        evaluated_results = []

        for s in schemes:
            eval_res = evaluate_scheme(s, user_profile)

            # Discard schemes that fail eligibility conditions
            if eval_res["status"] == EligibilityStatus.LIKELY_DOES_NOT_MATCH:
                continue

            s_copy = dict(s)
            s_copy["eligibility_status"] = eval_res["status"]
            s_copy["match_score"] = eval_res["confidence_score"]
            s_copy["match_label"] = eval_res["status"]
            s_copy["evidence"] = eval_res["evidence"]
            s_copy["missing_criteria"] = eval_res["missing_criteria"]
            s_copy["conflicts"] = eval_res["conflicts"]
            s_copy["rule_breakdown"] = eval_res["rule_breakdown"]
            evaluated_results.append(s_copy)

        # Sort: Potential Match first, then by match_score descending, then benefit_value
        evaluated_results.sort(
            key=lambda x: (
                1 if x["eligibility_status"] == EligibilityStatus.POTENTIAL_MATCH else 0,
                x["match_score"],
                x.get("benefit_value", 0)
            ),
            reverse=True
        )

        if len(evaluated_results) == 0:
            return jsonify({
                "status": "success",
                "count": 0,
                "message": "No relevant schemes were found with the current information.",
                "refinement_suggestions": [
                    "Verify if your annual family income limit is entered accurately.",
                    "Check Central Government (Pan-India) programs open to all States.",
                    "Review occupational category or explore general citizen welfare benefits."
                ],
                "user_profile": user_profile,
                "results": [],
                "disclaimer": Config.DISCLAIMER
            }), 200

        return jsonify({
            "status": "success",
            "count": len(evaluated_results),
            "user_profile": user_profile,
            "results": evaluated_results,
            "disclaimer": Config.DISCLAIMER
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Error while evaluating eligibility rules.",
            "detail": str(e)
        }), 500


@schemes_bp.route('/assistant', methods=['POST'])
def assistant_chat():
    """
    Multilingual conversational AI assistant endpoint.
    Handles intent detection, progressive clarification, fact extraction,
    and deterministic database scheme matching.
    """
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request payload must be formatted as application/json."
        }), 400

    data = request.get_json() or {}
    message = str(data.get('message', '')).strip()
    session_id = data.get('session_id')
    current_profile = data.get('current_profile')
    language = str(data.get('language', 'en')).strip().lower()
    selected_scheme_id = data.get('selected_scheme_id')

    if not message:
        return jsonify({
            "status": "error",
            "message": "Field 'message' cannot be empty."
        }), 400

    try:
        result = process_chat_message(
            message=message,
            session_id=session_id,
            current_profile=current_profile,
            language=language,
            selected_scheme_id=selected_scheme_id
        )
        result["disclaimer"] = Config.DISCLAIMER
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Conversation intelligence engine error.",
            "detail": str(e)
        }), 500


@schemes_bp.route('/assistant/clear', methods=['POST'])
def clear_assistant_session():
    """
    Reset conversation profile and message history for a given session.
    """
    try:
        data = request.get_json(silent=True) or {}
        session_id = data.get('session_id')
        if session_id:
            clear_session(session_id)
        return jsonify({
            "status": "success",
            "message": "Assistant session conversation memory cleared successfully."
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to clear assistant session.",
            "detail": str(e)
        }), 500


@schemes_bp.route('/assistant/status', methods=['GET'])
def get_assistant_status():
    """
    Return whether a live AI provider (Gemini or OpenAI) is active or running offline engine.
    """
    try:
        from ..ai_connector import get_ai_config
        return jsonify({
            "status": "success",
            "ai_status": get_ai_config()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to query AI configuration status.",
            "detail": str(e)
        }), 500


def stream_tts_audio():
    """
    Stream synthesized neural TTS audio for the given text and language (Telugu, Hindi, English).
    Used as an authentic fallback when client browser lacks native Indic speech packs.
    """
    text = request.args.get('text', '').strip()
    lang = request.args.get('lang', 'te').strip().lower()

    if not text:
        return jsonify({
            "status": "error",
            "message": "Query parameter 'text' is required."
        }), 400

    try:
        from ..tts_engine import synthesize_speech
        audio_bytes = synthesize_speech(text, lang=lang)
        if not audio_bytes:
            return jsonify({
                "status": "error",
                "message": f"TTS synthesis unavailable for language '{lang}'. Please install device speech pack."
            }), 503

        from flask import Response
        return Response(
            audio_bytes,
            mimetype="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=speech.mp3",
                "Cache-Control": "public, max-age=86400",
                "Access-Control-Allow-Origin": "*"
            }
        )
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "TTS streaming service error.",
            "detail": str(e)
        }), 500


def speak_tts_audio():
    """
    Synthesize audio and return metadata and stream URL.
    """
    data = request.get_json(silent=True) or {}
    text = str(data.get('text', '')).strip()
    lang = str(data.get('lang', 'te')).strip().lower()

    if not text:
        return jsonify({
            "status": "error",
            "message": "Field 'text' is required in JSON payload."
        }), 400

    import urllib.parse
    stream_url = f"/api/tts/stream?text={urllib.parse.quote(text)}&lang={urllib.parse.quote(lang)}"
    return jsonify({
        "status": "success",
        "lang": lang,
        "stream_url": stream_url
    }), 200


