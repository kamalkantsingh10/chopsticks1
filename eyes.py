import os
import sys
import time
import random
import logging
import spidev as SPI
from hw_drivers.display import LCD_1inch69 as LCD
from PIL import Image, ImageDraw

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
DOT_SIZE = 39
DOT_COLOR = (50, 255, 50)  # Light green
DOT_SPACING = 80  # Space between dots

# Calculate center positions for both dots
CENTER_Y = HEIGHT // 2
LEFT_X = (WIDTH // 2) - (DOT_SPACING // 2)
RIGHT_X = (WIDTH // 2) + (DOT_SPACING // 2)

class RobotDisplay:
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
        
        # Initialize single blinking state for both dots
        self.last_blink = time.time()
        self.blink_interval = random.uniform(2.0, 5.0)
        self.is_blinking = False
        self.blink_duration = random.uniform(0.1, 0.3)

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
            # Set new random duration for this blink
            self.blink_duration = random.uniform(0.1, 0.3)
        
        # Check if current blink should end
        if self.is_blinking and current_time - self.last_blink > self.blink_duration:
            self.is_blinking = False
            # Set new random interval until next blink
            self.blink_interval = random.uniform(2.0, 5.0)

    def draw_single_dot(self, draw, center_x):
        """Draw a single dot at the specified x position"""
        x1 = center_x - DOT_SIZE // 2
        y1 = CENTER_Y - DOT_SIZE // 2
        x2 = x1 + DOT_SIZE
        y2 = y1 + DOT_SIZE
        
        if self.is_blinking:
            # During blink, draw a thin horizontal line
            blink_height = max(3, DOT_SIZE // 8)
            y_mid = (y1 + y2) // 2
            y_blink1 = y_mid - blink_height // 2
            y_blink2 = y_mid + blink_height // 2
            self.draw_rounded_rectangle(draw, 
                                     [x1, y_blink1, x2, y_blink2],
                                     blink_height // 2, 
                                     DOT_COLOR)
        else:
            # Normal state - draw the full rounded square
            self.draw_rounded_rectangle(draw, 
                                     [x1, y1, x2, y2],
                                     DOT_SIZE // 4, 
                                     DOT_COLOR)

    def draw_dots(self):
        """Draw both dots with current blink state"""
        # Update blink state once for both dots
        self.update_blink()
        
        # Create new image with black background
        image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw both dots
        self.draw_single_dot(draw, LEFT_X)
        self.draw_single_dot(draw, RIGHT_X)
        
        # Display the image
        self.disp.ShowImage(image)

    def run(self):
        """Main loop to continuously update the display"""
        try:
            while True:
                self.draw_dots()
                time.sleep(0.05)  # Small delay for smooth animation
                
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        """Clean up display resources"""
        self.disp.module_exit()

def main():
    """Run the display"""
    display = RobotDisplay()
    try:
        display.run()
    except KeyboardInterrupt:
        print("Display stopped by user")
        display.cleanup()

if __name__ == "__main__":
    main()