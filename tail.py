from robot_hat import Servo
import time
from threading import Thread
import math

class TailController:
    """
    Controls the tail servo of a robot pet, handling different emotional states
    The tail is mounted at 45 degrees to the robot's length
    """
    def __init__(self, pin_number=1):
        self.servo = Servo(f"P{pin_number}")
        self.is_running = False
        self.background_thread = None
        self.delay = 0.005
        
        # Define movement parameters
        self.normal_angle = 15  # Small angle for normal state
        self.emotion_angle = 30  # Larger angle for emotional states
        
    def _move_servo(self, start_angle, end_angle, step=1):
        """Helper method to move servo smoothly between angles"""
        direction = 1 if end_angle > start_angle else -1
        for angle in range(start_angle, end_angle, direction):
            # Compensate for 45-degree mounting angle
            adjusted_angle = angle * math.cos(math.pi/4)  # 45 degrees in radians
            self.servo.angle(adjusted_angle)
            time.sleep(self.delay)
            
    def _normal_behavior(self):
        """Continuous gentle wagging for normal state"""
        while self.is_running:
            # Move right
            self._move_servo(0, self.normal_angle)
            # Move left
            self._move_servo(self.normal_angle, -self.normal_angle)
            # Return to center
            self._move_servo(-self.normal_angle, 0)
            time.sleep(1)  # Pause between wags
            
    def start_normal(self):
        """Start normal tail wagging behavior in background"""
        if not self.is_running:
            self.is_running = True
            self.background_thread = Thread(target=self._normal_behavior)
            self.background_thread.start()
            
    def stop_normal(self):
        """Stop normal tail wagging behavior"""
        self.is_running = False
        if self.background_thread:
            self.background_thread.join()
        self.servo.angle(0)
            
    def happy_wag(self):
        """One-time enthusiastic tail wag"""
        self.stop_normal()  # Stop normal behavior if running
        
        # Quick, enthusiastic wag
        self._move_servo(0, self.emotion_angle)
        self._move_servo(self.emotion_angle, -self.emotion_angle)
        self._move_servo(-self.emotion_angle, 0)
        
    def sad_wag(self):
        """One-time slow, droopy tail movement"""
        self.stop_normal()  # Stop normal behavior if running
        
        # Slow, deliberate movement
        original_delay = self.delay
        self.delay = 0.015  # Slower movement for sad emotion
        
        self._move_servo(0, -self.emotion_angle)
        time.sleep(0.5)  # Pause in drooped position
        self._move_servo(-self.emotion_angle, 0)
        
        self.delay = original_delay  # Restore original delay

# Usage example:
def demo_tail():
    tail = TailController()
    
    # Test normal behavior
    print("Starting normal behavior...")
    tail.start_normal()
    time.sleep(5)  # Let it wag normally for 5 seconds
    
    # Test happy emotion
    print("Testing happy wag...")
    tail.stop_normal()
    tail.happy_wag()
    time.sleep(1)
    
    # Test sad emotion
    print("Testing sad wag...")
    tail.sad_wag()
    time.sleep(1)
    
    # Return to normal behavior
    print("Returning to normal behavior...")
    tail.start_normal()
    time.sleep(5)
    tail.stop_normal()