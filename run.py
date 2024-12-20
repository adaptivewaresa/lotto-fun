from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from services import refresh_frequency_cache_task

def create_app():
    app = Flask(__name__)

    # Scheduler setup
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        refresh_frequency_cache_task,
        'interval',
        hours=24,  # Run every 24 hours
        next_run_time=None  # Start immediately
    )
    scheduler.start()

    # Register scheduler lifecycle hooks
    @app.before_first_request
    def start_scheduler():
        if not scheduler.running:
            scheduler.start()

    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        if scheduler.running:
            scheduler.shutdown()

    return app

# Initialize and run the app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
