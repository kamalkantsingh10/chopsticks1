from robot_hat import Servo
import time

FRONT_RIGHT_LEG_PINS = (5, 7)
FRONT_LEFT_LEG_PINS =  (4,6)
BACK_RIGHT_LEG_PINS = (8, 10)
BACK_LEFT_LEG_PINS =  (9,11)
class TheoJansenLeg:
    def __init__(self, inner_pin, outer_pin):
        self.inner_servo = Servo(f"P{inner_pin}")
        self.outer_servo = Servo(f"P{outer_pin}")
        self.delay = 0.0
        self.current_inner = 0
        self.current_outer = 0
        self.reset_position()
        
    def _move_servo_smooth(self, servo, start_angle, end_angle, step=1):
        direction = 1 if end_angle > start_angle else -1
        for angle in range(int(start_angle), int(end_angle), direction):
            servo.angle(angle)
            time.sleep(self.delay)
            
    def reset_position(self):
        self._move_servo_smooth(self.inner_servo, self.current_inner, 0)
        self._move_servo_smooth(self.outer_servo, self.current_outer, 0)
        self.current_inner = 0
        self.current_outer = 0
        
    def move_leg(self, inner_angle, outer_angle):
        actual_inner_angle = -inner_angle
        self._move_servo_smooth(self.inner_servo, self.current_inner, actual_inner_angle)
        time.sleep(0.01)
        self._move_servo_smooth(self.outer_servo, self.current_outer, outer_angle)
        self.current_inner = actual_inner_angle
        self.current_outer = outer_angle

class QuadrupedController:
    def __init__(self):
        self.front_right = TheoJansenLeg(*FRONT_RIGHT_LEG_PINS)
        self.front_left = TheoJansenLeg(*FRONT_LEFT_LEG_PINS)
        self.back_right = TheoJansenLeg(*BACK_RIGHT_LEG_PINS)
        self.back_left = TheoJansenLeg(*BACK_LEFT_LEG_PINS)
        self.raise_angle = 20
        self.lower_angle = -20
        
    def reset_all(self):
        self.front_right.reset_position()
        self.front_left.reset_position()
        self.back_right.reset_position()
        self.back_left.reset_position()
        
    def raise_front(self):
        self.front_right.move_leg(self.raise_angle, self.raise_angle)
        self.front_left.move_leg(self.raise_angle, self.raise_angle)
        self.back_right.move_leg(self.lower_angle/2, self.lower_angle/2)
        self.back_left.move_leg(self.lower_angle/2, self.lower_angle/2)
        
    def lower_front(self):
        self.front_right.move_leg(self.lower_angle, self.lower_angle)
        self.front_left.move_leg(self.lower_angle, self.lower_angle)
        self.back_right.move_leg(self.raise_angle/2, self.raise_angle/2)
        self.back_left.move_leg(self.raise_angle/2, self.raise_angle/2)
        
    def raise_back(self):
        self.back_right.move_leg(self.raise_angle, self.raise_angle)
        self.back_left.move_leg(self.raise_angle, self.raise_angle)
        self.front_right.move_leg(self.lower_angle/2, self.lower_angle/2)
        self.front_left.move_leg(self.lower_angle/2, self.lower_angle/2)
        
    def lower_back(self):
        self.back_right.move_leg(self.lower_angle, self.lower_angle)
        self.back_left.move_leg(self.lower_angle, self.lower_angle)
        self.front_right.move_leg(self.raise_angle/2, self.raise_angle/2)
        self.front_left.move_leg(self.raise_angle/2, self.raise_angle/2)

    def demo_leg(self, leg_name):
        leg = getattr(self, leg_name)
        leg.move_leg(20, 20)
        time.sleep(1)
        leg.move_leg(-20, -20)
        time.sleep(1)
        leg.reset_position()
    
def demo_legs_1by1():
    controller = QuadrupedController()
    legs = ['front_right', 'front_left', 'back_right', 'back_left']
    
    for leg in legs:
        print(f"Testing {leg}...")
        controller.demo_leg(leg)
    time.sleep(1)


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
