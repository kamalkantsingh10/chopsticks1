
from core.enums import Intensity,ServoConfig
from robot_hat import Servo
from threading import Thread, Lock
import time


class TailController:
    
    def __init__(self, config: ServoConfig):
        self.config = config
        self.servo = Servo(f"P{config.servo_pin}")
        self.current_angle = 0.0
        self.is_moving = False
        self.emergency_stop = False
        self.movement_lock = Lock()
        self.wag_thread = None

    def wag(self, speed: float, amplitude: float, intensity: Intensity) -> None:
        """
        Create wagging motion.
        Args:
            speed: Wagging frequency (0-1)
            amplitude: Movement range (0-1)
            intensity: Movement intensity
        """
        if self.emergency_stop or (self.wag_thread and self.wag_thread.is_alive()):
            return

        def _wag_motion():
            try:
                # Base delay and angle calculations
                base_delay = 0.01 / speed  # Inverse relationship with speed
                max_angle = self.config.max_angle * amplitude
                
                # Adjust parameters based on intensity
                if intensity == Intensity.HIGH:
                    max_angle *= 1.2
                    base_delay *= 0.7
                elif intensity == Intensity.LOW:
                    max_angle *= 0.8
                    base_delay *= 1.3

                while not self.emergency_stop:
                    # Wag cycle
                    self.set_angle(max_angle, speed)
                    time.sleep(base_delay)
                    self.set_angle(-max_angle, speed)
                    time.sleep(base_delay)

            except Exception as e:
                print(f"Error during wagging: {e}")
                self.stop()

        self.wag_thread = Thread(target=_wag_motion, daemon=True)
        self.wag_thread.start()

    def set_angle(self, angle: float, speed: float) -> None:
        """Move tail to specific angle"""
        if self.emergency_stop:
            return
            
        with self.movement_lock:
            try:
                # Clamp angle to limits
                angle = max(self.config.min_angle, 
                          min(self.config.max_angle, angle))
                
                # Add small delay based on speed for smoother motion
                delay = 0.01 * (1 - speed)
                self.servo.angle(angle)
                time.sleep(delay)
                self.current_angle = angle
                
            except Exception as e:
                print(f"Error setting angle: {e}")
                self.stop()

    def stop(self) -> None:
        """Emergency stop"""
        self.emergency_stop = True
        with self.movement_lock:
            self.servo.angle(0)  # Return to neutral position
            self.is_moving = False

    def cleanup(self) -> None:
        """Release hardware resources"""
        self.stop()
        if self.wag_thread:
            self.wag_thread.join(timeout=1.0)
        self.servo.angle(0)  # Return to neutral position