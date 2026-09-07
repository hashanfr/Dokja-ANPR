import os
import time
from datetime import datetime

import cv2

from config import Config
from services.vehicle_detector import VehicleDetector
from services.plate_detector import PlateDetector
from services.ocr_engine import OCREngine
from services.detection_manager import DetectionManager


class VideoProcessor:

    def __init__(self):

        print(
            "\n"
            "========================================"
        )

        print(
            "DOK-ANPR VIDEO PROCESSOR"
        )

        print(
            "========================================"
        )

        self.vehicle_detector = (
            VehicleDetector()
        )

        self.plate_detector = (
            PlateDetector()
        )

        self.ocr_engine = (
            OCREngine()
        )

        self.detection_manager = (
            DetectionManager()
        )

    def save_snapshot(
        self,
        frame,
        plate_bbox,
        frame_number
    ):

        try:

            os.makedirs(
                Config.SNAPSHOT_FOLDER,
                exist_ok=True
            )

            filename = (
                f"detection_"
                f"{int(time.time() * 1000)}_"
                f"{frame_number}.jpg"
            )

            full_path = os.path.join(
                Config.SNAPSHOT_FOLDER,
                filename
            )

            x1, y1, x2, y2 = (
                plate_bbox
            )

            height, width = (
                frame.shape[:2]
            )

            x1 = max(
                0,
                min(x1, width)
            )

            y1 = max(
                0,
                min(y1, height)
            )

            x2 = max(
                0,
                min(x2, width)
            )

            y2 = max(
                0,
                min(y2, height)
            )

            if x2 <= x1 or y2 <= y1:

                crop = frame

            else:

                crop = frame[
                    y1:y2,
                    x1:x2
                ]

            cv2.imwrite(
                full_path,
                crop
            )

            # Store web-accessible relative path
            return os.path.join(
                "snapshots",
                filename
            ).replace("\\", "/")

        except Exception as exc:

            print(
                f"[WARNING] Snapshot failed: "
                f"{exc}"
            )

            return None

    def process_video(
        self,
        video_path,
        camera_number,
        location
    ):

        if not os.path.exists(
            video_path
        ):

            return {
                "success": False,
                "error": "Video file does not exist."
            }

        capture = cv2.VideoCapture(
            video_path
        )

        if not capture.isOpened():

            return {
                "success": False,
                "error": (
                    "Unable to open video. "
                    "Check the video format."
                )
            }

        fps = capture.get(
            cv2.CAP_PROP_FPS
        )

        total_frames = int(
            capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        if fps <= 0:
            fps = 25

        duration = (
            total_frames / fps
            if total_frames > 0
            else 0
        )

        frame_number = 0
        processed_frames = 0

        vehicle_detections_total = 0
        plate_detections_total = 0
        ocr_success_total = 0
        database_saved_total = 0

        start_time = time.time()

        print(
            f"[VIDEO] Processing: "
            f"{video_path}"
        )

        print(
            f"[VIDEO] FPS: {fps:.2f}"
        )

        print(
            f"[VIDEO] Frames: "
            f"{total_frames}"
        )

        print(
            f"[VIDEO] Duration: "
            f"{duration:.2f}s"
        )

        print(
            "----------------------------------------"
        )

        while True:

            success, frame = (
                capture.read()
            )

            if not success:
                break

            frame_number += 1

            # Skip frames to speed processing
            if (
                frame_number
                % Config.FRAME_SKIP
                != 0
            ):
                continue

            processed_frames += 1

            # Video timestamp
            video_time_seconds = (
                frame_number / fps
            )

            # --------------------------------------------------
            # VEHICLE DETECTION
            # --------------------------------------------------

            vehicles = (
                self.vehicle_detector.detect(
                    frame
                )
            )

            vehicle_detections_total += (
                len(vehicles)
            )

            if vehicles:

                print(
                    f"[FRAME {frame_number}] "
                    f"Vehicles: {len(vehicles)}"
                )

            # --------------------------------------------------
            # PROCESS EACH VEHICLE
            # --------------------------------------------------

            for vehicle in vehicles:

                x1, y1, x2, y2 = (
                    vehicle["bbox"]
                )

                height, width = (
                    frame.shape[:2]
                )

                x1 = max(
                    0,
                    min(x1, width - 1)
                )

                y1 = max(
                    0,
                    min(y1, height - 1)
                )

                x2 = max(
                    0,
                    min(x2, width)
                )

                y2 = max(
                    0,
                    min(y2, height)
                )

                if (
                    x2 <= x1
                    or y2 <= y1
                ):
                    continue

                vehicle_crop = frame[
                    y1:y2,
                    x1:x2
                ]

                if (
                    vehicle_crop.size
                    == 0
                ):
                    continue

                # --------------------------------------------------
                # PLATE DETECTION
                # --------------------------------------------------

                plates = (
                    self.plate_detector.detect(
                        vehicle_crop
                    )
                )

                plate_detections_total += (
                    len(plates)
                )

                for plate in plates:

                    px1, py1, px2, py2 = (
                        plate["bbox"]
                    )

                    crop_height, crop_width = (
                        vehicle_crop.shape[:2]
                    )

                    px1 = max(
                        0,
                        min(
                            px1,
                            crop_width - 1
                        )
                    )

                    py1 = max(
                        0,
                        min(
                            py1,
                            crop_height - 1
                        )
                    )

                    px2 = max(
                        0,
                        min(
                            px2,
                            crop_width
                        )
                    )

                    py2 = max(
                        0,
                        min(
                            py2,
                            crop_height
                        )
                    )

                    if (
                        px2 <= px1
                        or py2 <= py1
                    ):
                        continue

                    plate_crop = (
                        vehicle_crop[
                            py1:py2,
                            px1:px2
                        ]
                    )

                    if (
                        plate_crop.size
                        == 0
                    ):
                        continue

                    # --------------------------------------------------
                    # OCR
                    # --------------------------------------------------

                    ocr_result = (
                        self.ocr_engine.read_plate(
                            plate_crop
                        )
                    )

                    if not ocr_result:

                        print(
                            f"[OCR] No readable "
                            f"plate at frame "
                            f"{frame_number}"
                        )

                        continue

                    ocr_success_total += 1

                    plate_number = (
                        ocr_result[
                            "plate_number"
                        ]
                    )

                    print(
                        f"[OCR] "
                        f"{plate_number} "
                        f"({ocr_result['confidence']:.2f})"
                    )

                    # Convert plate bbox back
                    # to original frame coordinates
                    absolute_plate_bbox = (
                        x1 + px1,
                        y1 + py1,
                        x1 + px2,
                        y1 + py2
                    )

                    snapshot_path = (
                        self.save_snapshot(
                            frame,
                            absolute_plate_bbox,
                            frame_number
                        )
                    )

                    # Timestamp based on video position
                    detection_time = (
                        datetime.utcnow()
                    )

                    # --------------------------------------------------
                    # SAVE DATABASE RECORD
                    # --------------------------------------------------

                    saved = (
                        self.detection_manager
                        .save_detection(
                            plate_number=plate_number,
                            vehicle_type=vehicle[
                                "vehicle_type"
                            ],
                            camera_number=(
                                camera_number
                            ),
                            location=location,
                            vehicle_confidence=(
                                vehicle[
                                    "confidence"
                                ]
                            ),
                            plate_confidence=(
                                ocr_result[
                                    "confidence"
                                ]
                            ),
                            snapshot_path=(
                                snapshot_path
                            ),
                            video_source=(
                                video_path
                            ),
                            timestamp=(
                                detection_time
                            )
                        )
                    )

                    if saved:

                        database_saved_total += 1

                        print(
                            "[SUCCESS] Detection "
                            "saved to database."
                        )

            # Progress display
            if (
                frame_number % 100 == 0
            ):

                percentage = (
                    (
                        frame_number
                        / total_frames
                    )
                    * 100
                    if total_frames > 0
                    else 0
                )

                print(
                    f"[PROGRESS] "
                    f"{percentage:.1f}%"
                )

        capture.release()

        elapsed = (
            time.time()
            - start_time
        )

        processing_fps = (
            processed_frames / elapsed
            if elapsed > 0
            else 0
        )

        print(
            "========================================"
        )

        print(
            "VIDEO PROCESSING COMPLETE"
        )

        print(
            f"Frames processed: "
            f"{processed_frames}"
        )

        print(
            f"Vehicles detected: "
            f"{vehicle_detections_total}"
        )

        print(
            f"Plates detected: "
            f"{plate_detections_total}"
        )

        print(
            f"OCR successes: "
            f"{ocr_success_total}"
        )

        print(
            f"Database records: "
            f"{database_saved_total}"
        )

        print(
            "========================================"
        )

        return {
            "success": True,

            "frames_processed": (
                processed_frames
            ),

            "total_frames": (
                total_frames
            ),

            "duration": round(
                duration,
                2
            ),

            "vehicles_detected": (
                vehicle_detections_total
            ),

            "plates_detected": (
                plate_detections_total
            ),

            "ocr_successes": (
                ocr_success_total
            ),

            "detections_saved": (
                database_saved_total
            ),

            "processing_fps": round(
                processing_fps,
                2
            )
        }