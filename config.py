import os


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


class Config:

    SECRET_KEY = "dokja-anpr-secret-key"

    # --------------------------------------------------
    # DATABASE
    # --------------------------------------------------

    DATA_FOLDER = os.path.join(
        BASE_DIR,
        "data"
    )

    DATABASE_PATH = os.path.join(
        DATA_FOLDER,
        "anpr.db"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        + DATABASE_PATH.replace("\\", "/")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --------------------------------------------------
    # UPLOADS
    # --------------------------------------------------

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    SNAPSHOT_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "snapshots"
    )

    ALLOWED_VIDEO_EXTENSIONS = {
        "mp4",
        "avi",
        "mov",
        "mkv",
        "webm"
    }

    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024

    # --------------------------------------------------
    # MODELS
    # --------------------------------------------------

    VEHICLE_MODEL_PATH = os.path.join(
        BASE_DIR,
        "models",
        "vehicle",
        "vehicle_model.pt"
    )

    PLATE_MODEL_PATH = os.path.join(
        BASE_DIR,
        "models",
        "plate",
        "plate_model.pt"
    )

    # --------------------------------------------------
    # AI SETTINGS
    # --------------------------------------------------

    VEHICLE_CONFIDENCE_THRESHOLD = 0.25

    PLATE_CONFIDENCE_THRESHOLD = 0.20

    OCR_CONFIDENCE_THRESHOLD = 0.25

    # Process every Nth frame.
    # 1 = every frame
    # 2 = every second frame
    FRAME_SKIP = 2

    # --------------------------------------------------
    # DUPLICATE CONTROL
    # --------------------------------------------------

    DUPLICATE_INTERVAL_SECONDS = 5

    # --------------------------------------------------
    # DEFAULT CAMERA
    # --------------------------------------------------

    DEFAULT_CAMERA_NUMBER = "CAM-01"

    DEFAULT_LOCATION = "Unknown Location"