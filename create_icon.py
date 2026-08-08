from PIL import Image, ImageDraw

img = Image.new("RGBA", (512, 512), (30, 100, 200, 255))

draw = ImageDraw.Draw(img)

draw.ellipse((100, 100, 412, 412), fill="white")

img.save(
    "app.ico",
    format="ICO",
    sizes=[
        (16, 16),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256),
    ],
)

print("app.ico created successfully!")