import numpy as np
import cv2

class ShapeEngine:

    @staticmethod
    def squircle_mask(w, h, radius=100):
        mask = np.zeros((h, w), dtype=np.uint8)

        r = max(1, min(radius, min(w, h)//2 - 5))

        # rounded corners logic
        rect = np.zeros((h, w), dtype=np.uint8)
        cv2.rectangle(rect, (r, r), (w-r, h-r), 255, -1)

        cv2.circle(rect, (r, r), r, 255, -1)
        cv2.circle(rect, (w-r, r), r, 255, -1)
        cv2.circle(rect, (r, h-r), r, 255, -1)
        cv2.circle(rect, (w-r, h-r), r, 255, -1)

        mask = cv2.GaussianBlur(rect, (7, 7), 0)

        return mask
