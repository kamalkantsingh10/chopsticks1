from robot_hat import Servo
import time

# Global pin configurations - To be set based on your setup
# Format: (inner_servo_pin, outer_servo_pin)
FRONT_RIGHT_LEG_PINS = (5, 7)  # Example: (4, 5)
FRONT_LEFT_LEG_PINS =   ( 11,9) # Example: (6, 7)
BACK_RIGHT_LEG_PINS = (8, 10)   # Example: (8, 9)
BACK_LEFT_LEG_PINS =  (6, 4)    # Example: (10, 11)

class TheoJansenLeg:
    """Controls a single Theo Jansen leg with two servos"""
    def __init__(self, inner_pin, outer_pin):
        self.inner_servo = Servo(f"P{inner_pin}")
        self.outer_servo = Servo(f"P{outer_pin}")
        self.delay = 0.005
        
        # Initialize positions
        self.current_inner = 0
        self.current_outer = 0
        self.reset_position()
        
    def _move_servo_smooth(self, servo, start_angle, end_angle, step=1):
        """Move servo smoothly between angles"""
        direction = 1 if end_angle > start_angle else -1
        for angle in range(int(start_angle), int(end_angle), direction):
            servo.angle(angle)
            time.sleep(self.delay)
            
    def reset_position(self):
        """Return leg to neutral position"""
        self._move_servo_smooth(self.inner_servo, self.current_inner, 0)
        self._move_servo_smooth(self.outer_servo, self.current_outer, 0)
        self.current_inner = 0
        self.current_outer = 0
        
    def move_leg(self, inner_angle, outer_angle):
        """
        Move leg to specified angles
        Note: Due to opposite servo orientations, we invert the inner angle
        Adds 20ms delay between starting servos to reduce current spike
        """
        # Invert inner angle due to opposite orientation
        actual_inner_angle = -inner_angle
        
        # Move inner servo first
        self._move_servo_smooth(self.inner_servo, self.current_inner, actual_inner_angle)
        
        # Wait 20ms before starting the second servo
        time.sleep(0.02)  # 20 milliseconds
        
        # Then move outer servo
        self._move_servo_smooth(self.outer_servo, self.current_outer, outer_angle)
        
        self.current_inner = actual_inner_angle
        self.current_outer = outer_angle

class QuadrupedController:
    """Controls all four legs of the robot"""
    def __init__(self):
        # Initialize all legs
        self.front_right = TheoJansenLeg(*FRONT_RIGHT_LEG_PINS)
        self.front_left = TheoJansenLeg(*FRONT_LEFT_LEG_PINS)
        self.back_right = TheoJansenLeg(*BACK_RIGHT_LEG_PINS)
        self.back_left = TheoJansenLeg(*BACK_LEFT_LEG_PINS)
        
        # Movement parameters
        self.raise_angle = 20  # Angle to raise body
        self.lower_angle = -20  # Angle to lower body
        
    def reset_all(self):
        """Reset all legs to neutral position"""
        self.front_right.reset_position()
        self.front_left.reset_position()
        self.back_right.reset_position()
        self.back_left.reset_position()
        
    def raise_front(self):
        """Raise front of the robot"""
        # For raising, inner servo moves down (negative) and outer moves up (positive)
        self.front_right.move_leg(self.raise_angle, self.raise_angle)
        self.front_left.move_leg(self.raise_angle, self.raise_angle)
        # Adjust back legs for stability
        self.back_right.move_leg(self.lower_angle/2, self.lower_angle/2)
        self.back_left.move_leg(self.lower_angle/2, self.lower_angle/2)
        
    def lower_front(self):
        """Lower front of the robot"""
        self.front_right.move_leg(self.lower_angle, self.lower_angle)
        self.front_left.move_leg(self.lower_angle, self.lower_angle)
        # Adjust back legs for stability
        self.back_right.move_leg(self.raise_angle/2, self.raise_angle/2)
        self.back_left.move_leg(self.raise_angle/2, self.raise_angle/2)
        
    def raise_back(self):
        """Raise back of the robot"""
        self.back_right.move_leg(self.raise_angle, self.raise_angle)
        self.back_left.move_leg(self.raise_angle, self.raise_angle)
        # Adjust front legs for stability
        self.front_right.move_leg(self.lower_angle/2, self.lower_angle/2)
        self.front_left.move_leg(self.lower_angle/2, self.lower_angle/2)
        
    def lower_back(self):
        """Lower back of the robot"""
        self.back_right.move_leg(self.lower_angle, self.lower_angle)
        self.back_left.move_leg(self.lower_angle, self.lower_angle)
        # Adjust front legs for stability
        self.front_right.move_leg(self.raise_angle/2, self.raise_angle/2)
        self.front_left.move_leg(self.raise_angle/2, self.raise_angle/2)

# Usage example:
def demo_legs():
    # First set the global pin numbers according to your setup
    # FRONT_RIGHT_LEG_PINS = (4, 5)
    # FRONT_LEFT_LEG_PINS = (6, 7)
    # BACK_RIGHT_LEG_PINS = (8, 9)
    # BACK_LEFT_LEG_PINS = (10, 11)
    
    controller = QuadrupedController()
    
    # Test sequence
    print("Testing leg movements...")
    
    print("Raising front...")
    controller.raise_front()
    time.sleep(2)
    
    print("Resetting position...")
    controller.reset_all()
    time.sleep(1)
    
    print("Lowering front...")
    controller.lower_front()
    time.sleep(2)
    
    print("Resetting position...")
    controller.reset_all()
    time.sleep(1)
    
    print("Raising back...")
    controller.raise_back()
    time.sleep(2)
    
    print("Resetting position...")
    controller.reset_all()
    time.sleep(1)
    
    print("Lowering back...")
    controller.lower_back()
    time.sleep(2)
    
    print("Final reset...")
    controller.reset_all()