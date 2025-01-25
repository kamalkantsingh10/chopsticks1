import os
import sys
import time
import random
import logging
import spidev as SPI
from hw_drivers.display import LCD_1inch69 as LCD
from PIL import Image, ImageDraw, ImageFont
import math

# Pin definitions
RST = 27
DC = 22
BL = 4
bus = 0
device = 0

# Logging setup
logging.basicConfig(level=logging.DEBUG)

def draw_eyes(disp, blink_progress=0):
    try:
        # Create image in landscape mode (280x240)
        image = Image.new("RGB", (280, 240), "BLACK")
        draw = ImageDraw.Draw(image)
        
        # Keep same eye sizes
        eye_size = 60
        pupil_size = 20
        
        # Center positions in 280x240 screen
        # Horizontal center points: 280/4 and 3*(280/4)
        # Vertical center point: 240/2
        left_eye_pos = (70, 120)     # 280/4 = 70
        right_eye_pos = (210, 120)   # 3*280/4 = 210
                                    # 240/2 = 120 for vertical center
        
        # Draw both eyes
        for pos in [left_eye_pos, right_eye_pos]:
            # White part of eye
            draw.ellipse(
                (pos[0] - eye_size,
                 pos[1] - eye_size * (1 - blink_progress),
                 pos[0] + eye_size,
                 pos[1] + eye_size * (1 - blink_progress)),
                fill="WHITE", outline="WHITE"
            )
            
            # Pupil (black center)
            if blink_progress < 0.9:
                draw.ellipse(
                    (pos[0] - pupil_size,
                     pos[1] - pupil_size * (1 - blink_progress),
                     pos[0] + pupil_size,
                     pos[1] + pupil_size * (1 - blink_progress)),
                    fill="BLACK"
                )
        
        disp.ShowImage(image)
        return True
        
    except Exception as e:
        logging.error(f"Error drawing eyes: {e}")
        return False

def main():
    try:
        # Create LCD object
        disp = LCD.LCD_1inch69(
            spi=SPI.SpiDev(bus, device),
            spi_freq=10000000,
            rst=RST,
            dc=DC,
            bl=BL
        )
        
        # Initialize display
        disp.Init()
        disp.clear()
        disp.bl_DutyCycle(50)
        
        last_blink = time.time()
        blink_duration = 0.2
        
        while True:
            current_time = time.time()
            
            # Blink handling
            if current_time - last_blink > 3:
                blink_progress = min(1, (current_time - last_blink - 3) / blink_duration)
                if blink_progress >= 1:
                    last_blink = current_time
            else:
                blink_progress = 0
            
            # Draw the eyes
            draw_eyes(disp, blink_progress)
            
            # Small delay
            time.sleep(0.05)
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("quit:")
        exit()

if __name__ == "__main__":
    main()