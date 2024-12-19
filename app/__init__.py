from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config')
    
    # Register routes and services
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
