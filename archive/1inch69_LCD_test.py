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

# Color definition (Vector uses blue-white color)
EYE_COLOR = (71, 235, 235)  # Bright cyan color
BG_COLOR = "BLACK"

# Vector/Cosmo eye expressions with larger sizes
EMOTIONS = {
    'normal': {
        'eye_width': 80,    # Increased from 45
        'eye_height': 80,   # Increased from 45
        'eye_curve': 15,    # Increased for proportion
        'pupil_size': 35,   # Increased from 20
        'pupil_offset': (0, 0)
    },
    'happy': {
        'eye_width': 80,
        'eye_height': 65,
        'eye_curve': 18,
        'pupil_size': 32,
        'pupil_offset': (0, -8)
    },
    'curious': {
        'eye_width': 80,
        'eye_height': 80,
        'eye_curve': 15,
        'pupil_size': 30,
        'pupil_offset': (15, 0),
        'different_pupils': True
    },
    'sleepy': {
        'eye_width': 80,
        'eye_height': 35,
        'eye_curve': 12,
        'pupil_size': 25,
        'pupil_offset': (0, 2)
    }
}

def draw_rounded_rectangle(draw, coords, radius, fill):
    """Draw a rectangle with rounded corners"""
    x1, y1, x2, y2 = coords
    
    # Ensure coordinates are in correct order
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    
    # Ensure minimum size
    if x2 - x1 < 2 * radius:
        radius = (x2 - x1) // 2
    if y2 - y1 < 2 * radius:
        radius = (y2 - y1) // 2
    
    if radius <= 0:
        draw.rectangle([x1, y1, x2, y2], fill=fill)
        return
        
    # Draw main rectangle
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    
    # Draw four corners
    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)

def draw_eyes(disp, emotion='normal', blink_progress=0):
    try:
        image = Image.new("RGB", (280, 240), BG_COLOR)
        draw = ImageDraw.Draw(image)
        
        style = EMOTIONS[emotion]
        
        # Base eye positions - adjusted for larger eyes
        left_eye_pos = (80, 120)    # Moved slightly more apart
        right_eye_pos = (200, 120)  # Moved slightly more apart
        
        # Calculate eye height with blink (ensure minimum height)
        eye_height = max(4, style['eye_height'] * (1 - blink_progress))
        
        for i, pos in enumerate([left_eye_pos, right_eye_pos]):
            # Draw the main eye shape
            eye_box = (
                pos[0] - style['eye_width']//2,
                pos[1] - eye_height//2,
                pos[0] + style['eye_width']//2,
                pos[1] + eye_height//2
            )
            draw_rounded_rectangle(draw, eye_box, style['eye_curve'], EYE_COLOR)
            
            # Draw pupils if not fully blinked
            if blink_progress < 0.9 and eye_height > 8:
                pupil_offset = style['pupil_offset']
                if style.get('different_pupils') and i == 1:
                    pupil_offset = (-pupil_offset[0], pupil_offset[1])
                
                # Scale pupil size with eye height
                pupil_scale = min(1, eye_height / style['eye_height'])
                pupil_size = int(style['pupil_size'] * pupil_scale)
                
                if pupil_size > 0:
                    pupil_box = (
                        pos[0] - pupil_size//2 + pupil_offset[0],
                        pos[1] - pupil_size//2 + pupil_offset[1],
                        pos[0] + pupil_size//2 + pupil_offset[0],
                        pos[1] + pupil_size//2 + pupil_offset[1]
                    )
                    draw_rounded_rectangle(draw, pupil_box, min(style['eye_curve']//2, pupil_size//4), BG_COLOR)
        
        disp.ShowImage(image)
        return True
        
    except Exception as e:
        logging.error(f"Error drawing eyes: {e}")
        return False

def main():
    try:
        disp = LCD.LCD_1inch69(
            spi=SPI.SpiDev(bus, device),
            spi_freq=10000000,
            rst=RST,
            dc=DC,
            bl=BL
        )
        
        disp.Init()
        disp.clear()
        disp.bl_DutyCycle(70)
        
        last_blink = time.time()
        blink_duration = 0.15
        current_emotion = 'normal'
        emotion_change_time = time.time()
        
        while True:
            current_time = time.time()
            
            # Blink handling
            if current_time - last_blink > random.uniform(2.5, 4.0):
                blink_progress = min(1, (current_time - last_blink - 2.5) / blink_duration)
                if blink_progress >= 1:
                    last_blink = current_time
            else:
                blink_progress = 0
            
            # Change emotion every 5 seconds for demo
            if current_time - emotion_change_time > 5:
                current_emotion = random.choice(list(EMOTIONS.keys()))
                emotion_change_time = current_time
                print(f"Changed emotion to: {current_emotion}")
            
            draw_eyes(disp, current_emotion, blink_progress)
            time.sleep(0.05)
            
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("quit:")
        exit()

if __name__ == "__main__":
    main()