from robot_hat import Servo
import time

FRONT_RIGHT_LEG_PINS = (5, 7)
FRONT_LEFT_LEG_PINS = (4, 6)
BACK_RIGHT_LEG_PINS = (8,10)
BACK_LEFT_LEG_PINS = (9,11)

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
        for angle in range(int(start_angle), int(end_angle), direction * step):
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
    
    def rise(self, angle):
        self.front_right.move_leg(angle, angle)
        self.front_left.move_leg(angle, angle)
        self.back_right.move_leg(angle, angle)
        self.back_left.move_leg(angle, angle)

    def happy(self):
        """Express happiness by doing a little dance"""
        for _ in range(2):  # Repeat the happy dance twice
            # Wiggle front and back alternately
            self.raise_front()
            time.sleep(0.2)
            self.reset_all()
            time.sleep(0.1)
            self.raise_back()
            time.sleep(0.2)
            self.reset_all()
            time.sleep(0.1)
        self.reset_all()

    def sad(self):
        """Express sadness by lowering front and drooping"""
        # Lower front legs slowly
        self.front_right.move_leg(-30, -30)
        self.front_left.move_leg(-30, -30)
        time.sleep(1)
        # Slight droop in back
        self.back_right.move_leg(-10, -10)
        self.back_left.move_leg(-10, -10)
        time.sleep(2)
        self.reset_all()

    def excited(self):
        """Express excitement by bouncing up and down"""
        for _ in range(3):  # Bounce three times
            # Rise up
            self.rise(30)
            time.sleep(0.2)
            # Go down
            self.rise(-10)
            time.sleep(0.2)
        self.reset_all()

    def sit(self):
        """Sit command - lower back end and keep front up"""
        # Lower back legs
        self.back_right.move_leg(-40, -40)
        self.back_left.move_leg(-40, -40)
        time.sleep(0.5)
        # Slightly adjust front for balance
        self.front_right.move_leg(10, 10)
        self.front_left.move_leg(10, 10)
        time.sleep(2)  # Hold the sit position

    def stand(self):
        """Stand command - return to neutral standing position"""
        self.reset_all()

    def lie_down(self):
        """Lie down command - lower both front and back"""
        # Lower back first
        self.back_right.move_leg(-40, -40)
        self.back_left.move_leg(-40, -40)
        time.sleep(0.5)
        # Then lower front
        self.front_right.move_leg(-30, -30)
        self.front_left.move_leg(-30, -30)
        time.sleep(2)  # Hold the position

    def beg(self):
        """Beg command - raise front legs up"""
        # Raise front legs high
        self.front_right.move_leg(45, 45)
        self.front_left.move_leg(45, 45)
        # Adjust back legs for balance
        self.back_right.move_leg(-20, -20)
        self.back_left.move_leg(-20, -20)
        time.sleep(2)  # Hold the begging position
        self.reset_all()

    def stretch(self):
        """Do a playful stretch"""
        # Front legs forward stretch
        self.front_right.move_leg(-30, 20)
        self.front_left.move_leg(-30, 20)
        time.sleep(1)
        # Back legs stretch
        self.back_right.move_leg(20, -30)
        self.back_left.move_leg(20, -30)
        time.sleep(1)
        self.reset_all()

    def wag(self):
        """Wag movement to show happiness"""
        for _ in range(4):  # Wag 4 times
            # Move back legs right
            self.back_right.move_leg(15, 15)
            self.back_left.move_leg(-15, -15)
            time.sleep(0.2)
            # Move back legs left
            self.back_right.move_leg(-15, -15)
            self.back_left.move_leg(15, 15)
            time.sleep(0.2)
        self.reset_all()

    def greet(self):
        """Greeting behavior combining multiple movements"""
        self.wag()
        time.sleep(0.5)
        self.excited()
        time.sleep(0.5)
        self.beg()
        
    
    def walk(self, speed):
        if speed <= 0:
            raise ValueError("Speed must be positive")
        
        # Configuration parameters
        base_delay = 1.0 / speed  # Base timing unit
        step_delay = base_delay * 0.25  # Individual step timing
        
        # Movement parameters - different for inner and outer servos
        inner_lift = 15  # Inner servo lift angle
        outer_lift = 5  # Outer servo lift angle
        inner_push = -15  # Inner servo push angle
        outer_push = -25  # Outer servo push angle
        
        # Neutral position slightly forward-leaning for stability
        neutral_inner = -10
        neutral_outer = 10
        
        def move_pair(leg1, leg2, inner_angle, outer_angle):
            """Helper to move a pair of legs together"""
            leg1.move_leg(inner_angle, outer_angle)
            leg2.move_leg(inner_angle, outer_angle)
            time.sleep(step_delay)
        
        # Walking cycle
        try:
            while True:  # Can be interrupted with Ctrl+C
                # Phase 1: Lift and forward swing diagonal pair (FR + BL)
                move_pair(self.front_right, self.back_left, inner_lift, outer_lift)
                
                # Phase 2: Plant and push with diagonal pair (FR + BL)
                move_pair(self.front_right, self.back_left, inner_push, outer_push)
                
                # Phase 3: Other legs push back while lifted legs move
                move_pair(self.front_left, self.back_right, inner_push*0.7, outer_push*0.7)
                time.sleep(step_delay * 0.5)
                
                # Phase 4: Lift and forward swing other diagonal pair (FL + BR)
                move_pair(self.front_left, self.back_right, inner_lift, outer_lift)
                
                # Phase 5: Plant and push with other diagonal pair (FL + BR)
                move_pair(self.front_left, self.back_right, inner_push, outer_push)
                
                # Phase 6: First pair pushes back while second pair moves
                move_pair(self.front_right, self.back_left, inner_push*0.7, outer_push*0.7)
                time.sleep(step_delay * 0.5)
                
        except KeyboardInterrupt:
            # Graceful shutdown - return to neutral
            all_legs = [self.front_right, self.front_left, self.back_right, self.back_left]
            for leg in all_legs:
                leg.move_leg(neutral_inner, neutral_outer)


    def demo_behaviors(self):
        """Demonstrate all robot behaviors with descriptions"""
        
        print("\n=== Starting Robot Behavior Demo ===\n")
        
        # Basic position and movement demo
        print("1. Basic standing position...")
        self.stand()
        time.sleep(2)
        
        print("\n2. Demonstrating basic commands:")
        print("- Sitting...")
        self.sit()
        time.sleep(2)
        
        print("- Standing...")
        self.stand()
        time.sleep(1)
        
        print("- Lying down...")
        self.lie_down()
        time.sleep(2)
        
        print("- Standing back up...")
        self.stand()
        time.sleep(1)
        
        print("\n3. Demonstrating emotions:")
        print("- Happy dance!")
        self.happy()
        time.sleep(1)
        
        print("- Showing excitement!")
        self.excited()
        time.sleep(1)
        
        print("- Wagging...")
        self.wag()
        time.sleep(1)
        
        print("- Acting sad...")
        self.sad()
        time.sleep(1)
        
        print("\n4. Special behaviors:")
        print("- Morning stretch...")
        self.stretch()
        time.sleep(1)
        
        print("- Begging...")
        self.beg()
        time.sleep(1)
        
        print("\n5. Final greeting performance...")
        self.greet()
        
        print("\nReturning to neutral position...")
        self.stand()
        
        print("\n=== Demo Complete! ===")


def demo_legs_1by1():
    controller = QuadrupedController()
    legs = ['front_right', 'front_left', 'back_right', 'back_left']
    
    for leg in legs:
        print(f"Testing {leg}...")
        controller.demo_leg(leg)
    time.sleep(1)

def demo_walk(speed=1):
    controller = QuadrupedController()
    
    print("Testing walk...")
    controller.demo_behaviors()
    

def demo_legs():
    controller = QuadrupedController()
    
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


