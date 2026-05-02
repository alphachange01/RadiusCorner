from PIL import Image, ImageDraw, ImageFilter

def apply_radius(path, value):
    img = Image.open(path).convert("RGBA")
    w, h = img.size

    v = max(50, min(int(value), 200))

    if v <= 70:
        radius = int(min(w, h) * 0.15)
    elif v <= 120:
        radius = int(min(w, h) * 0.3)
    elif v <= 170:
        radius = int(min(w, h) * 0.42)
    else:
        radius = int(min(w, h) * 0.5)

    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)

    mask = mask.filter(ImageFilter.GaussianBlur(2))
    img.putalpha(mask)

    out = path.replace(".png", f"_{value}.png")
    img.save(out)

    return out
