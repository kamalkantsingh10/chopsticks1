from robot_hat import Servo
import time
import math
import numpy as np
from hw_drivers.legs.inverse_kinematics import QuadrupedLeg_right, QuadrupedLeg_left


POSES = {
    'stand': {
        'front_right': (0, 40),     # 10mm forward from center
        'front_left': (0, 40),      # 10mm forward from center
        'back_right': (0, 40),
        'back_left': (0, 40)
    },
    'sit-tall': {
        'front_right': (-40, 70),
        'front_left': (-40, 70),
        'back_right': (15, 26),
        'back_left': (15, 26)
    },
    'sit-low': {
        'front_right': (0, 40),     # 10mm forward from center
        'front_left': (0, 40),
        'back_right': (15, 5),
        'back_left': (15, 5)
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
            
    def walk(self, num_steps, step_height=10, step_length=20, neutral_height=35):
        """
        Walking gait implementation with consistent x-direction
        step_height: Height of leg lift during step
        step_length: Length of each step
        neutral_height: Default standing height
        """
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
        self.move_to_pose('stand', transition_time=1.0)

    
    def walk_round(self, num_steps, radius=40, step_height=20, neutral_height=50):
        """
        Walking in a circular pattern
        radius: Radius of the circular path (mm)
        step_height: Height of leg lift during step
        neutral_height: Default standing height
        """
        print(f"Walking {num_steps} steps in a circle...")
        
        phase = 0
        step_count = 0
        step_angle = 2 * math.pi / (num_steps * 20)  # Divide circle into small increments
        current_angle = 0
        
        while step_count < num_steps:
            # Calculate positions for each leg based on phase and current angle
            if phase < 0.5:  # First diagonal pair stance phase
                # Calculate base positions as in normal walk
                rf_base = (radius/2 - phase*radius, neutral_height)
                lb_base = (radius/2 - phase*radius, neutral_height)
                
                lf_phase = phase * 2
                lf_base = (-radius/2 + lf_phase*radius, 
                          neutral_height - step_height * math.sin(lf_phase * math.pi))
                
                rb_phase = phase * 2
                rb_base = (-radius/2 + rb_phase*radius,
                          neutral_height - step_height * math.sin(rb_phase * math.pi))
                
            else:  # Second diagonal pair stance phase
                alt_phase = phase - 0.5
                
                rf_phase = alt_phase * 2
                rf_base = (-radius/2 + rf_phase*radius,
                          neutral_height - step_height * math.sin(rf_phase * math.pi))
                
                lb_phase = alt_phase * 2
                lb_base = (-radius/2 + lb_phase*radius,
                          neutral_height - step_height * math.sin(lb_phase * math.pi))
                
                lf_base = (radius/2 - alt_phase*radius, neutral_height)
                rb_base = (radius/2 - alt_phase*radius, neutral_height)
            
            # Rotate positions around circle
            positions = {
                'front_right': (
                    rf_base[0] * math.cos(current_angle) - radius * math.sin(current_angle),
                    rf_base[1]
                ),
                'front_left': (
                    lf_base[0] * math.cos(current_angle) - radius * math.sin(current_angle),
                    lf_base[1]
                ),
                'back_right': (
                    rb_base[0] * math.cos(current_angle) + radius * math.sin(current_angle),
                    rb_base[1]
                ),
                'back_left': (
                    lb_base[0] * math.cos(current_angle) + radius * math.sin(current_angle),
                    lb_base[1]
                )
            }
            
            # Move each leg
            for leg_name, pos in positions.items():
                self.legs[leg_name].move(*pos)
            
            time.sleep(0.02)
            
            # Update phase and angle
            phase = (phase + 0.05) % 1.0
            current_angle = (current_angle + step_angle) % (2 * math.pi)
            
            if phase < 0.05:
                step_count += 1
                print(f"Step {step_count}/{num_steps}")
        
        print("Returning to stand...")
        self.move_to_pose('stand', transition_time=1.0)