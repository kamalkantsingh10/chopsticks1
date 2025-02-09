from robot_hat import Servo
import time

class NeckController:
    """
    Controls the pan-tilt neck mechanism of a robot pet
    Pin 2: Left-right movement (pan)
    Pin 3: Up-down movement (tilt)
    Safety limits: -30 to 30 degrees for both servos
    """
    def __init__(self, pan_pin=2, tilt_pin=3):
        self.pan_servo = Servo(f"P{pan_pin}")   # Left-right movement
        self.tilt_servo = Servo(f"P{tilt_pin}") # Up-down movement
        self.delay = 0.005
        
        # Define safety limits
        self.MAX_ANGLE = 30
        self.MIN_ANGLE = -30
        
        # Initialize position to center
        self.current_pan = 0
        self.current_tilt = 0
        self.center()
        
    def _safe_angle(self, angle):
        """Ensure angle stays within safe limits"""
        return max(min(angle, self.MAX_ANGLE), self.MIN_ANGLE)
        
    def _move_servo_smooth(self, servo, start_angle, end_angle, step=1):
        """Move servo smoothly from start to end angle"""
        direction = 1 if end_angle > start_angle else -1
        for angle in range(start_angle, end_angle, direction):
            safe_angle = self._safe_angle(angle)
            servo.angle(safe_angle)
            time.sleep(self.delay)
            
    def center(self):
        """Return head to center position"""
        self._move_servo_smooth(self.pan_servo, self.current_pan, 0)
        self._move_servo_smooth(self.tilt_servo, self.current_tilt, 0)
        self.current_pan = 0
        self.current_tilt = 0
        
    def look_left(self, angle=30):
        """Turn head left"""
        safe_angle = self._safe_angle(angle)
        self._move_servo_smooth(self.pan_servo, self.current_pan, safe_angle)
        self.current_pan = safe_angle
        
    def look_right(self, angle=30):
        """Turn head right"""
        safe_angle = self._safe_angle(-angle)
        self._move_servo_smooth(self.pan_servo, self.current_pan, safe_angle)
        self.current_pan = safe_angle
        
    def look_up(self, angle=30):
        """Tilt head up"""
        safe_angle = self._safe_angle(angle)
        self._move_servo_smooth(self.tilt_servo, self.current_tilt, safe_angle)
        self.current_tilt = safe_angle
        
    def look_down(self, angle=30):
        """Tilt head down"""
        safe_angle = self._safe_angle(-angle)
        self._move_servo_smooth(self.tilt_servo, self.current_tilt, safe_angle)
        self.current_tilt = safe_angle
        
    def nod_yes(self, cycles=2, angle=20):
        """Nod head up and down"""
        safe_angle = self._safe_angle(angle)
        original_tilt = self.current_tilt
        
        for _ in range(cycles):
            # Look down
            self._move_servo_smooth(self.tilt_servo, original_tilt, -safe_angle)
            # Look up
            self._move_servo_smooth(self.tilt_servo, -safe_angle, safe_angle)
            # Return to starting position
            self._move_servo_smooth(self.tilt_servo, safe_angle, original_tilt)
        
        self.current_tilt = original_tilt
            
    def nod_no(self, cycles=2, angle=20):
        """Shake head left and right"""
        safe_angle = self._safe_angle(angle)
        original_pan = self.current_pan
        
        for _ in range(cycles):
            # Look left
            self._move_servo_smooth(self.pan_servo, original_pan, safe_angle)
            # Look right
            self._move_servo_smooth(self.pan_servo, safe_angle, -safe_angle)
            # Return to starting position
            self._move_servo_smooth(self.pan_servo, -safe_angle, original_pan)
        
        self.current_pan = original_pan

# Usage example:
def demo_neck():
    neck = NeckController()
    
    # Test basic movements
    print("Testing basic movements...")
    neck.look_left()
    time.sleep(1)
    neck.center()
    time.sleep(1)
    neck.look_right()
    time.sleep(1)
    neck.center()
    time.sleep(1)
    neck.look_up()
    time.sleep(1)
    neck.center()
    time.sleep(1)
    neck.look_down()
    time.sleep(1)
    neck.center()
    time.sleep(1)
    
    # Test nodding gestures
    print("Testing nod yes...")
    neck.nod_yes()
    time.sleep(1)
    
    print("Testing nod no...")
    neck.nod_no()
    time.sleep(1)
    
    # Return to center
    neck.center()