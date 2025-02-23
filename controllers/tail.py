from core.enums import Intensity, ServoConfig, Emotion
from robot_hat import Servo
from threading import Thread, Lock
import time
import random

class TailController:
    def __init__(self, config: ServoConfig):
        self.config = config
        self.servo = Servo(f"P{config.pin}")
        self.current_angle = 0.0
        self.is_moving = False
        self.emergency_stop = False
        self.movement_lock = Lock()
        self.wag_thread = None
        
    def set_emotion(self, emotion: Emotion) -> None:
        """
        Set tail behavior based on emotional state.
        
        Args:
            emotion: Emotional state from Emotion enum
        """
        # Stop any current wagging
        if self.wag_thread and self.wag_thread.is_alive():
            self.emergency_stop = True
            self.wag_thread.join(timeout=1.0)
            self.emergency_stop = False
            
        if emotion == Emotion.HAPPY:
            # Fast, medium amplitude wagging
            self.wag(speed=0.8, amplitude=0.7, intensity=Intensity.NORMAL)
            
        elif emotion == Emotion.SAD:
            # Slow, small amplitude, droopy tail
            self.set_angle(-30.0, 0.3)  # Drooped tail position
            
        elif emotion == Emotion.EXCITED:
            # Very fast, high amplitude wagging
            self.wag(speed=1.0, amplitude=0.9, intensity=Intensity.INTENSE)
            
        elif emotion == Emotion.ALERT:
            # Still, raised tail
            self.set_angle(45.0, 0.6)  # Alert, raised position
            
        elif emotion == Emotion.CURIOUS:
            # Slow, questioning side-to-side movement
            self.wag(speed=0.4, amplitude=0.5, intensity=Intensity.MILD)
            
        elif emotion == Emotion.SLEEPY:
            # Very slow, minimal movement
            self.set_angle(-15.0, 0.2)  # Slightly drooped
            
        elif emotion == Emotion.LOVING:
            # Gentle, rhythmic medium wagging
            self.wag(speed=0.6, amplitude=0.6, intensity=Intensity.NORMAL)
            
        elif emotion == Emotion.GRUMPY:
            # Stiff, minimal movement, slightly raised
            self.set_angle(15.0, 0.5)  # Slightly raised, stiff
            
        elif emotion == Emotion.SCARED:
            # Tucked tail
            self.set_angle(-45.0, 0.7)  # Tucked under
            
        elif emotion == Emotion.MISCHIEVOUS:
            # Random, unpredictable movements
            self.wag(speed=0.6, amplitude=0.6, intensity=Intensity.NORMAL)
            
        elif emotion == Emotion.NEUTRAL:
            # No movement, neutral position
            self.set_angle(0.0, 0.5)

        print (f"tail--> set {emotion.value}")
    
    def wag(self, speed: float, amplitude: float, intensity: Intensity) -> None:
        """
        Create wagging motion.
        Args:
            speed: Wagging frequency (0-1)
            amplitude: Movement range (0-1)
            intensity: Movement intensity
        """
        if self.emergency_stop or (self.wag_thread and self.wag_thread.is_alive()):
            print("will not wag")
            return
            
        def _wag_motion():
            
            try:
                # Base delay and angle calculations
                base_delay = 0.01 / speed  # Inverse relationship with speed
                max_angle = self.config.max_angle * amplitude
                
                # Adjust parameters based on intensity
                if intensity == Intensity.INTENSE:
                    max_angle *= 1.2
                    base_delay *= 0.7
                elif intensity == Intensity.MILD:
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