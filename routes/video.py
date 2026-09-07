import os
import uuid

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from werkzeug.utils import secure_filename

from services.video_processor import (
    VideoProcessor
)


video_bp = Blueprint(
    "video",
    __name__,
    url_prefix="/video"
)


def allowed_file(filename):

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = (
        filename.rsplit(
            ".",
            1
        )[1]
        .lower()
    )

    return (
        extension
        in current_app.config[
            "ALLOWED_VIDEO_EXTENSIONS"
        ]
    )


@video_bp.route(
    "/analysis",
    methods=["GET", "POST"]
)
def analysis():

    result = None

    if request.method == "POST":

        video = request.files.get(
            "video"
        )

        camera_number = (
            request.form.get(
                "camera_number"
            )
            or current_app.config[
                "DEFAULT_CAMERA_NUMBER"
            ]
        )

        location = (
            request.form.get(
                "location"
            )
            or current_app.config[
                "DEFAULT_LOCATION"
            ]
        )

        if not video:

            flash(
                "Please select a video.",
                "danger"
            )

            return redirect(
                url_for(
                    "video.analysis"
                )
            )

        if not video.filename:

            flash(
                "No video selected.",
                "danger"
            )

            return redirect(
                url_for(
                    "video.analysis"
                )
            )

        if not allowed_file(
            video.filename
        ):

            flash(
                "Unsupported video format.",
                "danger"
            )

            return redirect(
                url_for(
                    "video.analysis"
                )
            )

        original_name = (
            secure_filename(
                video.filename
            )
        )

        unique_name = (
            f"{uuid.uuid4().hex}_"
            f"{original_name}"
        )

        upload_folder = (
            current_app.config[
                "UPLOAD_FOLDER"
            ]
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        save_path = os.path.join(
            upload_folder,
            unique_name
        )

        try:

            video.save(
                save_path
            )

            print(
                f"[UPLOAD] Video saved:"
                f"\n{save_path}"
            )

            processor = (
                VideoProcessor()
            )

            result = (
                processor.process_video(
                    save_path,
                    camera_number,
                    location
                )
            )

            if result.get(
                "success"
            ):

                saved = result.get(
                    "detections_saved",
                    0
                )

                flash(
                    f"Analysis completed. "
                    f"{saved} detection(s) saved.",
                    "success"
                )

            else:

                flash(
                    result.get(
                        "error",
                        "Video processing failed."
                    ),
                    "danger"
                )

        except Exception as exc:

            print(
                "[ERROR] Video route failed:"
            )

            print(exc)

            result = {
                "success": False,
                "error": str(exc)
            }

            flash(
                f"Processing error: {exc}",
                "danger"
            )

    return render_template(
        "analysis.html",
        result=result
    )