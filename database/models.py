from datetime import datetime

from database.database import db


class Detection(db.Model):

    __tablename__ = "detections"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    plate_number = db.Column(
        db.String(32),
        nullable=False,
        index=True
    )

    vehicle_type = db.Column(
        db.String(32),
        nullable=False,
        default="Unknown"
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )

    camera_number = db.Column(
        db.String(64),
        nullable=False,
        default="CAM-01"
    )

    location = db.Column(
        db.String(255),
        nullable=False,
        default="Unknown Location"
    )

    vehicle_confidence = db.Column(
        db.Float,
        nullable=True
    )

    plate_confidence = db.Column(
        db.Float,
        nullable=True
    )

    snapshot_path = db.Column(
        db.String(500),
        nullable=True
    )

    video_source = db.Column(
        db.String(500),
        nullable=True
    )

    def __repr__(self):

        return (
            f"<Detection "
            f"{self.plate_number} "
            f"{self.vehicle_type}>"
        )