import os
import time
import random
import logging
import math
import threading
import spidev as SPI
from hw_drivers.display import LCD_1inch69 as LCD
from PIL import Image, ImageDraw
from core.enums import Emotion

# Display configuration
class DisplayConfig:
    # Pin definitions
    RST = 27
    DC = 22
    BL = 4
    BUS = 0
    DEVICE = 0
    
    # Display dimensions
    WIDTH = 240
    HEIGHT = 280
    
    # Visual configuration
    DOT_SIZE = 70
    DOT_SPACING = 90
    MAIN_COLOR = (50, 255, 50)  # Light green
    BACKGROUND_COLOR = (0, 0, 0)  # Very black


class FaceController:
    def __init__(self):
        # Initialize the display
        self.config = DisplayConfig()
        self.initialize_display()
        
        # Initialize emotion and blink states
        self.current_emotion = Emotion.NEUTRAL
        self.is_blinking = False
        self.last_blink_time = time.time()
        self.blink_duration = 0.2
        self.blink_interval = random.uniform(2.0, 5.0)
        
        # Threading control
        self._running = False
        self._thread = None
        
        # Show initial face
        self.update_display()
    
    def initialize_display(self):
        """Initialize the LCD display"""
        try:
            self.disp = LCD.LCD_1inch69(
                spi=SPI.SpiDev(self.config.BUS, self.config.DEVICE),
                spi_freq=10000000,
                rst=self.config.RST,
                dc=self.config.DC,
                bl=self.config.BL
            )
            self.disp.Init()
            self.disp.clear()
            self.disp.bl_DutyCycle(70)
            print("Display initialized successfully")
        except Exception as e:
            print(f"Error initializing display: {e}")
            raise
    
    def set_emotion(self, emotion):
        """Set the current emotion and update the display immediately"""
        if emotion != self.current_emotion:
            print(f"Changing emotion from {self.current_emotion.name} to {emotion.name}")
            self.current_emotion = emotion
            
            # Trigger a blink when emotion changes
            self.is_blinking = True
            self.last_blink_time = time.time()
            self.blink_duration = 0.2
            
            # Update the display immediately
            self.update_display()
    
    def update_blink_state(self):
        """Update the blink state based on timing"""
        current_time = time.time()
        
        # Check if currently blinking
        if self.is_blinking:
            # End blink if duration has passed
            if current_time - self.last_blink_time > self.blink_duration:
                self.is_blinking = False
                self.blink_interval = random.uniform(2.0, 5.0)
                return True  # Blink state changed
        else:
            # Start a new blink if interval has passed
            if current_time - self.last_blink_time > self.blink_interval:
                self.is_blinking = True
                self.last_blink_time = current_time
                self.blink_duration = random.uniform(0.1, 0.3)
                return True  # Blink state changed
        
        return False  # No change
    
    def get_emotion_shapes(self, emotion):
        """Get the shapes for both eyes based on the emotion"""
        shapes = {
            'left': 'rounded_rect',  # Default shape
            'right': 'rounded_rect',  # Default shape
            'size_left': self.config.DOT_SIZE,
            'size_right': self.config.DOT_SIZE,
            'dx_left': 0,
            'dx_right': 0,
            'dy_left': 0,
            'dy_right': 0,
            'color_left': self.config.MAIN_COLOR,
            'color_right': self.config.MAIN_COLOR
        }
        
        # Configure shapes based on emotion
        if emotion == Emotion.NEUTRAL:
            pass  # Use defaults
        elif emotion == Emotion.HAPPY:
            shapes['left'] = 'arc_up'
            shapes['right'] = 'arc_up'
        elif emotion == Emotion.SAD:
            shapes['left'] = 'arc_down'
            shapes['right'] = 'arc_down'
        elif emotion == Emotion.EXCITED:
            shapes['left'] = 'star'
            shapes['right'] = 'star'
            shapes['color_left'] = (220, 220, 220)  # white
            shapes['color_right'] = (220, 220, 220)  # white
        elif emotion == Emotion.ALERT:
            shapes['left'] = 'circle'
            shapes['right'] = 'circle'
            shapes['size_left'] = int(self.config.DOT_SIZE * 1.2)
            shapes['size_right'] = int(self.config.DOT_SIZE * 1.2)
        elif emotion == Emotion.CURIOUS:
            shapes['size_left'] = int(self.config.DOT_SIZE * 1.5)
            shapes['size_right'] = int(self.config.DOT_SIZE * 0.8)
            shapes['dx_left'] = -10
            shapes['dx_right'] = 10
        elif emotion == Emotion.SLEEPY:
            shapes['left'] = 'zzz'
            shapes['right'] = 'zzz'
            shapes['dx_left'] = -15
            shapes['dx_right'] = 15
        elif emotion == Emotion.LOVING:
            shapes['left'] = 'heart'
            shapes['right'] = 'heart'
            shapes['color_left'] = (240,80,80)  # pink
            shapes['color_right'] = (240,80,80)  # pink
        elif emotion == Emotion.GRUMPY:
            # Orange angry eyes with the correct shape from the reference
            shapes['left'] = 'orange_angry'
            shapes['right'] = 'orange_angry'
            # Adjust size and positioning to match reference
            shapes['size_left'] = int(self.config.DOT_SIZE * 1.2)
            shapes['size_right'] = int(self.config.DOT_SIZE * 1.2)
            # Set orange color
            shapes['color_left'] = (255, 99, 71)  # Orange
            shapes['color_right'] = (255, 99, 71)  # Orange
            shapes['dx_left'] = -10
            shapes['dx_right'] = 10
        elif emotion == Emotion.SCARED:
            shapes['left'] = 'circle'
            shapes['right'] = 'circle'
            shapes['size_left'] = int(self.config.DOT_SIZE * 0.5)
            shapes['size_right'] = int(self.config.DOT_SIZE * 0.5)
        elif emotion == Emotion.MISCHIEVOUS:
            shapes['right'] = 'line_horizontal'
        
        return shapes
    
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
    
    def draw_eye(self, draw, x_center, shape_type, size, dx=0, dy=0, color=None):
        """Draw a single eye with the specified shape"""
        # Calculate coordinates
        center_y = self.config.HEIGHT // 2
        x_pos = int(x_center + dx)
        y_pos = int(center_y + dy)
        
        x1 = int(x_pos - size // 2)
        y1 = int(y_pos - size // 2)
        x2 = int(x_pos + size // 2)
        y2 = int(y_pos + size // 2)
        
        # Use provided color or default
        if color is None:
            color = self.config.MAIN_COLOR
        
        # Draw different shape based on if blinking
        if self.is_blinking:
            # All shapes when blinking become a thin horizontal line
            blink_height = max(3, size // 8)
            y_mid = (y1 + y2) // 2
            y_blink1 = y_mid - blink_height // 2
            y_blink2 = y_mid + blink_height // 2
            self.draw_rounded_rectangle(draw, [x1, y_blink1, x2, y_blink2], blink_height // 2, color)
        else:
            # Draw the appropriate shape based on emotion
            if shape_type == 'rounded_rect':
                radius = size // 4
                self.draw_rounded_rectangle(draw, [x1, y1, x2, y2], radius, color)
            
            elif shape_type == 'circle':
                draw.ellipse([x1, y1, x2, y2], fill=color)
            
            elif shape_type == 'arc_up':
                # Create a smile arc
                arc_y1 = y1 - int(size * 0.2)
                arc_y2 = y2 + int(size * 0.2)
                thickness = max(1, int(size // 4))
                draw.arc([x1, arc_y1, x2, arc_y2], 180, 0, fill=color, width=thickness)
            
            elif shape_type == 'arc_down':
                # Create a frown arc
                arc_y1 = y1 - int(size * 0.2)
                arc_y2 = y2 + int(size * 0.2)
                thickness = max(1, int(size // 4))
                draw.arc([x1, arc_y1, x2, arc_y2], 0, 180, fill=color, width=thickness)
            
            elif shape_type == 'line_horizontal':
                line_thickness = max(1, int(size // 8))
                mid_y = int((y1 + y2) // 2)
                draw.line([int(x1), mid_y, int(x2), mid_y], fill=color, width=line_thickness)
            
            elif shape_type == 'x':
                line_thickness = max(1, int(size // 8))
                draw.line([int(x1), int(y1), int(x2), int(y2)], fill=color, width=line_thickness)
                draw.line([int(x2), int(y1), int(x1), int(y2)], fill=color, width=line_thickness)
            
            elif shape_type == 'orange_angry':
                # Create orange angry eyes based on the reference image
                # These are triangular/diagonal shapes with gradient-like stripes
                
                # Draw the main triangular shape
                width = x2 - x1
                height = y2 - y1
                
                # Create a triangle pointing toward the center
                is_left = x_pos < self.config.WIDTH // 2
                
                if is_left:
                    # Left eye - triangle pointing right
                    points = [
                        (x1, y1),             # Top left
                        (x1, y2),             # Bottom left
                        (x2, (y1 + y2) // 1.5)  # Middle right (point)
                    ]
                else:
                    # Right eye - triangle pointing left
                    points = [
                        (x2, y1),             # Top right
                        (x2, y2),             # Bottom right
                        (x1, (y1 + y2) // 1.5)  # Middle left (point)
                    ]
                
                # Draw the main orange shape
                draw.polygon(points, fill=color)
                
                
                
            elif shape_type == 'heart':
                # Heart shape
                 # Scale and center point
                scale = size / 100
                cx, cy = x_pos, y_pos
                
                # Define heart points relative to center (normalized to 0-100 range)
                relative_points = [
                    (0, -15),    # Top center
                    (-5, -20),   # Top left curve
                    (-10, -25),
                    (-20, -30),
                    (-25, -31),
                    (-30, -31),
                    (-35, -30),
                    (-40, -28),
                    (-43, -25),
                    (-45, -20),
                    (-46, -15),
                    (-45, -10),
                    (-43, -5),
                    (-40, 0),    # Left mid
                    (-35, 5),
                    (-30, 10),
                    (-25, 15),
                    (-20, 20),
                    (-15, 25),
                    (-10, 30),
                    (-5, 35),
                    (0, 40),     # Bottom point
                    (5, 35),
                    (10, 30),
                    (15, 25),
                    (20, 20),
                    (25, 15),
                    (30, 10),
                    (35, 5),
                    (40, 0),     # Right mid
                    (43, -5),
                    (45, -10),
                    (46, -15),
                    (45, -20),
                    (43, -25),
                    (40, -28),
                    (35, -30),
                    (30, -31),
                    (25, -31),
                    (20, -30),
                    (15, -28),
                    (10, -25),
                    (5, -20),
                ]
                
                # Convert relative points to absolute positions
                points = [(cx + x * scale, cy + y * scale) for x, y in relative_points]
                
                # Draw the polygon
                draw.polygon(points, fill=color)
            
            elif shape_type == 'star':
                # Star shape
                cx, cy = x_pos, y_pos
                outer_radius = int(size // 2)
                inner_radius = int(outer_radius // 2)
                
                points = []
                for i in range(10):
                    angle = 2 * math.pi * i / 10 - math.pi / 2
                    radius = inner_radius if i % 2 else outer_radius
                    x = int(cx + radius * math.cos(angle))
                    y = int(cy + radius * math.sin(angle))
                    points.append((x, y))
                color
                draw.polygon(points, fill=color)
            
            elif shape_type == 'zzz':
                # Z's for sleepy emotion
                z_size = size // 3
                
                for i in range(3):
                    z_offset_x = (i - 1) * (z_size // 2)
                    z_offset_y = (i - 1) * (z_size // 2)
                    
                    current_z_size = int(z_size * (0.7 + i * 0.15))
                    
                    z_x = x_pos + z_offset_x
                    z_y = y_pos + z_offset_y - current_z_size
                    
                    z_points = [
                        (z_x - current_z_size//2, z_y),
                        (z_x + current_z_size//2, z_y),
                        (z_x - current_z_size//2, z_y + current_z_size),
                        (z_x + current_z_size//2, z_y + current_z_size)
                    ]
                    
                    line_width = max(1, current_z_size//8)
                    draw.line([z_points[0], z_points[1]], fill=color, width=line_width)
                    draw.line([z_points[1], z_points[2]], fill=color, width=line_width)
                    draw.line([z_points[2], z_points[3]], fill=color, width=line_width)
    
    def update_display(self):
        """Update the display with the current emotion"""
        try:
            # Create a new image
            image = Image.new("RGB", (self.config.WIDTH, self.config.HEIGHT), self.config.BACKGROUND_COLOR)
            draw = ImageDraw.Draw(image)
            
            # Get eye shapes based on current emotion
            shapes = self.get_emotion_shapes(self.current_emotion)
            
            # Calculate eye positions
            left_x = (self.config.WIDTH // 2) - (self.config.DOT_SPACING // 2)
            right_x = (self.config.WIDTH // 2) + (self.config.DOT_SPACING // 2)
            
            # Draw both eyes
            self.draw_eye(
                draw,
                left_x,
                shapes['left'],
                shapes['size_left'],
                shapes['dx_left'],
                shapes['dy_left'],
                shapes['color_left']
            )
            
            self.draw_eye(
                draw,
                right_x,
                shapes['right'],
                shapes['size_right'],
                shapes['dx_right'],
                shapes['dy_right'],
                shapes['color_right']
            )
            
            # Display the image
            self.disp.ShowImage(image)
            #print(f"Display updated: Emotion={self.current_emotion.name}, Blinking={self.is_blinking}")
            
        except Exception as e:
            print(f"Error updating display: {e}")
    
    def animation_loop(self):
        """Main animation loop that updates blinking and display"""
        self._running = True
        last_update_time = time.time()
        
        try:
            while self._running:
                # Check if blink state has changed
                blink_changed = self.update_blink_state()
                
                # Update display if needed
                if blink_changed:
                    self.update_display()
                
                # Sleep to prevent high CPU usage
                time.sleep(0.02)
                
        except Exception as e:
            print(f"Error in animation loop: {e}")
        finally:
            self._running = False
    
    def start(self):
        """Start the animation thread"""
        if self._thread is None or not self._thread.is_alive():
            self._thread = threading.Thread(target=self.animation_loop, daemon=True)
            self._thread.start()
            print("Animation thread started")
            return True
        return False
    
    def stop(self):
        """Stop the animation thread"""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
            success = not self._thread.is_alive()
            print(f"Animation thread stopped: {success}")
            return success
        return True
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.stop()
            if hasattr(self, 'disp'):
                self.disp.module_exit()
                print("Display resources cleaned up")
        except Exception as e:
            print(f"Error during cleanup: {e}")


# Example usage
if __name__ == "__main__":
    try:
        face = FaceController()
        face.start()
        
        # Cycle through all emotions
        emotions = list(Emotion)
        for emotion in emotions:
            print(f"Setting emotion: {emotion.name}")
            face.set_emotion(emotion)
            time.sleep(5)
        
        # Keep running until interrupted
        print("Animation running. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        if 'face' in locals():
            face.cleanup()