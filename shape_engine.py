import cv2
import numpy as np
import os

def apply_radius(path, value):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ValueError("Image not found")

    h, w = img.shape[:2]
    size = max(w, h)

    v = max(50, min(int(value), 200))
    t = (v - 50) / 150  # 0 → 1

    radius = int((size // 2) * t)

    # create square canvas
    canvas = np.zeros((size, size, 4), dtype=np.uint8)

    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    x = (size - w) // 2
    y = (size - h) // 2
    canvas[y:y+h, x:x+w] = img

    # mask
    mask = np.zeros((size, size), dtype=np.uint8)

    # base square
    mask[:] = 255

    # smooth corners (important part)
    if radius > 0:
        k = radius if radius % 2 == 1 else radius + 1
        mask = cv2.GaussianBlur(mask, (k, k), 0)

    result = cv2.bitwise_and(canvas, canvas, mask=mask)

    out = path.replace(".png", f"_{value}.png")
    cv2.imwrite(out, result)

    return out
