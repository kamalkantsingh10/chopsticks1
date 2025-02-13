import os
import sys
import time
import random
import logging
import math
import spidev as SPI
from hw_drivers.display import LCD_1inch69 as LCD
from PIL import Image, ImageDraw
from enum import Enum

class Emotion(Enum):
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    ALERT = "alert"
    CURIOUS = "curious"
    SLEEPY = "sleepy"
    LOVING = "loving"
    GRUMPY = "grumpy"
    SCARED = "scared"
    MISCHIEVOUS = "mischievous"
    NEUTRAL = "neutral"

# Pin definitions for the display
RST = 27
DC = 22
BL = 4
bus = 0
device = 0

# Display dimensions (portrait mode)
WIDTH = 240
HEIGHT = 280

# Dot configuration
DOT_SIZE = 70
MAIN_COLOR = (50, 255, 50)  # Light green - our primary color
BACKGROUND_COLOR = (10, 12, 15)  # Very dark blue-gray
DOT_SPACING = 90

# Calculate center positions for both dots
CENTER_Y = HEIGHT // 2
LEFT_X = (WIDTH // 2) - (DOT_SPACING // 2)
RIGHT_X = (WIDTH // 2) + (DOT_SPACING // 2)

# Transition configuration
TRANSITION_DURATION = 1.0  # Duration of transition in seconds
TRANSITION_STEPS = 30  # Number of frames for transition

def lerp_color(color1, color2, t):
    """Linear interpolation between two colors"""
    return tuple(int(a + (b - a) * t) for a, b in zip(color1, color2))

def lerp_value(v1, v2, t):
    """Linear interpolation between two values"""
    return v1 + (v2 - v1) * t

class FaceController:
    def __init__(self):
        # Initialize display
        self.disp = LCD.LCD_1inch69(
            spi=SPI.SpiDev(bus, device),
            spi_freq=10000000,
            rst=RST,
            dc=DC,
            bl=BL
        )
        self.disp.Init()
        self.disp.clear()
        self.disp.bl_DutyCycle(70)
        
        # Initialize states
        self.last_blink = time.time()
        self.blink_interval = random.uniform(2.0, 5.0)
        self.is_blinking = False
        self.blink_duration = random.uniform(0.1, 0.3)
        self.current_emotion = Emotion.NEUTRAL
        self.target_emotion = Emotion.NEUTRAL
        self.transition_start = 0
        self.transition_progress = 1.0  # 1.0 means no transition

    def get_emotion_config(self, emotion):
        config = {
            'left': {},
            'right': {},
            'blink': False
        }
        
        base_config = {
            'color': MAIN_COLOR,
            'size': DOT_SIZE
        }
        
        if emotion == Emotion.NEUTRAL:
            config['left'] = {**base_config, 'shape': 'rounded_rect'}
            config['right'] = {**base_config, 'shape': 'rounded_rect'}
            config['blink'] = True
        elif emotion == Emotion.HAPPY:
            config['left'] = {**base_config, 'shape': 'arc_up'}
            config['right'] = {**base_config, 'shape': 'arc_up'}
        elif emotion == Emotion.SAD:
            config['left'] = {**base_config, 'shape': 'arc_down'}
            config['right'] = {**base_config, 'shape': 'arc_down'}
        elif emotion == Emotion.EXCITED:
            config['left'] = {**base_config, 'shape': 'star'}
            config['right'] = {**base_config, 'shape': 'star'}
        elif emotion == Emotion.ALERT:
            new_size = int(DOT_SIZE * 1.2)
            config['left'] = {**base_config, 'shape': 'circle', 'size': new_size}
            config['right'] = {**base_config, 'shape': 'circle', 'size': new_size}
        elif emotion == Emotion.CURIOUS:
            config['left'] = {**base_config, 'shape': 'rounded_rect', 'size': int(DOT_SIZE * 1.5), 'dx': -10}
            config['right'] = {**base_config, 'shape': 'rounded_rect', 'size': int(DOT_SIZE * 0.8), 'dx': 10}
        elif emotion == Emotion.SLEEPY:
            config['left'] = {**base_config, 'shape': 'line_horizontal'}
            config['right'] = {**base_config, 'shape': 'line_horizontal'}
        elif emotion == Emotion.LOVING:
            config['left'] = {**base_config, 'shape': 'heart'}
            config['right'] = {**base_config, 'shape': 'heart'}
        elif emotion == Emotion.GRUMPY:
            config['left'] = {**base_config, 'shape': 'x'}
            config['right'] = {**base_config, 'shape': 'x'}
        elif emotion == Emotion.SCARED:
            new_size = int(DOT_SIZE * 0.5)
            config['left'] = {**base_config, 'shape': 'circle', 'size': new_size}
            config['right'] = {**base_config, 'shape': 'circle', 'size': new_size}
        elif emotion == Emotion.MISCHIEVOUS:
            config['left'] = {**base_config, 'shape': 'rounded_rect'}
            config['right'] = {**base_config, 'shape': 'line_horizontal'}
        
        return config

    def interpolate_configs(self, config1, config2, t):
        """Interpolate between two emotion configurations"""
        result = {
            'left': {},
            'right': {},
            'blink': config1['blink']
        }
        
        for side in ['left', 'right']:
            c1, c2 = config1[side], config2[side]
            result[side] = {
                'shape': c2['shape'],  # Shapes don't interpolate
                'color': lerp_color(c1['color'], c2['color'], t),
                'size': lerp_value(c1.get('size', DOT_SIZE), c2.get('size', DOT_SIZE), t),
                'dx': lerp_value(c1.get('dx', 0), c2.get('dx', 0), t),
                'dy': lerp_value(c1.get('dy', 0), c2.get('dy', 0), t)
            }
        
        return result

    def set_emotion(self, emotion):
        """Start transition to new emotion with a blink"""
        if emotion != self.target_emotion:
            self.target_emotion = emotion
            self.transition_start = time.time()
            self.transition_progress = 0.0
            # Force a blink to start
            self.is_blinking = True
            self.last_blink = time.time()
            self.blink_duration = 0.3  # Slightly longer blink for transition

    def update_transition(self):
        """Update transition progress"""
        if self.transition_progress < 1.0:
            self.transition_progress = min(1.0, (time.time() - self.transition_start) / TRANSITION_DURATION)
            if self.transition_progress >= 1.0:
                self.current_emotion = self.target_emotion

    def draw_rounded_rectangle(self, draw, coords, radius, fill):
        """Helper function to draw a rounded rectangle"""
        x1, y1, x2, y2 = coords
        
        # Draw the rounded corners
        draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
        draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
        draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
        draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)
        
        # Draw the main rectangles
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)

    def update_blink(self):
        """Update blink state for both dots"""
        current_time = time.time()
        
        # Check if it's time to start a new blink
        if not self.is_blinking and current_time - self.last_blink > self.blink_interval:
            self.is_blinking = True
            self.last_blink = current_time
            self.blink_duration = random.uniform(0.1, 0.3)
        
        # Check if current blink should end
        if self.is_blinking and current_time - self.last_blink > self.blink_duration:
            self.is_blinking = False
            self.blink_interval = random.uniform(2.0, 5.0)

    def draw_single_dot(self, draw, center_x, eye_config):
        """Draw a single eye based on configuration"""
        shape = eye_config.get('shape', 'rounded_rect')
        color = eye_config.get('color', MAIN_COLOR)
        size = eye_config.get('size', DOT_SIZE)
        dx = eye_config.get('dx', 0)
        dy = eye_config.get('dy', 0)

        x_center = int(center_x + dx)
        y_center = int(CENTER_Y + dy)

        x1 = int(x_center - size // 2)
        y1 = int(y_center - size // 2)
        x2 = int(x_center + size // 2)
        y2 = int(y_center + size // 2)

        if self.is_blinking:
            blink_height = max(3, size // 8)
            y_mid = (y1 + y2) // 2
            y_blink1 = y_mid - blink_height // 2
            y_blink2 = y_mid + blink_height // 2
            self.draw_rounded_rectangle(draw, [x1, y_blink1, x2, y_blink2], blink_height // 2, color)
        else:
            if shape == 'rounded_rect':
                radius = size // 4
                self.draw_rounded_rectangle(draw, [x1, y1, x2, y2], radius, color)
            elif shape == 'arc_up':
                thickness = max(1, int(size // 4))
                draw.arc([int(x1), int(y1), int(x2), int(y2)], 180, 0, fill=color, width=thickness)
            elif shape == 'arc_down':
                thickness = max(1, int(size // 4))
                draw.arc([int(x1), int(y1), int(x2), int(y2)], 0, 180, fill=color, width=thickness)
            elif shape == 'circle':
                draw.ellipse([x1, y1, x2, y2], fill=color)
            elif shape == 'line_horizontal':
                line_thickness = max(1, int(size // 8))
                mid_y = int((y1 + y2) // 2)
                draw.line([int(x1), mid_y, int(x2), mid_y], fill=color, width=line_thickness)
            elif shape == 'heart':
                cx = int((x1 + x2) // 2)
                cy = int((y1 + y2) // 2)
                radius = int(size // 4)
                # Heart points (approximation)
                points = [
                    (int(cx - radius), int(cy - radius + 10)),
                    (cx, int(cy + radius)),
                    (int(cx + radius), int(cy - radius + 10)),
                    (cx, int(cy - radius))
                ]
                draw.polygon(points, fill=color)
            elif shape == 'star':
                cx = int((x1 + x2) // 2)
                cy = int((y1 + y2) // 2)
                outer_radius = int(size // 2)
                inner_radius = int(outer_radius // 2)
                points = []
                for i in range(10):
                    angle = 2 * math.pi * i / 10 - math.pi / 2
                    radius = inner_radius if i % 2 else outer_radius
                    x = int(cx + radius * math.cos(angle))
                    y = int(cy + radius * math.sin(angle))
                    points.append((x, y))
                draw.polygon(points, fill=color)
            elif shape == 'x':
                line_thickness = max(1, int(size // 8))
                draw.line([int(x1), int(y1), int(x2), int(y2)], fill=color, width=line_thickness)
                draw.line([int(x2), int(y1), int(x1), int(y2)], fill=color, width=line_thickness)

    def draw_dots(self):
        """Draw both eyes with emotion configuration, transitioning during blinks"""
        self.update_blink()
        
        # If we're in a transition and blinking
        if self.transition_progress < 1.0 and self.is_blinking:
            # If we're in the first half of the blink, show original emotion
            if time.time() - self.last_blink < self.blink_duration / 2:
                config = self.get_emotion_config(self.current_emotion)
            else:
                # In the second half of the blink, show new emotion and complete transition
                config = self.get_emotion_config(self.target_emotion)
                self.current_emotion = self.target_emotion
                self.transition_progress = 1.0
        else:
            # Normal display - either current or target emotion
            config = self.get_emotion_config(self.current_emotion)
        
        image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(image)
        
        self.draw_single_dot(draw, LEFT_X, config['left'])
        self.draw_single_dot(draw, RIGHT_X, config['right'])
        
        self.disp.ShowImage(image)

    def run(self):
        """Main loop to continuously update and cycle emotions"""
        emotions = list(Emotion)
        current_index = emotions.index(Emotion.NEUTRAL)
        last_change = time.time()
        try:
            while True:
                if time.time() - last_change > 5:
                    current_index = (current_index + 1) % len(emotions)
                    self.set_emotion(emotions[current_index])
                    last_change = time.time()
                self.draw_dots()
                time.sleep(1.0 / TRANSITION_STEPS)  # Smooth frame rate
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        """Clean up display resources"""
        self.disp.module_exit()

