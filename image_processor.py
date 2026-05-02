import cv2
import numpy as np
from shape_engine import ShapeEngine

class ImageProcessor:

    @staticmethod
    def process(image_path):
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        if img is None:
            raise Exception("Image not loaded")

        h, w = img.shape[:2]

        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

        # 🔥 SAFE ZOOM FIX (MUHIM)
        scale = 0.85
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized = cv2.resize(img, (new_w, new_h), cv2.INTER_AREA)

        canvas = np.zeros((h, w, 4), dtype=np.uint8)

        x = (w - new_w) // 2
        y = (h - new_h) // 2

        canvas[y:y+new_h, x:x+new_w] = resized

        # mask
        mask = ShapeEngine.squircle_mask(w, h)
        canvas[:, :, 3] = mask

        output = "temp/output.png"
        cv2.imwrite(output, canvas)

        return output
