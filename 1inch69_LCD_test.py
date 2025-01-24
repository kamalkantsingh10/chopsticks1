#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from hw_drivers.display import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 22
BL = 4
bus = 0 
device = 0 
logging.basicConfig(level = logging.DEBUG)

try:
    # display with hardware SPI:pip 
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch69.LCD_1inch69(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch69.LCD_1inch69()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(50)

    Font1 = ImageFont.truetype("/home/kamal/projects/chopsticks1/hw_drivers/display/Font/Font01.ttf", 25)
    Font2 = ImageFont.truetype("/home/kamal/projects/chopsticks1/hw_drivers/display/Font/Font01.ttf", 35)
    Font3 = ImageFont.truetype("/home/kamal/projects/chopsticks1/hw_drivers/display/Font/Font02.ttf", 32)

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width,disp.height ), "WHITE")
    draw = ImageDraw.Draw(image1)

    logging.info("draw point")
    draw.rectangle((25, 10, 26, 11), fill = "BLACK")
    draw.rectangle((25, 25, 27, 27), fill = "BLACK")
    draw.rectangle((25, 40, 28, 43), fill = "BLACK")
    draw.rectangle((25, 55, 29, 59), fill = "BLACK")

    logging.info("draw rectangle")
    draw.rectangle([(40, 10), (90, 60)], fill = "WHITE", outline="BLUE")
    draw.rectangle([(105, 10), (150, 60)], fill = "BLUE")

    logging.info("draw line")
    draw.line([(40, 10), (90, 60)], fill = "RED", width = 1)
    draw.line([(90, 10), (40, 60)], fill = "RED", width = 1)
    draw.line([(130, 65), (130, 115)], fill = "RED", width = 1)
    draw.line([(105, 90), (155, 90)], fill = "RED", width = 1)

    logging.info("draw circle")
    draw.arc((105, 65, 155, 115), 0, 360, fill =(0, 255, 0))
    draw.ellipse((40, 65, 90, 115), fill = (0, 255, 0))

    logging.info("draw text")
    draw.rectangle([(20, 120), (160, 153)], fill = "BLUE")
    draw.text((25, 120), 'Hello world', fill = "RED", font=Font1)
    draw.rectangle([(20,155), (192, 195)], fill = "RED")
    draw.text((21, 155), 'WaveShare', fill = "WHITE", font=Font2)
    draw.text((25, 190), '1234567890', fill = "GREEN", font=Font3)
    text= u"微雪电子"
    draw.text((25, 230),text, fill = "BLUE", font=Font3)
    image1=image1.rotate(0)
    disp.ShowImage(image1)
    time.sleep(2)
    
    image2 = Image.new("RGB", (disp.height,disp.width ), "WHITE")
    draw = ImageDraw.Draw(image2)
    draw.text((60, 2), u"题龙阳县青草湖", fill = 808000, font=Font3)
    draw.text((100, 42), u"元  唐珙", fill = 808080, font=Font3)
    draw.text((60, 82), u"西风吹老洞庭波，", fill = "BLUE", font=Font3)
    draw.text((60, 122), u"一夜湘君白发多。", fill = "RED", font=Font3)
    draw.text((60, 162), u"醉后不知天在水，", fill = "GREEN", font=Font3)
    draw.text((60, 202), u"满船清梦压星河。", fill = "BLACK", font=Font3)
    image2=image2.rotate(0)
    disp.ShowImage(image2)
    time.sleep(2)   
    
    logging.info("show image")
    ImagePath = ["/home/kamal/projects/chopsticks1/trials/LCD_1inch69_4.jpg", "/home/kamal/projects/chopsticks1/trials/LCD_1inch69_6.jpg", "../pic/LCD_1inch69_6.jpg"]
    for i in range(0, 3):
        image = Image.open(ImagePath[i])	
        # image = image.rotate(0)
        disp.ShowImage(image)
        time.sleep(2)
    disp.module_exit()
    logging.info("quit:")
    
except IOError as e:
    logging.info(e)    
    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()