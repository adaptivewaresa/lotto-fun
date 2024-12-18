from flask import Flask
from app.routes import api_bp


def create_app():
    """Application factory."""
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(api_bp)

    return app
