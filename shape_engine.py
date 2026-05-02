from PIL import Image, ImageDraw, ImageFilter

def apply_radius(path, value):
    img = Image.open(path).convert("RGBA")

    w, h = img.size
    size = max(w, h)

    v = max(50, min(int(value), 200))

    # 🔥 REAL CONTRAST MAPPING (MUHIM)
    # 50 -> sharp square
    # 100 -> mild round
    # 150 -> strong round
    # 200 -> almost circle

    if v == 50:
        radius = 0
    elif v <= 80:
        radius = int(size * 0.08)
    elif v <= 120:
        radius = int(size * 0.18)
    elif v <= 160:
        radius = int(size * 0.32)
    else:
        radius = int(size * 0.48)

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    x = (size - w) // 2
    y = (size - h) // 2
    canvas.paste(img, (x, y), img)

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, size, size),
        radius=radius,
        fill=255
    )

    mask = mask.filter(ImageFilter.GaussianBlur(3))

    canvas.putalpha(mask)

    out = path.replace(".png", f"_{value}.png")
    canvas.save(out)

    return out
