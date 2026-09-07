import os
import torch

from ultralytics import YOLO

from config import Config


class PlateDetector:

    def __init__(self):

        self.model = None

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model_path = Config.PLATE_MODEL_PATH

        self.load_model()


    def load_model(self):

        print("\n" + "=" * 50)
        print("PLATE DETECTOR")
        print("=" * 50)

        print(f"[MODEL] Path: {self.model_path}")
        print(f"[MODEL] Exists: {os.path.exists(self.model_path)}")


        if not os.path.exists(self.model_path):

            print(
                "[ERROR] Plate model file does not exist."
            )

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
                    "Plate model file is empty or too small."
                )


            self.model = YOLO(
                self.model_path
            )


            print(
                "[SUCCESS] Plate model loaded."
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
                "[ERROR] Plate model loading failed:"
            )

            print(
                f"        {type(exc).__name__}: {exc}"
            )

            print(
                "[FIX] Replace plate_model.pt with "
                "a valid YOLO plate-detection model."
            )

            self.model = None


        print("=" * 50 + "\n")


    def is_available(self):

        return self.model is not None


    def detect(self, vehicle_crop):

        if self.model is None:

            return []


        if vehicle_crop is None:

            return []


        if vehicle_crop.size == 0:

            return []


        try:

            results = self.model.predict(

                source=vehicle_crop,

                conf=Config.PLATE_CONFIDENCE_THRESHOLD,

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


                    x1, y1, x2, y2 = map(

                        int,

                        box.xyxy[0].tolist()

                    )


                    detections.append({

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
                f"[ERROR] Plate detection failed: {exc}"
            )

            return []
