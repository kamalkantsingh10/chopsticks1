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

# Emotion definitions with specific characteristics for each
EMOTIONS = {
    'normal': {
        'eye_size': 60,
        'pupil_size': 20,
        'pupil_offset': (0, 0),
        'eye_stretch': 1.0,
        'color': 'WHITE',
        'pupil_color': 'BLACK'
    },
    'happy': {
        'eye_size': 55,
        'pupil_size': 18,
        'pupil_offset': (0, -10),
        'eye_stretch': 0.8,  # Squished vertically for happy look
        'color': 'WHITE',
        'pupil_color': 'BLACK'
    },
    'angry': {
        'eye_size': 60,
        'pupil_size': 25,
        'pupil_offset': (0, 5),
        'eye_stretch': 1.2,
        'color': 'WHITE',
        'pupil_color': 'RED'
    },
    'sad': {
        'eye_size': 60,
        'pupil_size': 20,
        'pupil_offset': (0, 15),
        'eye_stretch': 1.1,
        'color': 'WHITE',
        'pupil_color': 'BLUE'
    },
    'excited': {
        'eye_size': 65,
        'pupil_size': 15,
        'pupil_offset': (0, 0),
        'eye_stretch': 1.0,
        'color': 'WHITE',
        'pupil_color': 'BLACK'
    },
    'sleepy': {
        'eye_size': 60,
        'pupil_size': 20,
        'pupil_offset': (0, 15),
        'eye_stretch': 0.5,  # Very squished for sleepy look
        'color': 'WHITE',
        'pupil_color': 'BLACK'
    },
    'surprised': {
        'eye_size': 70,
        'pupil_size': 15,
        'pupil_offset': (0, 0),
        'eye_stretch': 1.3,
        'color': 'WHITE',
        'pupil_color': 'BLACK'
    },
    'love': {
        'eye_size': 55,
        'pupil_size': 25,
        'pupil_offset': (0, 0),
        'eye_stretch': 0.9,
        'color': 'WHITE',
        'pupil_color': 'RED',
        'heart_pupils': True
    },
    'confused': {
        'eye_size': 60,
        'pupil_size': 20,
        'pupil_offset': (10, 0),  # Pupils look in different directions
        'eye_stretch': 1.0,
        'color': 'WHITE',
        'pupil_color': 'BLACK',
        'different_pupils': True
    },
    'suspicious': {
        'eye_size': 55,
        'pupil_size': 20,
        'pupil_offset': (15, 0),
        'eye_stretch': 0.7,
        'color': 'WHITE',
        'pupil_color': 'BLACK'
    },
    'dizzy': {
        'eye_size': 60,
        'pupil_size': 20,
        'pupil_offset': (0, 0),
        'eye_stretch': 1.0,
        'color': 'WHITE',
        'pupil_color': 'BLACK',
        'spiral_pupils': True
    }
}

def draw_heart(draw, center, size, color):
    """Helper function to draw heart-shaped pupils"""
    x, y = center
    points = [
        (x, y - size//2),
        (x - size//2, y - size//4),
        (x - size//2, y + size//4),
        (x, y + size//2),
        (x + size//2, y + size//4),
        (x + size//2, y - size//4),
    ]
    draw.polygon(points, fill=color)

def draw_spiral(draw, center, size, color):
    """Helper function to draw spiral pupils for dizzy eyes"""
    x, y = center
    points = []
    for t in range(0, 360, 30):
        r = size * (t / 360)
        px = x + r * math.cos(math.radians(t))
        py = y + r * math.sin(math.radians(t))
        points.append((px, py))
    if len(points) > 2:
        draw.line(points, fill=color, width=3)

def draw_eyes(disp, emotion='normal', blink_progress=0):
    try:
        image = Image.new("RGB", (280, 240), "BLACK")
        draw = ImageDraw.Draw(image)
        
        style = EMOTIONS[emotion]
        eye_size = style['eye_size']
        pupil_size = style['pupil_size']
        base_offset = style['pupil_offset']
        stretch = style['eye_stretch']
        
        # Eye positions
        left_eye_pos = (70, 120)
        right_eye_pos = (210, 120)
        
        # Draw both eyes
        for i, pos in enumerate([left_eye_pos, right_eye_pos]):
            # White part of eye
            draw.ellipse(
                (pos[0] - eye_size,
                 pos[1] - eye_size * stretch * (1 - blink_progress),
                 pos[0] + eye_size,
                 pos[1] + eye_size * stretch * (1 - blink_progress)),
                fill=style['color']
            )
            
            if blink_progress < 0.9:
                pupil_offset = base_offset
                if style.get('different_pupils') and i == 1:
                    pupil_offset = (-base_offset[0], base_offset[1])
                
                if style.get('heart_pupils'):
                    draw_heart(draw, 
                             (pos[0] + pupil_offset[0], 
                              pos[1] + pupil_offset[1] * (1 - blink_progress)),
                             pupil_size * 2, 
                             style['pupil_color'])
                elif style.get('spiral_pupils'):
                    draw_spiral(draw,
                              (pos[0] + pupil_offset[0],
                               pos[1] + pupil_offset[1] * (1 - blink_progress)),
                              pupil_size,
                              style['pupil_color'])
                else:
                    draw.ellipse(
                        (pos[0] - pupil_size + pupil_offset[0],
                         pos[1] - pupil_size * (1 - blink_progress) + pupil_offset[1],
                         pos[0] + pupil_size + pupil_offset[0],
                         pos[1] + pupil_size * (1 - blink_progress) + pupil_offset[1]),
                        fill=style['pupil_color']
                    )
        
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
        disp.bl_DutyCycle(50)
        
        last_blink = time.time()
        blink_duration = 0.2
        current_emotion = 'normal'
        emotion_change_time = time.time()
        
        while True:
            current_time = time.time()
            
            # Blink handling
            if current_time - last_blink > 3:
                blink_progress = min(1, (current_time - last_blink - 3) / blink_duration)
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