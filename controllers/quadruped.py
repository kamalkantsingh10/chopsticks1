from robot_hat import Servo
import time
import math
import numpy as np
from hw_drivers.legs.inverse_kinematics import QuadrupedLeg_right, QuadrupedLeg_left
from core.enums import Emotion, Pose
from emotions.quadruped_1 import EmotionalBehaviors  # Import the new class

POSES = {
    'stand': {
        'front_right': (0, 38),     # 10mm forward from center
        'front_left': (0, 38),      # 10mm forward from center
        'back_right': (0, 38),
        'back_left': (0, 38)
    },
    'sit-tall': {
        'front_right': (-45, 70),
        'front_left': (-45, 70),
        'back_right': (-25, 5),
        'back_left': (-25, 5)
    },
    'sit-low': {
        'front_right': (0, 50),     # 10mm forward from center
        'front_left': (0, 50),
        'back_right': (-13, 10),
        'back_left': (-13, 10)
    },
    'lie-down': {
        'front_right': (-16, 10),
        'front_left': (-16, 10),
        'back_right': (-16, 10),
        'back_left':(-16, 10)
    },
    'bow': {
        'front_right': (0, 20),
        'front_left': (0, 20),
        'back_right': (0, 55),
        'back_left': (0, 55)
    }
}


class QuadrupedController:
    def __init__(self):
        # Initialize legs with correct servo pins based on top view layout
        self.legs = {
            'front_left': QuadrupedLeg_left(5, 4),    # Left front servos (5,4)
            'front_right': QuadrupedLeg_right(6, 7),   # Right front servos (6,7)
            'back_left': QuadrupedLeg_left(8, 11),    # Left back servos (8,11)
            'back_right': QuadrupedLeg_right(9, 10)    # Right back servos (9,10)
        }
        self.current_pose = Pose.SIT_LOW.value
        
        # Initialize emotional behaviors
        self.emotions = EmotionalBehaviors(self)
        
    def move_to_pose(self, pose_name, transition_time=.5):
        """Move to a predefined pose with smooth interpolation"""
        if pose_name not in POSES:
            print(f"Unknown pose: {pose_name}")
            return
            
        pose = POSES[pose_name]
        print(f"Moving to pose: {pose_name}")
        
        # Store starting positions
        start_positions = {
            leg_name: (leg.current_x, leg.current_y)
            for leg_name, leg in self.legs.items()
        }
        
        # Calculate number of interpolation steps
        steps = int(transition_time * 50)  # 50 steps per second
        
        # Perform interpolation
        for step in range(steps + 1):
            t = step / steps  # Interpolation factor (0 to 1)
            
            # Use sine interpolation for smoother acceleration/deceleration
            smooth_t = (1 - math.cos(t * math.pi)) / 2
            
            # Move each leg to interpolated position
            for leg_name, target_pos in pose.items():
                start_x, start_y = start_positions[leg_name]
                target_x, target_y = target_pos
                
                # Calculate interpolated position
                current_x = start_x + (target_x - start_x) * smooth_t
                current_y = start_y + (target_y - start_y) * smooth_t
                
                # Move leg
                self.legs[leg_name].move(current_x, current_y)
            
            # Small delay between steps
            time.sleep(transition_time / steps)
        
        # Update current pose
        self.current_pose = pose_name
            
    def walk(self, num_steps, step_height=10, step_length=20, neutral_height=35):
        """
        Walking gait implementation with consistent x-direction
        step_height: Height of leg lift during step
        step_length: Length of each step
        neutral_height: Default standing height
        """

        print("Standing up first")
        self.move_to_pose(Pose.STAND.value, transition_time=0.5)
        print(f"Walking {num_steps} steps...")
        
        # Initialize phase
        phase = 0
        step_count = 0
        
        # Execute specified number of steps
        while step_count < num_steps:
            # Calculate positions for each leg based on phase
            # Positive x is forward for all legs
            
            # Right front and left back move together (diagonal pairs)
            if phase < 0.5:  # First diagonal pair stance phase
                # Right front leg (on ground, moving backward)
                rf_x = step_length/2 - phase*2*step_length
                rf_y = neutral_height
                
                # Left back leg (on ground, moving backward)
                lb_x = step_length/2 - phase*2*step_length
                lb_y = neutral_height
                
                # Left front leg (in air, moving forward)
                lf_phase = phase * 2
                lf_x = -step_length/2 + lf_phase*step_length
                lf_y = neutral_height - step_height * math.sin(lf_phase * math.pi)
                
                # Right back leg (in air, moving forward)
                rb_phase = phase * 2
                rb_x = -step_length/2 + rb_phase*step_length
                rb_y = neutral_height - step_height * math.sin(rb_phase * math.pi)
                
            else:  # Second diagonal pair stance phase
                alt_phase = phase - 0.5
                
                # Right front leg (in air, moving forward)
                rf_phase = alt_phase * 2
                rf_x = -step_length/2 + rf_phase*step_length
                rf_y = neutral_height - step_height * math.sin(rf_phase * math.pi)
                
                # Left back leg (in air, moving forward)
                lb_phase = alt_phase * 2
                lb_x = -step_length/2 + lb_phase*step_length
                lb_y = neutral_height - step_height * math.sin(lb_phase * math.pi)
                
                # Left front leg (on ground, moving backward)
                lf_x = step_length/2 - alt_phase*2*step_length
                lf_y = neutral_height
                
                # Right back leg (on ground, moving backward)
                rb_x = step_length/2 - alt_phase*2*step_length
                rb_y = neutral_height
            
            # Move all legs to calculated positions
            positions = {
                'front_right': (rf_x, rf_y),
                'front_left': (lf_x, lf_y),
                'back_right': (rb_x, rb_y),
                'back_left': (lb_x, lb_y)
            }
            
            # Move each leg
            for leg_name, pos in positions.items():
                self.legs[leg_name].move(*pos)
            
            # Small delay for smooth motion
            time.sleep(0.02)
            
            # Update phase
            phase = (phase + 0.05) % 1.0
            
            # Count steps (one step is a complete cycle)
            if phase < 0.05:
                step_count += 1
                print(f"Step {step_count}/{num_steps}")
        
        # Return to neutral standing position
        print("Returning to stand...")
        self.move_to_pose(self.current_pose, transition_time=0.5)
    
    def express_emotion(self, emotion):
        """Express an emotion using the emotional behaviors module"""
        # Make sure we're in a standing position first
        if self.current_pose != Pose.STAND.value:
            self.move_to_pose(Pose.STAND.value, transition_time=0.5)
        
        # Delegate to the emotions controller to take the stance
        self.emotions.express_emotion(emotion)
        
        # Update current pose - still technically in a modified stand
        self.current_pose = Pose.STAND.value