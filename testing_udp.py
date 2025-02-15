# On Pi Zero (server.py)
import socket
import json
from threading import Thread
import RPi.GPIO as GPIO

from controllers.audio import AudioController
from core.enums import Emotion, Intensity


class HardwareController:
    def __init__(self):
        # Initialize your hardware
        GPIO.setmode(GPIO.BCM)
        # self.motor = Motor(pin1, pin2)
        # self.display = Display()
        
        # UDP Server setup
        self.UDP_IP = "0.0.0.0"
        self.UDP_PORT = 5005
        print("setting up server")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        print("server setup")
        self.controller = AudioController()
        
    def handle_command(self, command_dict):
        value = command_dict.get('value')
        self.controller.speak(value, Emotion.HAPPY, Intensity.NORMAL)
        
        
    
    def start(self):
        print("starting server")
        while True:
            data, addr = self.sock.recvfrom(1024)
            print("recieved:"+ str(data)+" , "+ str(addr))
            try:
                command = json.loads(data.decode())
                self.handle_command(command)
            except json.JSONDecodeError:
                print("Invalid command format")

# Run the controller
controller = HardwareController()
controller.start()