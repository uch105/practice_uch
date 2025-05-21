from PIL import Image, ImageDraw, ImageFont
import random
import string

def generate_captcha(text, font_path='Chalkboard.ttf', font_size=30, image_size=(150, 60)):
    image = Image.new('RGB', image_size, 'white')
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0,0),text,font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    position = ((image_size[0] - text_width) // 3, (image_size[1] - text_height) // 3)

    for i in range(5):
        start = (random.randint(0, image_size[0]), random.randint(0, image_size[1]))
        end = (random.randint(0, image_size[0]), random.randint(0, image_size[1]))
        draw.line([start, end], fill='black', width=1)

    draw.text(position, text, fill='black', font=font)

    for _ in range(100):
        xy = (random.randint(0, image_size[0]), random.randint(0, image_size[1]))
        draw.point(xy, fill="black")

    return image

def save_captcha_image(image, file_path):
    image.save(file_path)
    print(f"Captcha saved as {file_path}")

def generate_random_text(length=6):
    letters_and_digits = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

captcha_text = generate_random_text()

captcha_image = generate_captcha(captcha_text)

save_captcha_image(captcha_image, 'captcha_image.png')