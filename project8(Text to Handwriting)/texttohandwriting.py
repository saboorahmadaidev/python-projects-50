from PIL import Image, ImageDraw, ImageFont

txt = "Hello, this is a sample text to be converted into handwriting style."
try:
    font_path = r"C:\Windows\Fonts\Segoe Print.ttf"  
    font = ImageFont.truetype(font_path, 40)
except OSError:
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\calibrib.ttf", 40)
    except OSError:
        print("Warning: Font file not found. Using default font.")
        font = ImageFont.load_default()

# Create an image
img = Image.new("RGB", (1200, 250), color="white")
draw = ImageDraw.Draw(img)

draw.text((10, 50), txt, fill=(0, 0, 138), font=font)

# Save the image
img.save("handwritten_image.png")
print("Handwriting image created successfully!")
