import numpy as np
import cv2

class ShapeEngine:

    @staticmethod
    def squircle_mask(w, h):
        mask = np.zeros((h, w), dtype=np.uint8)

        cv2.rectangle(mask, (10, 10), (w-10, h-10), 255, -1)
        cv2.circle(mask, (w//2, h//2), min(w, h)//2 - 10, 255, -1)

        mask = cv2.GaussianBlur(mask, (9, 9), 0)

        return mask
