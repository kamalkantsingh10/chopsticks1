import time
import socket
from controllers.audio import AudioController
from controllers.face import FaceController
from controllers.head import HeadController
from controllers.quadruped import QuadrupedController
from controllers.tail import TailController
from controllers.indicator import Indicator
from emotions.head import Head_Emotions

from typing import Dict, List, Optional
from dataclasses import dataclass
import json

from core.enums import Emotion, Intensity,Position, ServoConfig, Pose




class Chopsticks:
    def __init__(self):
        #initialize server for socket
        self.state={ "pose":Pose.STAND.value,
            "neck_tilt": 0,
            "emotion":Emotion.NEUTRAL
        }
        self.UDP_IP = "0.0.0.0"
        self.UDP_PORT = 5005
        print("setting up server")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        print("server setup")
        
        #instantiate contoller now
        self.quadruped = QuadrupedController()
        print("legs set")
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
        self.head_em = Head_Emotions(self.head)
        print("head configured")
        #initialize audio
        self.voice = AudioController()
        print("speaker set")
        self.face =FaceController()
        self.face.start()
        print("face screen set")
        tail_config = ServoConfig(
            pin=0,
            min_angle=-30,
            max_angle=30,
            default_speed=1.0
        )
        print("tail set")
        self.tail = TailController(tail_config)
        self.indicator= Indicator()
        print("indicator set")

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
        p3= command_dict.get("p3")

        if p1=="pose":
            self.assume_pose(p2)
        elif p1=="yes or no":
            self.say_yes_no(p2)
        elif p1=="say":
            self.say(p2)
        elif p1=="walk":
            self.walk(num_steps=p2, direction=p3)
        elif p1=="dance":
            self.dance()
        elif p1=="emotions":
            self.show_emotion(emotion=p2)
        else:
            print("Invalid please")

    def show_emotion(self, emotion):
        display_emotion= f"{emotion}"
        emotion_to_show= Emotion.NEUTRAL
        if emotion == Emotion.HAPPY.value:
            emotion_to_show= Emotion.HAPPY
        elif emotion==Emotion.SAD.value:
            emotion_to_show= Emotion.SAD
        elif emotion==Emotion.EXCITED.value:
            emotion_to_show= Emotion.EXCITED
        elif emotion==Emotion.CURIOUS.value:
            emotion_to_show= Emotion.CURIOUS
        elif emotion==Emotion.SLEEPY.value:
            emotion_to_show= Emotion.SLEEPY 
        elif emotion==Emotion.LOVING.value:
            emotion_to_show= Emotion.LOVING
        elif emotion==Emotion.GRUMPY.value:
            emotion_to_show= Emotion.GRUMPY
        elif emotion==Emotion.SCARED.value:
            emotion_to_show= Emotion.SCARED
        elif emotion==Emotion.MISCHIEVOUS.value:
            emotion_to_show= Emotion.MISCHIEVOUS
        elif emotion==Emotion.NEUTRAL.value:
            emotion_to_show= Emotion.NEUTRAL
            display_emotion= f"Chopsticks"
        else:
            emotion_to_show= Emotion.NEUTRAL
            display_emotion= f"Chopsticks"

        self.head_em.express(emotion_to_show)
        self.tail.set_emotion(emotion_to_show)
        self.face.set_emotion(emotion_to_show)
        #show body movement for emotion only when standing or if sl
        if self.state["pose"]==Pose.STAND.value:
            self.quadruped.express_emotion(emotion_to_show)
        self.state["emotion"]=emotion_to_show  #setting current set of emotion. this is used for Audio Pitching
        self.indicator.display_text(display_emotion)


   

        
        


    def walk(self, num_steps,direction):
        self.indicator.display_text("walking")
        length=0
        if direction=="front":
            length=30
        elif direction=="back":
            length=-20
        self.quadruped.walk(num_steps=int(num_steps), step_length=length)

    def dance(self):
        self.quadruped.walk(num_steps=8, step_length=0) # bot dances at same place with 0 step length

    def assume_pose(self, pose):
        #pose is managed though head tilt and body positions
        self.indicator.display_text(pose)
        if pose== Pose.SIT_TALL.value:
            self.quadruped.move_to_pose(pose)
            self.head.set_base_tilt(tilt_angle= 20)
            self.state["neck_tilt"]=20
            self.state["pose"]=pose
        elif pose== Pose.SIT_LOW.value:
            self.quadruped.move_to_pose(pose)
            self.head.set_base_tilt(tilt_angle= -30)
            self.state["neck_tilt"]=-30
            self.state["pose"]=pose
        elif pose== Pose.STAND.value:
            self.quadruped.move_to_pose(pose)
            self.head.set_base_tilt(tilt_angle= -10)
            self.state["neck_tilt"]=-10
            self.state["pose"]=pose
        elif pose== Pose.LIE_DOWN.value:
            self.quadruped.move_to_pose(pose)
            self.head.set_base_tilt(tilt_angle= 30)
            self.state["neck_tilt"]=30
            self.state["pose"]=pose
            self.tail.stop()
        elif pose== Pose.BOW.value:
            self.quadruped.move_to_pose(pose)
            self.head.set_base_tilt(tilt_angle= 10)
            self.state["neck_tilt"]=10
            self.state["pose"]=pose
        else :
            print(f"invalid pose: {pose}" )
        

    def say_yes_no(self, expression):
        self.indicator.display_text("yes")
        if expression=="yes":
            self.head.nod_yes(base_tilt=self.state["neck_tilt"] )
        elif  expression=="no":
            self.head.shake_no()
        else:
            print("invalid expression")

    
    def say(self, text):
        self.voice.speak(text, self.state.get("emotion"))
