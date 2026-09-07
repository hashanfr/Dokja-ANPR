from datetime import datetime

from config import Config
from database.database import db
from database.models import Detection


class DetectionManager:

    def __init__(self):

        self.last_detections = {}

    def normalize_plate(
        self,
        plate_number
    ):

        if not plate_number:
            return ""

        return (
            str(plate_number)
            .upper()
            .replace(" ", "")
            .strip()
        )

    def is_duplicate(
        self,
        plate_number,
        camera_number
    ):

        plate_number = (
            self.normalize_plate(
                plate_number
            )
        )

        key = (
            plate_number,
            str(camera_number)
        )

        last_time = (
            self.last_detections.get(
                key
            )
        )

        if last_time is None:
            return False

        elapsed = (
            datetime.utcnow()
            - last_time
        ).total_seconds()

        return (
            elapsed
            < Config.DUPLICATE_INTERVAL_SECONDS
        )

    def register_detection(
        self,
        plate_number,
        camera_number
    ):

        key = (
            self.normalize_plate(
                plate_number
            ),
            str(camera_number)
        )

        self.last_detections[key] = (
            datetime.utcnow()
        )

    def save_detection(
        self,
        plate_number,
        vehicle_type,
        camera_number,
        location,
        vehicle_confidence,
        plate_confidence,
        snapshot_path=None,
        video_source=None,
        timestamp=None
    ):

        plate_number = (
            self.normalize_plate(
                plate_number
            )
        )

        if not plate_number:
            return None

        if self.is_duplicate(
            plate_number,
            camera_number
        ):

            return None

        detection = Detection(
            plate_number=plate_number,
            vehicle_type=(
                vehicle_type
                or "Unknown"
            ),
            timestamp=(
                timestamp
                or datetime.utcnow()
            ),
            camera_number=(
                camera_number
                or "CAM-01"
            ),
            location=(
                location
                or "Unknown Location"
            ),
            vehicle_confidence=(
                vehicle_confidence
            ),
            plate_confidence=(
                plate_confidence
            ),
            snapshot_path=snapshot_path,
            video_source=video_source
        )

        try:

            db.session.add(
                detection
            )

            db.session.commit()

            self.register_detection(
                plate_number,
                camera_number
            )

            print(
                f"[DATABASE] Saved detection: "
                f"{plate_number}"
            )

            return detection

        except Exception as exc:

            db.session.rollback()

            print(
                "[ERROR] Database save failed:"
            )

            print(exc)

            return None