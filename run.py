import time
import socket
from controllers.audio import AudioController
from controllers.face import FaceController
from controllers.head import HeadController
from controllers.quadruped import QuadrupedController
from controllers.tail import TailController
from controllers.indicator import Indicator


from typing import Dict, List, Optional
from dataclasses import dataclass
import json

from core.enums import Emotion, Intensity,Position, ServoConfig, Pose




class Chopsticks ():
    def __init__(self):
        #initialize server for socket
        self.current_state={
            "pose": "sitting"
            "neck_tilt": 10
        }
        self.UDP_IP = "0.0.0.0"
        self.UDP_PORT = 5005
        print("setting up server")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        print("server setup")
        
        #instantiate contoller now
        self.quadruped = QuadrupedController()

    def start(self):
        print("starting server now and starting to listen")
        while True:
            data, addr = self.sock.recvfrom(1024)
            print("recieved:"+ str(data)+" , "+ str(addr))
            try:
                command = json.loads(data.decode())
                self.route(command)
            except json.JSONDecodeError:
                print("Invalid command format")
    
    def route(self, command_dict):
        pass

    def walk(self):
        pass

    def assume_pose(self, pose):
        if pose== Pose.SIT_TALL:
            self.quadruped.move_to_pose(pose)
            
        elif pose== Pose.SIT_LOW:
            self.quadruped.move_to_pose(pose)
        elif pose== Pose.STAND:
            self.quadruped.move_to_pose(pose)
        elif pose== Pose.LIE_DOWN:
            self.quadruped.move_to_pose(pose)
        elif pose== Pose.BOW:
            self.quadruped.move_to_pose(pose)
        

        pass

    def say_yes_no(self):
        pass

    def show_emotion(self):
        pass

