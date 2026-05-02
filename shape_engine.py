from PIL import Image, ImageDraw, ImageFilter

def apply_radius(path, value):
    img = Image.open(path).convert("RGBA")

    w, h = img.size
    size = max(w, h)

    v = max(50, min(int(value), 200))

    # radius mapping
    if v <= 70:
        radius = int(size * 0.15)
    elif v <= 120:
        radius = int(size * 0.3)
    elif v <= 170:
        radius = int(size * 0.42)
    else:
        radius = int(size * 0.5)

    # 🔥 1. FORCE SQUARE CANVAS (MUHIM QISM)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # center image
    x = (size - w) // 2
    y = (size - h) // 2
    canvas.paste(img, (x, y), img)

    # 🔥 2. NEW MASK (REAL SHAPE CONTROL)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, size, size),
        radius=radius,
        fill=255
    )

    mask = mask.filter(ImageFilter.GaussianBlur(1.5))

    canvas.putalpha(mask)

    out = path.replace(".png", f"_{value}.png")
    canvas.save(out)

    return out
