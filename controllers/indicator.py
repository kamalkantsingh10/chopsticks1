import sys
import os
import logging
import time
from hw_drivers.display.o91inch import OLED_0in91
from PIL import Image, ImageDraw, ImageFont

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
        # Initialize display once
        disp = OLED_0in91.OLED_0in91()
        disp.Init()
        
        # Font paths
        font_path = '/home/kamal/projects/chopsticks1/hw_drivers/display/Font/Font00.ttf'
        font1 = ImageFont.truetype(font_path, 12)
        font2 = ImageFont.truetype(font_path, 18)

        while True:
            # Create new image
            image1 = Image.new('1', (disp.width, disp.height), "WHITE")
            draw = ImageDraw.Draw(image1)

            # Draw border
            draw.line([(0,0),(127,0)], fill=0)
            draw.line([(0,0),(0,31)], fill=0)
            draw.line([(0,31),(127,31)], fill=0)
            draw.line([(127,0),(127,31)], fill=0)

            # Get and display temperature
            temp = get_cpu_temp()
            if temp is not None:
                temp_str = f'Temp: {temp:.1f}C'
                draw.text((20,0), 'Waveshare', font=font1, fill=0)
                draw.text((20,15), temp_str, font=font1, fill=0)

            # Ensure display is on
            disp.command(0xAF)  # Display ON
            
            # Update display
            image1 = image1.rotate(0)
            disp.ShowImage(disp.getbuffer(image1))
            
            # Commands to keep display active
            disp.command(0x81)  # Set contrast
            disp.command(0xFF)  # Maximum contrast
            disp.command(0x8D)  # Charge pump
            disp.command(0x14)  # Enable charge pump
            
            time.sleep(2)

    except KeyboardInterrupt:
        print("Program stopped by user")
        disp.command(0xAE)  # Display OFF
        disp.clear()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    indicator()