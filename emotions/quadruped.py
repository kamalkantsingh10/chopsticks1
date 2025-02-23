import time
from core.enums import Emotion

class EmotionalBehaviors:
    def __init__(self, controller):
        """
        Initialize with a reference to the QuadrupedController
        
        Args:
            controller: QuadrupedController instance
        """
        self.controller = controller
        self.base_height = 38  # Default standing height from POSES['stand']
        
    def express_emotion(self, emotion):
        """
        Express an emotion by taking a specific stance
        
        Args:
            emotion (str): Emotion from Emotion enum
        """
        # Start from stand position if needed
        if self.controller.current_pose != "stand":
            return
        
        print(f"Expressing emotion: {emotion}")
        
        # Call the appropriate emotion method
        if emotion == Emotion.HAPPY:
            self._happy()
        elif emotion == Emotion.SAD:
            self._sad()
        elif emotion == Emotion.EXCITED:
            self._excited()
        elif emotion == Emotion.ALERT:
            self._alert()
        elif emotion == Emotion.CURIOUS:
            self._curious()
        elif emotion == Emotion.SLEEPY:
            self._sleepy()
        elif emotion == Emotion.LOVING:
            self._loving()
        elif emotion == Emotion.GRUMPY:
            self._grumpy()
        elif emotion == Emotion.SCARED:
            self._scared()
        elif emotion == Emotion.MISCHIEVOUS:
            self._mischievous()
        elif emotion == Emotion.NEUTRAL:
            self._neutral()
        else:
            print(f"Unknown emotion: {emotion}")
    
    def _happy(self):
        """Happy emotion - raised, alert stance with a slight bounce"""
        positions = {
            'front_right': (3, self.base_height + 5),
            'front_left': (3, self.base_height + 5),
            'back_right': (-2, self.base_height),
            'back_left': (-2, self.base_height)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)
    
    def _sad(self):
        """Sad emotion - drooping front legs"""
        positions = {
            'front_right': (0, self.base_height - 10),
            'front_left': (0, self.base_height - 10),
            'back_right': (0, self.base_height),
            'back_left': (0, self.base_height)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)
    
    def _excited(self):
        """Excited emotion - raised stance ready to move"""
        positions = {
            'front_right': (5, self.base_height + 7),
            'front_left': (5, self.base_height + 7),
            'back_right': (-3, self.base_height + 3),
            'back_left': (-3, self.base_height + 3)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)
    
    def _alert(self):
        """Alert emotion - standing tall and stiff"""
        positions = {
            'front_right': (0, self.base_height + 8),
            'front_left': (0, self.base_height + 8),
            'back_right': (0, self.base_height + 5),
            'back_left': (0, self.base_height + 5)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)
    
    def _curious(self):
        """Curious emotion - leaning forward with front legs extended"""
        positions = {
            'front_right': (8, self.base_height + 3),
            'front_left': (8, self.base_height + 3),
            'back_right': (-3, self.base_height - 3),
            'back_left': (-3, self.base_height - 3)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)
    
    def _sleepy(self):
        """Sleepy emotion - lowered stance"""
        positions = {
            'front_right': (0, self.base_height - 15),
            'front_left': (0, self.base_height - 15),
            'back_right': (0, self.base_height - 10),
            'back_left': (0, self.base_height - 10)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)
    
    def _loving(self):
        """Loving emotion - leaning forward with legs close together"""
        positions = {
            'front_right': (3, self.base_height),
            'front_left': (3, self.base_height),
            'back_right': (-3, self.base_height - 5),
            'back_left': (-3, self.base_height - 5)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)
    
    def _grumpy(self):
        """Grumpy emotion - hunched posture"""
        positions = {
            'front_right': (-3, self.base_height - 5),
            'front_left': (-3, self.base_height - 5),
            'back_right': (3, self.base_height - 3),
            'back_left': (3, self.base_height - 3)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)
    
    def _scared(self):
        """Scared emotion - cowering back, braced stance"""
        positions = {
            'front_right': (-10, self.base_height),
            'front_left': (-10, self.base_height),
            'back_right': (-5, self.base_height - 8),
            'back_left': (-5, self.base_height - 8)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)
    
    def _mischievous(self):
        """Mischievous emotion - low crouch, ready to pounce"""
        positions = {
            'front_right': (8, self.base_height - 7),
            'front_left': (8, self.base_height - 7),
            'back_right': (-3, self.base_height - 5),
            'back_left': (-3, self.base_height - 5)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)
    
    def _neutral(self):
        """Neutral emotion - standard standing position"""
        positions = {
            'front_right': (0, self.base_height),
            'front_left': (0, self.base_height),
            'back_right': (0, self.base_height),
            'back_left': (0, self.base_height)
        }
        
        for leg_name, pos in positions.items():
            self.controller.legs[leg_name].move(*pos)