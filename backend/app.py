"""
Flask Application Factory & Entry Point for Government Scheme Finder Backend.
Configures CORS, registers API Blueprints, serves frontend assets, and provides error handling.
"""
import os
from flask import Flask, jsonify, send_from_directory, request
from .config import Config
from .database import init_db
from .routes.schemes import schemes_bp


def create_app():
    """
    Application factory pattern to configure and return the Flask application.
    """
    app = Flask(__name__, static_folder=Config.FRONTEND_DIR)
    app.config.from_object(Config)

    # Initialize SQLite database schema and seed data
    init_db()

    # Register API blueprints
    app.register_blueprint(schemes_bp)

    # Enable CORS headers for all responses
    @app.after_request
    def set_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        return response

    # Preflight OPTIONS handler
    @app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
    @app.route('/<path:path>', methods=['OPTIONS'])
    def handle_options_preflight(path):
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        return response

    # API Health Check Endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "Government Scheme Finder REST API",
            "version": "1.0.0",
            "database": "SQLite",
            "disclaimer": Config.DISCLAIMER
        }), 200

    # Dedicated Assistant Chat Routes
    @app.route('/api/assistant/chat', methods=['POST'])
    def assistant_chat_route():
        from .routes.schemes import assistant_chat
        return assistant_chat()

    @app.route('/api/assistant/clear', methods=['POST'])
    def assistant_clear_route():
        from .routes.schemes import clear_assistant_session
        return clear_assistant_session()

    @app.route('/api/assistant/status', methods=['GET'])
    def assistant_status_route():
        from .routes.schemes import get_assistant_status
        return get_assistant_status()

    @app.route('/api/tts/stream', methods=['GET'])
    def tts_stream_route():
        from .routes.schemes import stream_tts_audio
        return stream_tts_audio()

    @app.route('/api/tts/speak', methods=['POST'])
    def tts_speak_route():
        from .routes.schemes import speak_tts_audio
        return speak_tts_audio()


    # Serve Frontend UI when opened from the backend server
    @app.route('/')
    def serve_frontend_index():
        if os.path.exists(os.path.join(Config.FRONTEND_DIR, 'index.html')):
            return send_from_directory(Config.FRONTEND_DIR, 'index.html')
        return jsonify({
            "status": "running",
            "message": "Government Scheme Finder API is active. Access frontend via static server or frontend/index.html."
        }), 200

    @app.route('/<path:filename>')
    def serve_frontend_static(filename):
        file_path = os.path.join(Config.FRONTEND_DIR, filename)
        if os.path.exists(file_path):
            return send_from_directory(Config.FRONTEND_DIR, filename)
        return jsonify({
            "status": "error",
            "message": f"Resource '{filename}' not found."
        }), 404

    # Global Error Handlers
    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({
            "status": "error",
            "code": 400,
            "message": "Bad request. Please verify the request parameters or JSON payload."
        }), 400

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            "status": "error",
            "code": 404,
            "message": "The requested API endpoint or resource was not found."
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({
            "status": "error",
            "code": 405,
            "message": "HTTP method not allowed for this endpoint."
        }), 405

    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please check server logs."
        }), 500

    return app


if __name__ == '__main__':
    app = create_app()
    print(f"Starting Government Scheme Finder Backend on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
