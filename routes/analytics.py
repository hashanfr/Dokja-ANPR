from flask import (
    Blueprint,
    jsonify,
    render_template
)

from database.database import db
from database.models import Detection


analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics"
)


@analytics_bp.route("/")
def analytics():

    total = Detection.query.count()

    unique_plates = (
        db.session.query(
            Detection.plate_number
        )
        .distinct()
        .count()
    )

    vehicle_distribution = {}

    detections = (
        Detection.query.all()
    )

    for detection in detections:

        vehicle_type = (
            detection.vehicle_type
        )

        vehicle_distribution[
            vehicle_type
        ] = (
            vehicle_distribution.get(
                vehicle_type,
                0
            ) + 1
        )

    most_detected = None

    if vehicle_distribution:

        most_detected = max(
            vehicle_distribution,
            key=vehicle_distribution.get
        )

    return render_template(
        "analytics.html",
        total=total,
        unique_plates=unique_plates,
        vehicle_distribution=(
            vehicle_distribution
        ),
        most_detected=most_detected
    )


@analytics_bp.route(
    "/api/summary"
)
def analytics_summary():

    total = Detection.query.count()

    unique_plates = (
        db.session.query(
            Detection.plate_number
        )
        .distinct()
        .count()
    )

    distribution = {}

    for detection in (
        Detection.query.all()
    ):

        vehicle_type = (
            detection.vehicle_type
        )

        distribution[
            vehicle_type
        ] = (
            distribution.get(
                vehicle_type,
                0
            ) + 1
        )

    return jsonify({
        "total_detections": total,
        "unique_plates": unique_plates,
        "vehicle_distribution": distribution
    })