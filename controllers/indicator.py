import sys
import os
import time
from hw_drivers.display.o91inch import OLED_0in91
from PIL import Image, ImageDraw, ImageFont

class Indicator:
    def __init__(self):
        self.disp = OLED_0in91.OLED_0in91()
        self.disp.Init()
        font_path = '/home/kamal/projects/chopsticks1/hw_drivers/display/Font/Font00.ttf'
        self.font1 = ImageFont.truetype(font_path, 15)
        # Turn on display
        self.disp.command(0xAF)
        self.display_text("Chopsticks 1.0")
        
    def display_text(self, text):
        """Display center-aligned text on the screen"""
        # Create a blank white image
        image = Image.new('1', (self.disp.width, self.disp.height), 1)
        draw = ImageDraw.Draw(image)
        
        # Draw center-aligned text in black
        text_width = self.font1.getlength(text)
        text_x = (self.disp.width - text_width) // 2
        text_y = (self.disp.height - 24) // 2
        draw.text((text_x, text_y), text, font=self.font1, fill=0)
        
        # Show the image
        image = image.rotate(0)
        self.disp.ShowImage(self.disp.getbuffer(image))