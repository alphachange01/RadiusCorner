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

        # alpha fix
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

        # SAFE ZOOM (kesilmasin)
        scale = 0.85
        nw = int(w * scale)
        nh = int(h * scale)

        resized = cv2.resize(img, (nw, nh), cv2.INTER_AREA)

        canvas = np.zeros((h, w, 4), dtype=np.uint8)

        x = (w - nw) // 2
        y = (h - nh) // 2

        canvas[y:y+nh, x:x+nw] = resized

        # SQUIRCLE MASK
        mask = ShapeEngine.squircle_mask(w, h)

        canvas[:, :, 3] = mask

        output = "temp/output.png"
        cv2.imwrite(output, canvas)

        return output
