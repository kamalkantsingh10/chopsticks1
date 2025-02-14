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

def indicator():
    try:
        disp = OLED_0in91.OLED_0in91()
        disp.Init()
        
        font_path = '/home/kamal/projects/chopsticks1/hw_drivers/display/Font/Font00.ttf'
        font1 = ImageFont.truetype(font_path, 18)

        # Segment settings
        segments = 10  # Number of segments
        segment_gap = 2  # Gap between segments

        while True:
            #disp.clear()
            image1 = Image.new('1', (disp.width, disp.height), 0)
            draw = ImageDraw.Draw(image1)

            # Fill background white
            draw.rectangle((0, 0, disp.width-1, disp.height-1), fill=1)

            # Get sensor values
            battery_voltage = utils.get_battery_voltage()
            temp = get_cpu_temp()

            # Calculate battery percentage (6V-8.4V range)
            min_voltage = 6.0
            max_voltage = 8.0
            battery_percentage = min(100, max(0, ((battery_voltage - min_voltage) / (max_voltage - min_voltage)) * 100))

            # Battery bar dimensions (2/3 of screen width)
            bar_width = int(disp.width * 2/3)
            
            # Draw battery outline
            draw.rectangle((0, 0, bar_width, disp.height-1), fill=1, outline=0)
            
            # Calculate segment dimensions
            segment_width = (bar_width - (segments + 1) * segment_gap) // segments
            filled_segments = int((battery_percentage / 100) * segments)

            # Draw segments
            for i in range(segments):
                x1 = segment_gap + i * (segment_width + segment_gap)
                x2 = x1 + segment_width
                y1 = 2
                y2 = disp.height 
                
                if i < filled_segments:
                    # Fill segment for battery level
                    draw.rectangle((x1, y1, x2, y2), fill=0)

            # Temperature in remaining 1/3
            if temp is not None:
                temp_text = f" {temp:.0f}C"
                # Center text in remaining space
                text_width = font1.getlength(temp_text)
                text_x = bar_width + 8+((disp.width - bar_width) - text_width) // 2
                text_y = (disp.height - 24) // 2
                draw.text((text_x, text_y), temp_text, font=font1, fill=0)

            # Ensure display is on and update
            disp.command(0xAF)
            image1 = image1.rotate(0)
            disp.ShowImage(disp.getbuffer(image1))
            
            time.sleep(30)

    except KeyboardInterrupt:
        print("Program stopped by user")
        disp.command(0xAE)
        disp.clear()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    indicator()