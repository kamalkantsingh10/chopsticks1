from robot_hat import Servo
import time
import math
import numpy as np

# Robot Dimensions (mm)
SERVO_SEPARATION = 20   # Distance between servo centers
HORN_LENGTH = 40       # Servo horn length
LOWER_BAR = 71        # Lower bar length

# Define poses as x,y coordinates for each leg
# x values are offsets from center position (SERVO_SEPARATION/2)
# For right legs: positive x is forward
# For left legs: we'll multiply x by -1 before sending to IK
POSES = {
    'stand': {
        'front_right': (10, 50),     # 10mm forward from center
        'front_left': (10, 50),      # 10mm forward from center
        'back_right': (10, 50),
        'back_left': (10, 50),
        'head_tilt':-5
    },
    'sit on 2 legs': {
        'front_right': (20, 50),
        'front_left': (20, 50),
        'back_right': (-10, 30),
        'back_left': (-10, 30),
        'head_tilt':25
    },
    'sit': {
        'front_right': (20, 50),
        'front_left': (20, 50),
        'back_right': (-10, 30),
        'back_left': (-10, 30),
        'head_tilt':-15
    },
    'sit- relaxed': {
        'front_right': (20, 50),
        'front_left': (20, 50),
        'back_right': (-10, 30),
        'back_left': (-10, 30),
        'head_tilt':-25
    },
    'lie': {
        'front_right': (20, 20),
        'front_left': (20, 20),
        'back_right': (-10, 20),
        'back_left': (-10, 20),
        'head_tilt':25
    },
    'bow': {
        'front_right': (20, 20),
        'front_left': (20, 20),
        'back_right': (10, 40),
        'back_left': (10, 40),
        'head_tilt':-25
    },

}

class FiveBarLinkage:
    def __init__(self, inner_pin, outer_pin):
        self.servo_a = Servo(f"P{inner_pin}")  # Left servo
        self.servo_b = Servo(f"P{outer_pin}")  # Right servo
        
        # Mechanism dimensions
        self.d = SERVO_SEPARATION  # Distance between servos
        self.l1 = HORN_LENGTH     # Horn length (both servos)
        self.l2 = LOWER_BAR       # Lower bar length (both sides)
        
        # Current angles
        self.current_a = 0
        self.current_b = 0
        
    def solve_ik(self, x, y):
        """
        Solve inverse kinematics for target point (x,y)
        Returns: (angle_a, angle_b) where:
            angle_a: servo A angle (negative = CCW from left)
            angle_b: servo B angle (positive = CW from right)
        """
        try:
            # Transform target point to account for servo separation
            x_a = x            # Left servo is reference at (0,0)
            x_b = x - self.d   # Right servo is offset by -d
            
            # Calculate distances from each servo to target
            r_a = math.sqrt(x_a**2 + y**2)     # Distance from left servo
            r_b = math.sqrt(x_b**2 + y**2)     # Distance from right servo
            
            # Check if target is reachable
            if r_a > (self.l1 + self.l2) or r_b > (self.l1 + self.l2):
                raise ValueError("Target point out of reach")
            
            # For Servo A (left)
            cos_a2 = (r_a**2 - self.l1**2 - self.l2**2) / (-2 * self.l1 * self.l2)
            a2 = math.acos(max(-1, min(1, cos_a2)))
            a1 = math.atan2(y, x_a) + math.atan2(self.l2 * math.sin(a2), 
                                                self.l1 + self.l2 * math.cos(a2))
            # Angle for servo A (negative for CCW)
            angle_a = -math.degrees(a1)
            
            # For Servo B (right)
            cos_b2 = (r_b**2 - self.l1**2 - self.l2**2) / (-2 * self.l1 * self.l2)
            b2 = math.acos(max(-1, min(1, cos_b2)))
            b1 = math.atan2(y, x_b) - math.atan2(self.l2 * math.sin(b2), 
                                                self.l1 + self.l2 * math.cos(b2))
            # Angle for servo B (positive for CW)
            angle_b = math.degrees(b1)
            
            return angle_a+90, 90-angle_b

        except Exception as e:
            print(f"IK calculation error: {str(e)}")
            return None, None
        
    def move_to(self, x, y):
        """Move the foot point to target x,y position"""
        angles = self.solve_ik(x, y)
        print(f"Target: ({x}, {y}), Angles: {angles}")
        if angles[0] is not None and angles[1] is not None:
            self.servo_a.angle(angles[0])
            self.servo_b.angle(angles[1])
            self.current_a = angles[0]
            self.current_b = angles[1]
            return True
        return False


