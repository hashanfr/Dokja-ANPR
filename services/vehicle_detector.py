import os
import torch
from ultralytics import YOLO

from config import Config


class VehicleDetector:

    def __init__(self):

        self.model = None

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model_path = Config.VEHICLE_MODEL_PATH

        self.class_mapping = {
            "car": "Car",
            "motorcycle": "Bike",
            "motorbike": "Bike",
            "bus": "Bus",
            "truck": "Truck",
            "van": "Van",
            "bicycle": "Bike",
        }

        self.load_model()


    def load_model(self):

        print("\n" + "=" * 50)
        print("VEHICLE DETECTOR")
        print("=" * 50)

        print(f"[MODEL] Path: {self.model_path}")
        print(f"[MODEL] Exists: {os.path.exists(self.model_path)}")

        if not os.path.exists(self.model_path):

            print("[ERROR] Vehicle model file does not exist.")

            self.model = None
            return


        try:

            file_size = os.path.getsize(
                self.model_path
            )

            print(
                f"[MODEL] File size: "
                f"{file_size / (1024 * 1024):.2f} MB"
            )


            if file_size < 1024:

                raise ValueError(
                    "Vehicle model file is empty or too small."
                )


            self.model = YOLO(
                self.model_path
            )


            print(
                "[SUCCESS] Vehicle model loaded."
            )

            print(
                f"[DEVICE] {self.device}"
            )


            if hasattr(self.model, "names"):

                print(
                    f"[CLASSES] {self.model.names}"
                )


        except Exception as exc:

            print(
                "[ERROR] Vehicle model loading failed:"
            )

            print(
                f"        {type(exc).__name__}: {exc}"
            )

            print(
                "[FIX] Replace vehicle_model.pt with "
                "a valid YOLO .pt model."
            )

            self.model = None


        print("=" * 50 + "\n")


    def is_available(self):

        return self.model is not None


    def detect(self, frame):

        if self.model is None:

            return []


        if frame is None:

            return []


        try:

            results = self.model.predict(

                source=frame,

                conf=Config.VEHICLE_CONFIDENCE_THRESHOLD,

                device=self.device,

                verbose=False

            )


            detections = []


            for result in results:

                if result.boxes is None:
                    continue


                for box in result.boxes:

                    confidence = float(
                        box.conf[0].item()
                    )


                    class_id = int(
                        box.cls[0].item()
                    )


                    class_name = result.names.get(
                        class_id,
                        "Other"
                    )


                    normalized_type = (
                        self.class_mapping.get(
                            class_name.lower(),
                            "Other"
                        )
                    )


                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0].tolist()
                    )


                    detections.append({

                        "vehicle_type":
                            normalized_type,

                        "confidence":
                            confidence,

                        "bbox": (
                            x1,
                            y1,
                            x2,
                            y2
                        )

                    })


            return detections


        except Exception as exc:

            print(
                f"[ERROR] Vehicle detection failed: {exc}"
            )

            return []


    def get_device_name(self):

        if self.device == "cuda":

            try:

                return torch.cuda.get_device_name(0)

            except Exception:

                return "NVIDIA GPU"


        return "CPU"

