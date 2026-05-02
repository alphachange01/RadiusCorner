import cv2
import numpy as np

class ShapeEngine:

    @staticmethod
    def squircle_mask(w, h):
        mask = np.zeros((h, w), dtype=np.uint8)

        cv2.ellipse(
            mask,
            (w // 2, h // 2),
            (w // 2 - 10, h // 2 - 10),
            0,
            0,
            360,
            255,
            -1
        )

        return cv2.GaussianBlur(mask, (7, 7), 0)
