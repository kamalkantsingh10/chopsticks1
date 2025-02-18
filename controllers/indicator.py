import sys
import os
import logging
import time
from hw_drivers.display.o91inch import OLED_0in91
from PIL import Image, ImageDraw, ImageFont
from robot_hat import utils

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp_file:
            temp = float(temp_file.read()) / 1000.0
        return temp
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

class  Indicator:
    def __init__(self):
        self.disp = OLED_0in91.OLED_0in91()
        self.Init()
        
        font_path = '/home/kamal/projects/chopsticks1/hw_drivers/display/Font/Font00.ttf'
        self.font1 = ImageFont.truetype(font_path, 18)

        # Segment settings
        self.segments = 10  # Number of segments
        self.segment_gap = 2  # Gap between segments

    def start(self):
        while True:
            #disp.clear()
            image1 = Image.new('1', (self.disp.width, self.disp.height), 0)
            draw = ImageDraw.Draw(image1)

            # Fill background white
            draw.rectangle((0, 0, self.disp.width-1, self.disp.height-1), fill=1)

            # Get sensor values
            battery_voltage = utils.get_battery_voltage()
            temp = get_cpu_temp()

            # Calculate battery percentage (6V-8.4V range)
            min_voltage = 6.0
            max_voltage = 8.0
            battery_percentage = min(100, max(0, ((battery_voltage - min_voltage) / (max_voltage - min_voltage)) * 100))

            # Battery bar dimensions (2/3 of screen width)
            bar_width = int(self.disp.width * 2/3)
            
            # Draw battery outline
            draw.rectangle((0, 0, bar_width, self.disp.height-1), fill=1, outline=0)
            
            # Calculate segment dimensions
            segment_width = (bar_width - (self.segments + 1) * self.segment_gap) // self.segments
            filled_segments = int((battery_percentage / 100) * self.segments)

            # Draw segments
            for i in range(self.segments):
                x1 = self.segment_gap + i * (segment_width + self.segment_gap)
                x2 = x1 + segment_width
                y1 = 2
                y2 = self.disp.height 
                
                if i < filled_segments:
                    # Fill segment for battery level
                    draw.rectangle((x1, y1, x2, y2), fill=0)

            # Temperature in remaining 1/3
            if temp is not None:
                temp_text = f" {temp:.0f}C"
                # Center text in remaining space
                text_width = self.font1.getlength(temp_text)
                text_x = bar_width + 8+((self.disp.width - bar_width) - text_width) // 2
                text_y = (self.disp.height - 24) // 2
                draw.text((text_x, text_y), temp_text, font=self.font1, fill=0)

            # Ensure display is on and update
            self.disp.command(0xAF)
            image1 = image1.rotate(0)
            self.disp.ShowImage(self.disp.getbuffer(image1))
            
            time.sleep(60)
