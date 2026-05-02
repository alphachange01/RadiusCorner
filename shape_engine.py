from PIL import Image, ImageDraw

def apply_radius(path, value):
    img = Image.open(path).convert("RGBA")

    size = max(img.size)
    v = max(50, min(int(value), 200))

    t = (v - 50) / 150
    radius = int(size * (0.01 + 0.49 * t))

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    img = img.resize((size, size))
    canvas.paste(img, (0, 0))

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, size, size),
        radius=radius,
        fill=255
    )

    canvas.putalpha(mask)

    out = path.replace(".png", f"_{value}.png")
    canvas.save(out)

    return out
