from flask import (
    Blueprint,
    render_template
)

from database.database import db
from database.models import Detection


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def dashboard():

    total_detections = (
        Detection.query.count()
    )

    unique_plates = (
        db.session.query(
            Detection.plate_number
        )
        .distinct()
        .count()
    )

    vehicle_counts = {}

    detections = (
        Detection.query.all()
    )

    for detection in detections:

        vehicle_type = (
            detection.vehicle_type
        )

        vehicle_counts[
            vehicle_type
        ] = (
            vehicle_counts.get(
                vehicle_type,
                0
            ) + 1
        )

    recent_detections = (
        Detection.query
        .order_by(
            Detection.timestamp.desc()
        )
        .limit(10)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_detections=total_detections,
        unique_plates=unique_plates,
        vehicle_counts=vehicle_counts,
        recent_detections=recent_detections
    )