import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Create the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED display instance
# 128x32 display with hardware I2C
WIDTH = 128
HEIGHT = 32
BORDER = 5

display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Clear the display
display.fill(0)
display.show()

# Create blank image for drawing
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

# Draw a test pattern
draw.rectangle((0, 0, WIDTH, HEIGHT), outline=255, fill=0)
draw.text((WIDTH//4, HEIGHT//4), "Hello!", fill=255)

# Display image
display.image(image)
display.show()