import os
import sys 
import time
import random
import logging
import spidev as SPI
import math
from hw_drivers.display import LCD_1inch69
from PIL import Image, ImageDraw

RST = 27
DC = 22
BL = 4
bus = 0 
device = 0 

class RobotEyes:
    def __init__(self):
        self.expression = "neutral"
        self.base_size = 100
        self.pupil_size = 50  
        self.blink_state = 1.0
        self.expressions = {
            "happy": ((0, 0), (0, 0), 1.0, 0.7),
            "sad": ((0, 0), (0, 0), 0.7, 1.0),
            "neutral": ((0, 0), (0, 0), 1.0, 1.0),
            "angry": ((0, 0), (0, 0), 0.6, 1.0),
            "surprised": ((0, 0), (0, 0), 1.4, 1.4),
            "excited": ((0, 0), (0, 0), 1.2, 0.8),
            "sleepy": ((0, 0), (0, 0), 0.3, 1.0),
            "blink": ((0, 0), (0, 0), 0.1, 1.0)
        }
        self.current_image = None
        
    def set_expression(self, expression):
        if expression in self.expressions:
            self.expression = expression
            return True
        return False

def draw_robot_eyes(disp, robot_eyes):
    image = Image.new("RGB", (disp.height, disp.width), "#000000")
    draw = ImageDraw.Draw(image)

    left_center = (disp.height//2 - 100, disp.width//2)
    right_center = (disp.height//2 + 100, disp.width//2)
        
    expr = robot_eyes.expressions[robot_eyes.expression]
    
    for eye_center in [left_center, right_center]:
        height_scale = expr[2]
        width_scale = expr[3]
        draw.ellipse((eye_center[0]-robot_eyes.base_size*width_scale,
                     eye_center[1]-robot_eyes.base_size*height_scale,
                     eye_center[0]+robot_eyes.base_size*width_scale,
                     eye_center[1]+robot_eyes.base_size*height_scale),
                     fill="#FFFFFF", outline="#FFFFFF", width=4)
        pupil_x = eye_center[0]
        pupil_y = eye_center[1]
        
        ps = robot_eyes.pupil_size
        draw.ellipse((pupil_x-ps, pupil_y-ps,
                     pupil_x+ps, pupil_y+ps),
                     fill="#000000")
        
        image_rotated = image.rotate(90, expand=True)
    robot_eyes.current_image = image_rotated
    disp.ShowImage(image_rotated)

try:
    disp = LCD_1inch69.LCD_1inch69(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp.Init()
    disp.clear()
    disp.bl_DutyCycle(50)
    
    robot_eyes = RobotEyes()
    expressions = ["happy", "sad", "neutral", "angry", "surprised", "excited", "sleepy", "blink"]
    last_expression = time.time()
    
    draw_robot_eyes(disp, robot_eyes)
    
    while True:
        now = time.time()
        if now - last_expression > random.uniform(2, 4):
            new_expression = random.choice(expressions)
            if robot_eyes.set_expression(new_expression):
                draw_robot_eyes(disp, robot_eyes)
            last_expression = now
        time.sleep(0.05)
except KeyboardInterrupt: 
    disp.module_exit()
    exit()