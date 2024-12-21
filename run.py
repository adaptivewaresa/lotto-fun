from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app.services import refresh_frequency_cache_task
from app.routes import api_bp  # Import the blueprint


def create_app():
    app = Flask(__name__)

    # Register the blueprint
    # Register API routes at the root "/"
    app.register_blueprint(api_bp, url_prefix="/")

    # Scheduler setup
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        refresh_frequency_cache_task,
        'interval',
        hours=24,  # Run every 24 hours
        next_run_time=None  # Start immediately
    )

    @app.before_request
    def start_scheduler():
        if not scheduler.running:
            scheduler.start()

    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        if scheduler.running:
            scheduler.shutdown()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
