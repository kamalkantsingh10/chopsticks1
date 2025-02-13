from robot_hat import Servo
import time

# Leg servo pin assignments
FRONT_RIGHT_LEG_PINS = (6, 7)   
FRONT_LEFT_LEG_PINS = (5,4)    
BACK_RIGHT_LEG_PINS = (9, 10)   
BACK_LEFT_LEG_PINS = (8,11)    

class QuadrupedLeg:
    def __init__(self, inner_pin, outer_pin):
        self.inner_servo = Servo(f"P{inner_pin}")
        self.outer_servo = Servo(f"P{outer_pin}")
        self.current_inner = 0
        self.current_outer = 0
        self.MIN_ANGLE = -35
        self.MAX_ANGLE = 35
        
    def _clamp_angle(self, angle):
        return max(self.MIN_ANGLE, min(self.MAX_ANGLE, angle))
        
    def move(self, inner_angle, outer_angle):
        """Immediately set servo angles with clamping"""
        self.current_inner = self._clamp_angle(inner_angle)
        self.current_outer = self._clamp_angle(outer_angle)
        self.inner_servo.angle(self.current_inner)
        self.outer_servo.angle(self.current_outer)

class QuadrupedController:
    def __init__(self):
        self.legs = {
            'front_right': QuadrupedLeg(*FRONT_RIGHT_LEG_PINS),
            'front_left': QuadrupedLeg(*FRONT_LEFT_LEG_PINS),
            'back_right': QuadrupedLeg(*BACK_RIGHT_LEG_PINS),
            'back_left': QuadrupedLeg(*BACK_LEFT_LEG_PINS)
        }
        self.transition_speed = 50  # Steps per second
        
    def _transition_legs(self, targets, duration):
        """Low-level leg coordination with mechanical constraints"""
        steps = int(duration * self.transition_speed)
        if steps == 0:
            return

        start_positions = {leg: (l.current_inner, l.current_outer) 
                         for leg, l in self.legs.items()}
        
        for step in range(steps):
            t = step / steps
            for leg in self.legs:
                start_in, start_out = start_positions[leg]
                target_in, target_out = targets[leg]
                
                current_in = start_in + (target_in - start_in) * t
                current_out = start_out + (target_out - start_out) * t
                
                self.legs[leg].move(current_in, current_out)
            
            time.sleep(duration/steps)

    def walk(self, steps=10, step_duration=0.4):
        """Dynamic trotting gait with diagonal leg pairs"""
        # Gait parameters (angles in degrees)
        swing_lift = 30    # Height when leg is swinging
        swing_forward = 25 # Forward extension during swing
        push_back = -20    # Rearward push during stance
        
        phase1 = {
            'front_right': (swing_lift, swing_forward),
            'back_left': (swing_lift, swing_forward),
            'front_left': (push_back, push_back),
            'back_right': (push_back, push_back)
        }
        
        phase2 = {
            'front_left': (swing_lift, swing_forward),
            'back_right': (swing_lift, swing_forward),
            'front_right': (push_back, push_back),
            'back_left': (push_back, push_back)
        }
        
        step_time = step_duration/2  # Time per phase
        
        for _ in range(steps):
            # First diagonal pair movement
            self._transition_legs(phase1, step_time)
            # Second diagonal pair movement
            self._transition_legs(phase2, step_time)
        
        # Return to neutral position
        self._transition_legs({
            leg: (0, 0) for leg in self.legs
        }, duration=0.5)
    
    
    
    
    def transition_to_pose(self, pose, duration=1.5):
        """Smoothly transition all legs to new positions"""
        start_angles = {leg: (self.legs[leg].current_inner, 
                            self.legs[leg].current_outer) 
                      for leg in self.legs}
        
        steps = int(duration * self.transition_speed)
        for step in range(steps):
            t = step / steps
            for leg in self.legs:
                start_in, start_out = start_angles[leg]
                target_in, target_out = pose[leg]
                
                current_in = start_in + (target_in - start_in) * t
                current_out = (start_out + (target_out - start_out) * t)
                
                self.legs[leg].move(current_in, current_out)
            
            time.sleep(duration/steps)

    # Defined poses ###########################################################
    @property
    def normal_stand(self):
        return {
            'front_right': (0, 0),
            'front_left': (0, 0),
            'back_right': (0, 0),
            'back_left': (0, 0)
        }
    
    @property
    def alert_stance(self):
        return {
            'front_right': (25, 20),
            'front_left': (25, 20),
            'back_right': (-15, -10),
            'back_left': (-15, -10)
        }
    
    @property
    def sitting(self):
        return {
            'front_right': (10, 5),
            'front_left': (10, 5),
            'back_right': (-35, -30),
            'back_left': (-35, -30)
        }
    
    @property
    def lie_down(self):
        return {
            'front_right': (-35, -30),
            'front_left': (-35, -30),
            'back_right': (-35, -30),
            'back_left': (-35, -30)
        }
    
    @property
    def play_bow(self):
        return {
            'front_right': (-35, -30),
            'front_left': (-35, -30),
            'back_right': (45, 40),
            'back_left': (45, 40)
        }
    
    @property
    def stretch(self):
        return {
            'front_right': (45, 40),
            'front_left': (45, 40),
            'back_right': (-35, -30),
            'back_left': (-35, -30)
        }
    
    @property
    def sprint_ready(self):
        return {
            'front_right': (-20, -15),
            'front_left': (-20, -15),
            'back_right': (-30, -25),
            'back_left': (-30, -25)
        }
    
    @property
    def sleeping(self):
        return {
            'front_right': (-35, -35),
            'front_left': (-35, -35),
            'back_right': (-35, -35),
            'back_left': (-35, -35)
        }
    
    @property
    def beg(self):
        return {
            'front_right': (45, 40),
            'front_left': (45, 40),
            'back_right': (-25, -20),
            'back_left': (-25, -20)
        }
    
    @property
    def crouching(self):
        return {
            'front_right': (-25, -20),
            'front_left': (-25, -20),
            'back_right': (-30, -25),
            'back_left': (-30, -25)
        }

# Example usage
if __name__ == "__main__":
    bot = QuadrupedController()
    
    # Morning routine demonstration
    print("rise up...")
    bot.transition_to_pose(bot.normal_stand, duration=1)
    time.sleep(1)
    
    # print("Stretching...")
    # bot.transition_to_pose(bot.stretch, duration=1.5)
    # time.sleep(0.5)
    # bot.transition_to_pose(bot.normal_stand, duration=1)
    
    # print("Playful greeting!")
    # bot.transition_to_pose(bot.play_bow, duration=1)
    # time.sleep(0.5)
    # bot.transition_to_pose(bot.normal_stand, duration=0.8)
    
    # print("Going for a walk...")
    # # Implement walking gait pattern here
    # time.sleep(2)
    
    # print("Time to rest...")
    # bot.transition_to_pose(bot.lie_down, duration=3)
    # bot.transition_to_pose(bot.sleeping, duration=2)

    # print("going to sleep..")
    # bot.transition_to_pose(bot.sleeping, duration=1)
    # time.sleep(1)
    print("getup")
    bot.transition_to_pose(bot.sitting, duration=1)
    print("sit")
    # bot.walk(steps=8, step_duration=1)
   