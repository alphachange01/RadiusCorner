import cv2
import numpy as np

def apply_radius(path, value):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    h, w = img.shape[:2]
    size = max(w, h)

    v = max(50, min(int(value), 200))
    t = (v - 50) / 150

    radius = int((size // 2) * t)

    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    canvas = np.zeros((size, size, 4), dtype=np.uint8)

    x = (size - w) // 2
    y = (size - h) // 2
    canvas[y:y+h, x:x+w] = img

    # 🔥 REAL MASK (NO BLUR!)
    mask = np.zeros((size, size), dtype=np.uint8)

    # square base
    mask[:] = 255

    # cut corners manually (IMPORTANT PART)
    if radius > 0:
        corner = np.zeros((size, size), dtype=np.uint8)

        cv2.rectangle(corner, (radius, 0), (size-radius, size), 255, -1)
        cv2.rectangle(corner, (0, radius), (size, size-radius), 255, -1)

        # circles in corners
        cv2.circle(corner, (radius, radius), radius, 255, -1)
        cv2.circle(corner, (size-radius, radius), radius, 255, -1)
        cv2.circle(corner, (radius, size-radius), radius, 255, -1)
        cv2.circle(corner, (size-radius, size-radius), radius, 255, -1)

        mask = corner

    result = cv2.bitwise_and(canvas, canvas, mask=mask)

    out = path.replace(".png", f"_{value}.png")
    cv2.imwrite(out, result)

    return out
