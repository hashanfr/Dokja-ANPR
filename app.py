import os

from flask import Flask

from config import Config
from database.database import db

from routes.dashboard import dashboard_bp
from routes.video import video_bp
from routes.detections import detections_bp
from routes.analytics import analytics_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

                         
    db.init_app(app)

                         
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(detections_bp)
    app.register_blueprint(analytics_bp)

                                 
    with app.app_context():
        from database.models import Detection
        db.create_all()

    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.SNAPSHOT_FOLDER, exist_ok=True)
    os.makedirs(Config.DATA_FOLDER, exist_ok=True)

    return app


app = create_app()


if __name__ == "__main__":
    print("=" * 60)
    print("        DOK-ANPR | AI VEHICLE MONITORING SYSTEM")
    print("=" * 60)
    print("Server: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server.")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )