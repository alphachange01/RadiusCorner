import cv2
import numpy as np

class ShapeEngine:

    @staticmethod
    def squircle_mask(w, h, radius=30):
        mask = np.zeros((h, w), dtype=np.uint8)

        center = (w // 2, h // 2)
        axes = (w // 2 - 10, h // 2 - 10)

        cv2.ellipse(
            mask,
            center,
            axes,
            0,
            0,
            360,
            255,
            -1
        )

        mask = cv2.GaussianBlur(mask, (7, 7), 0)
        return mask

    @staticmethod
    def circle_mask(w, h):
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (w // 2, h // 2), min(w, h)//2 - 5, 255, -1)
        return cv2.GaussianBlur(mask, (7, 7), 0)
