from flask import (
    Blueprint,
    current_app,
    render_template,
    redirect,
    request,
    url_for
)

import os

from database.database import db
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


@detections_bp.route(
    "/<int:detection_id>/delete",
    methods=["POST"]
)
def delete_detection(
    detection_id
):

    detection = (
        Detection.query.get_or_404(
            detection_id
        )
    )

    if detection.snapshot_path:

        snapshot_path = os.path.join(
            current_app.static_folder,
            detection.snapshot_path
        )

        if os.path.isfile(snapshot_path):
            os.remove(snapshot_path)

    db.session.delete(detection)
    db.session.commit()

    return redirect(
        url_for(
            "detections.detections"
        )
    )


@detections_bp.route(
    "/delete-all",
    methods=["POST"]
)
def delete_all_detections():

    detections_list = (
        Detection.query.all()
    )

    for detection in detections_list:

        if not detection.snapshot_path:
            continue

        snapshot_path = os.path.join(
            current_app.static_folder,
            detection.snapshot_path
        )

        if os.path.isfile(snapshot_path):
            os.remove(snapshot_path)

    Detection.query.delete(
        synchronize_session=False
    )

    db.session.commit()

    return redirect(
        url_for(
            "detections.detections"
        )
    )