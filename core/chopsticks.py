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




class Chopsticks:
    def __init__(self):
        #initialize server for socket
        self.state={ "pose": "sitting",
            "neck_tilt": 0
        }
        self.UDP_IP = "0.0.0.0"
        self.UDP_PORT = 5005
        print("setting up server")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        print("server setup")
        
        #instantiate contoller now
        self.quadruped = QuadrupedController()

        #instantiating head- will move to a conf file.. but now keep it as is
        pan_config = ServoConfig(
        pin=2,
        min_angle=-65,
        max_angle=65,
        default_speed=1.0
        )
    
        tilt_config = ServoConfig(
            pin=3,
            min_angle=-30,
            max_angle=30,
            default_speed=1.0
        )
    
    # Initialize head controller
        self.head = HeadController(pan_config, tilt_config)
        #initialize audio
        self.voice = AudioController()

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
        p1= command_dict.get("p1")
        p2= command_dict.get("p2")

        if p1=="pose":
            self.assume_pose(p2)
        elif p1=="yes or no":
            self.say_yes_no(p2)
        elif p1=="say":
            self.say(p2)
        else:
            print("Invalid please")

    def walk(self):
        pass

    def assume_pose(self, pose):
        #pose is managed though head tilt and body positions
        if pose== Pose.SIT_TALL:
            self.quadruped.move_to_pose(pose)
            self.head.set_base_tilt(tilt_angle= 20)
            self.state["neck_tilt"]=20
            self.state["pose"]=pose
        elif pose== Pose.SIT_LOW:
            self.quadruped.move_to_pose(pose)
            self.head.set_base_tilt(tilt_angle= -30)
            self.state["neck_tilt"]=-30
            self.state["pose"]=pose
        elif pose== Pose.STAND:
            self.quadruped.move_to_pose(pose)
            self.head.set_base_tilt(tilt_angle= -10)
            self.state["neck_tilt"]=-10
            self.state["pose"]=pose
        elif pose== Pose.LIE_DOWN:
            self.quadruped.move_to_pose(pose)
            self.head.set_base_tilt(tilt_angle= -20)
            self.state["neck_tilt"]=-20
            self.state["pose"]=pose
        elif pose== Pose.BOW:
            self.quadruped.move_to_pose(pose)
            self.head.set_base_tilt(tilt_angle= 10)
            self.state["neck_tilt"]=10
            self.state["pose"]=pose
        else :
            print(f"invalid pose: {pose}" )
        

    def say_yes_no(self, expression):
        if expression=="yes":
            self.head.nod_yes(base_tilt=self.state["neck_tilt"] )
        elif  expression=="no":
            self.head.shake_no()
        else:
            print("invalid expression")

    def show_emotion(self):
        pass

    def say(text):
        self.voice.speak(text, Emotion.HAPPY, Intensity.NORMAL)
