
import config
import board
import random, time
from PIL import Image, ImageDraw, ImageFont
# from adafruit_rgb_display import ili9341
# from adafruit_rgb_display import st7789  # pylint: disable=unused-import
# from adafruit_rgb_display import hx8357  # pylint: disable=unused-import
from adafruit_rgb_display import st7735  # pylint: disable=unused-import
# from adafruit_rgb_display import ssd1351  # pylint: disable=unused-import
# from adafruit_rgb_display import ssd1331  # pylint: disable=unused-import


# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=172, height=320, x_offset=34, # 1.47" ST7789
# disp = st7789.ST7789(spi, rotation=270, width=170, height=320, x_offset=35, # 1.9" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
disp = st7735.ST7735R(spi, rotation=config.Rotation,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True, width=80,       # 0.96" MiniTFT Rev A ST7735R
# disp = st7735.ST7735R(spi, rotation=90, invert=True, width=80,    # 0.96" MiniTFT Rev B ST7735R
# x_offset=26, y_offset=1,
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
#disp = ili9341.ILI9341(
#    spi,
#    rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=config.cs_pin,
    dc=config.dc_pin,
    rst=config.reset_pin,
    baudrate=config.BAUDRATE,
)
# pylint: enable=line-too-long

def draw_image(filename):
    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width  # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width  # we swap height/width to rotate it to landscape!
        height = disp.height
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))
    font = ImageFont.truetype(config.font_path_2, config.font_size)
    draw.text((10, 5), "Scan and Charge", font=font, fill=(0, 0, 0))

    disp.image(image)

    image = Image.open(filename)

    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height - 25

    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    # Display image.
    disp.image(image)

def display_info(voltage, current, energy):
    image = Image.new("RGB", (disp.width, disp.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=(0, 0, 0))

    font = ImageFont.truetype(config.font_path, config.font_size)
    # Draw text on the image
    text = "Voltage: {:.2f} V\nCurrent: {:.2f} A\nUnits: {:.2f} Kwh \n\n     Charging".format(voltage, current, energy)
    draw.text((10, 10), text, font=font, fill=(255, 255, 255))

    # Convert the PIL image to a format compatible with the display
    disp.image(image)

    # Delay for one second
    time.sleep(1)


def display_text(text):
    image = Image.new("RGB", (disp.width, disp.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=(0, 0, 0))

    font = ImageFont.truetype(config.font_path, config.font_size)
    # Draw text on the image
    draw.text((10, 50), text, font=font, fill=(255, 255, 255))

    # Convert the PIL image to a format compatible with the display
    disp.image(image)

    # Delay for one second
    time.sleep(1)