class FiveBarLinkageLeft():
    def __init__(self, inner_pin, outer_pin):
        self.servo_a = Servo(f"P{inner_pin}")  # Left servo
        self.servo_b = Servo(f"P{outer_pin}")  # Right servo
        
        # Mechanism dimensions
        self.d = SERVO_SEPARATION  # Distance between servos
        self.l1 = HORN_LENGTH     # Horn length (both servos)
        self.l2 = LOWER_BAR       # Lower bar length (both sides)
        
        # Current angles
        self.current_a = 0
        self.current_b = 0
        
    def solve_ik(self, x, y):
        """
        Solve inverse kinematics for target point (x,y)
        Returns: (angle_a, angle_b) where:
            angle_a: servo A angle (negative = CCW from left)
            angle_b: servo B angle (positive = CW from right)
        """
        try:
            # Transform target point to account for servo separation
            x_a = x            # Left servo is reference at (0,0)
            x_b = x - self.d   # Right servo is offset by -d
            
            # Calculate distances from each servo to target
            r_a = math.sqrt(x_a**2 + y**2)     # Distance from left servo
            r_b = math.sqrt(x_b**2 + y**2)     # Distance from right servo
            
            # Check if target is reachable
            if r_a > (self.l1 + self.l2) or r_b > (self.l1 + self.l2):
                raise ValueError("Target point out of reach")
            
            # For Servo A (left)
            cos_a2 = (r_a**2 - self.l1**2 - self.l2**2) / (-2 * self.l1 * self.l2)
            a2 = math.acos(max(-1, min(1, cos_a2)))
            a1 = math.atan2(y, x_a) + math.atan2(self.l2 * math.sin(a2), 
                                                self.l1 + self.l2 * math.cos(a2))
            # Angle for servo A (negative for CCW)
            angle_a = -math.degrees(a1)
            
            # For Servo B (right)
            cos_b2 = (r_b**2 - self.l1**2 - self.l2**2) / (-2 * self.l1 * self.l2)
            b2 = math.acos(max(-1, min(1, cos_b2)))
            b1 = math.atan2(y, x_b) - math.atan2(self.l2 * math.sin(b2), 
                                                self.l1 + self.l2 * math.cos(b2))
            # Angle for servo B (positive for CW)
            angle_b = math.degrees(b1)
            
            return angle_a+90, 90-angle_b

        except Exception as e:
            print(f"IK calculation error: {str(e)}")
            return None, None
        
    def move_to(self, x, y):
        """Move the foot point to target x,y position"""
        angles = self.solve_ik(x, y)
        print(f"Target: ({x}, {y}), Angles: {angles}")
        if angles[0] is not None and angles[1] is not None:
            self.servo_a.angle(angles[0])
            self.servo_b.angle(angles[1])
            self.current_a = angles[0]
            self.current_b = angles[1]
            return True
        return False

class QuadrupedLeg:
    def __init__(self, servo_a_pin, servo_b_pin):
        self.linkage = FiveBarLinkage(servo_a_pin, servo_b_pin)
        self.current_x = SERVO_SEPARATION/2
        self.current_y = 50  # Default height
        
    def move(self, x, y):
        """Move leg end point to x,y position"""
        actual_x = x + SERVO_SEPARATION/2  # Add center offset
        
        success = self.linkage.move_to(actual_x, y)
        if success:
            self.current_x = x  # Store the logical x
            self.current_y = y
        return success

class QuadrupedController:
    def __init__(self):
        # Initialize legs with correct servo pins based on top view layout
        self.legs = {
            'front_left': QuadrupedLeg(5, 4),    # Left front servos (5,4)
            'front_right': QuadrupedLeg(6, 7),   # Right front servos (6,7)
            'back_left': QuadrupedLeg(8, 11),    # Left back servos (8,11)
            'back_right': QuadrupedLeg(9, 10)    # Right back servos (9,10)
        }
        
    def move_to_pose(self, pose_name, transition_time=1.0):
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
            
    def walk(self, num_steps, step_height=20, step_length=20, neutral_height=50):
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

# Test the implementation
if __name__ == "__main__":
    robot = QuadrupedController()
    
    # Test sequence
    print("Testing poses...")
    
    # Stand
    print("Standing...")
    robot.move_to_pose('stand')
    time.sleep(1)
    
    # Sit
    print("Sitting...")
    robot.move_to_pose('sit')
    time.sleep(1)
    
    # Lie down
    print("Lying down...")
    robot.move_to_pose('lie')
    time.sleep(1)
    
    # Bow
    print("Bowing...")
    robot.move_to_pose('bow')
    time.sleep(1)
    
    # Alert
    print("Alert stance...")
    robot.move_to_pose('alert')
    time.sleep(1)
    
    # Back to stand
    print("Standing...")
    robot.move_to_pose('stand')