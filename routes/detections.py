from flask import (
    Blueprint,
    render_template,
    request
)

from database.models import Detection


detections_bp = Blueprint(
    "detections",
    __name__,
    url_prefix="/detections"
)


@detections_bp.route("/")
def detections():

    query = Detection.query

    search = (
        request.args.get(
            "search",
            ""
        )
        .strip()
    )

    vehicle_type = (
        request.args.get(
            "vehicle_type",
            ""
        )
        .strip()
    )

    camera = (
        request.args.get(
            "camera",
            ""
        )
        .strip()
    )

    if search:

        query = query.filter(
            Detection.plate_number.ilike(
                f"%{search}%"
            )
        )

    if vehicle_type:

        query = query.filter(
            Detection.vehicle_type
            == vehicle_type
        )

    if camera:

        query = query.filter(
            Detection.camera_number
            == camera
        )

    detections_list = (
        query
        .order_by(
            Detection.timestamp.desc()
        )
        .all()
    )

    return render_template(
        "detections.html",
        detections=detections_list,
        search=search,
        vehicle_type=vehicle_type,
        camera=camera
    )


@detections_bp.route(
    "/<int:detection_id>"
)
def vehicle_details(
    detection_id
):

    detection = (
        Detection.query.get_or_404(
            detection_id
        )
    )

    return render_template(
        "vehicle_details.html",
        detection=detection
    )