import re

import cv2

from config import Config


class OCREngine:

    def __init__(self):

        self.reader = None

        try:

            import easyocr

            print(
                "[INFO] Loading EasyOCR..."
            )

            self.reader = easyocr.Reader(
                ["en"],
                gpu=False
            )

            print(
                "[INFO] EasyOCR ready."
            )

        except Exception as exc:

            print(
                f"[ERROR] EasyOCR unavailable: "
                f"{exc}"
            )

    def is_available(self):

        return self.reader is not None

    def clean_text(self, text):

        if not text:
            return ""

        text = str(text).upper()

        text = re.sub(
            r"[^A-Z0-9]",
            "",
            text
        )

        return text

    def enhance_plate_image(
        self,
        plate_image
    ):

        if (
            plate_image is None
            or plate_image.size == 0
        ):

            return None

        height, width = (
            plate_image.shape[:2]
        )

        scale = Config.PLATE_IMAGE_SCALE

        resized = cv2.resize(
            plate_image,
            (
                max(1, width * scale),
                max(1, height * scale)
            ),
            interpolation=cv2.INTER_CUBIC
        )

        denoised = cv2.bilateralFilter(
            resized,
            7,
            45,
            45
        )

        gray = cv2.cvtColor(
            denoised,
            cv2.COLOR_BGR2GRAY
        )

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        contrast = clahe.apply(gray)

        blurred = cv2.GaussianBlur(
            contrast,
            (0, 0),
            1.2
        )

        sharpened = cv2.addWeighted(
            contrast,
            1.6,
            blurred,
            -0.6,
            0
        )

        return cv2.cvtColor(
            sharpened,
            cv2.COLOR_GRAY2BGR
        )

    def preprocess_variants(
        self,
        plate_image
    ):

        if (
            plate_image is None
            or plate_image.size == 0
        ):

            return []

        resized = self.enhance_plate_image(
            plate_image
        )

        if resized is None:
            return []

        gray = cv2.cvtColor(
            resized,
            cv2.COLOR_BGR2GRAY
        )

                   
        normal = gray

                                                                  
        enhanced = gray

                   
        _, binary = cv2.threshold(
            enhanced,
            0,
            255,
            cv2.THRESH_BINARY
            + cv2.THRESH_OTSU
        )

                   
        adaptive = cv2.adaptiveThreshold(
            enhanced,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        return [
            resized,
            normal,
            enhanced,
            binary,
            adaptive
        ]

    def looks_like_plate(
        self,
        text
    ):

        if not text:
            return False

        if len(text) < 5:
            return False

        if len(text) > 12:
            return False

                                          
        has_letter = bool(
            re.search(
                r"[A-Z]",
                text
            )
        )

        has_number = bool(
            re.search(
                r"[0-9]",
                text
            )
        )

        if not (
            has_letter
            and has_number
        ):
            return False

                                   
        indian_pattern = (
            r"^[A-Z]{2}"
            r"[0-9]{1,2}"
            r"[A-Z]{1,3}"
            r"[0-9]{3,4}$"
        )

        if re.match(
            indian_pattern,
            text
        ):

            return True

                                
        return (
            len(text) >= 6
            and len(text) <= 10
        )

    def read_plate(
        self,
        plate_image
    ):

        if not self.is_available():

            return None

        variants = (
            self.preprocess_variants(
                plate_image
            )
        )

        if not variants:
            return None

        candidates = []

        try:

            for image in variants:

                results = (
                    self.reader.readtext(
                        image,
                        detail=1,
                        paragraph=False,
                        allowlist=(
                            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            "0123456789"
                        )
                    )
                )

                for result in results:

                    if len(result) < 3:
                        continue

                    raw_text = result[1]

                    confidence = float(
                        result[2]
                    )

                    cleaned = (
                        self.clean_text(
                            raw_text
                        )
                    )

                    if not cleaned:
                        continue

                    candidates.append({
                        "plate_number": cleaned,
                        "confidence": confidence
                    })

            if not candidates:
                return None

                                              
                                  
            valid = [
                item
                for item in candidates
                if self.looks_like_plate(
                    item["plate_number"]
                )
            ]

            if valid:

                valid.sort(
                    key=lambda x: x[
                        "confidence"
                    ],
                    reverse=True
                )

                best = valid[0]

            else:

                candidates.sort(
                    key=lambda x: x[
                        "confidence"
                    ],
                    reverse=True
                )

                best = candidates[0]

            if (
                best["confidence"]
                < Config.OCR_CONFIDENCE_THRESHOLD
            ):

                return None

            return best

        except Exception as exc:

            print(
                f"[ERROR] OCR failed: {exc}"
            )

            return None