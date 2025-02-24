from core.enums import Intensity, ServoConfig, Emotion
from robot_hat import Servo
from threading import Thread, Lock
import time
import random
import math

class TailController:
    def __init__(self, config: ServoConfig):
        self.config = config
        self.servo = Servo(f"P{config.pin}")
        self.current_angle = 0.0
        self.is_moving = False
        self.emergency_stop = False
        self.movement_lock = Lock()
        self.wag_thread = None
        self.idle_thread = None
        
    def set_emotion(self, emotion: Emotion) -> None:
        """
        Set tail behavior based on emotional state with natural dog-like movements.
        
        Args:
            emotion: Emotional state from Emotion enum
        """
        # Stop any current movement
        self._stop_current_movements()
            
        if emotion == Emotion.HAPPY:
            # Enthusiastic wagging with natural rhythm
            self.wag(
                speed=0.8,
                amplitude=0.7,
                intensity=Intensity.NORMAL,
                pattern="sine"
            )
            
        elif emotion == Emotion.SAD:
            # Droopy tail with occasional subtle movements
            self.set_angle(-30.0, 0.3)
            self._start_idle_movement(
                base_angle=-30.0,
                amplitude=5.0,
                frequency=0.2
            )
            
        elif emotion == Emotion.EXCITED:
            # Rapid, varied wagging with increasing intensity
            self.wag(
                speed=1.0,
                amplitude=0.9,
                intensity=Intensity.INTENSE,
                pattern="crescendo"
            )
            
        elif emotion == Emotion.ALERT:
            # Raised tail with minimal, alert movements
            self.set_angle(45.0, 0.6)
            self._start_idle_movement(
                base_angle=45.0,
                amplitude=3.0,
                frequency=0.5
            )
            
        elif emotion == Emotion.CURIOUS:
            # Inquisitive side-to-side movement with pauses
            self.wag(
                speed=0.4,
                amplitude=0.5,
                intensity=Intensity.MILD,
                pattern="pause"
            )
            
        elif emotion == Emotion.SLEEPY:
            # Very slow, gentle swaying
            self._start_idle_movement(
                base_angle=-15.0,
                amplitude=8.0,
                frequency=0.15
            )
            
        elif emotion == Emotion.LOVING:
            # Smooth, gentle wagging with natural flow
            self.wag(
                speed=0.6,
                amplitude=0.6,
                intensity=Intensity.NORMAL,
                pattern="smooth"
            )
            
        elif emotion == Emotion.GRUMPY:
            # Occasional sharp, stiff movements
            self._start_idle_movement(
                base_angle=15.0,
                amplitude=10.0,
                frequency=0.3,
                pattern="sharp"
            )
            
        elif emotion == Emotion.SCARED:
            # Tucked tail with trembling
            self._start_idle_movement(
                base_angle=-65.0,
                amplitude=3.0,
                frequency=1.2,
                pattern="trembling"
            )
            
        elif emotion == Emotion.MISCHIEVOUS:
            # Playful, unpredictable movements
            self.wag(
                speed=0.6,
                amplitude=0.6,
                intensity=Intensity.NORMAL,
                pattern="random"
            )
            
        elif emotion == Emotion.NEUTRAL:
            # Subtle, life-like idle movements
            self._start_idle_movement(
                base_angle=0.0,
                amplitude=5.0,
                frequency=0.3
            )

        print(f"tail--> set {emotion.value}")
    
    def wag(self, speed: float, amplitude: float, intensity: Intensity, pattern: str = "sine") -> None:
        """
        Create natural wagging motion with various patterns.
        
        Args:
            speed: Wagging frequency (0-1)
            amplitude: Movement range (0-1)
            intensity: Movement intensity
            pattern: Movement pattern ("sine", "crescendo", "pause", "smooth", "random")
        """
        if self.emergency_stop or (self.wag_thread and self.wag_thread.is_alive()):
            print("will not wag")
            return
            
        def _wag_motion():
            try:
                base_delay = 0.01 / speed
                max_angle = self.config.max_angle * amplitude
                
                if intensity == Intensity.INTENSE:
                    max_angle *= 1.2
                    base_delay *= 0.7
                elif intensity == Intensity.MILD:
                    max_angle *= 0.8
                    base_delay *= 1.3
                
                phase = 0.0
                while not self.emergency_stop:
                    if pattern == "sine":
                        angle = max_angle * math.sin(phase)
                        phase += 0.2
                    elif pattern == "crescendo":
                        angle = max_angle * math.sin(phase) * (1 + 0.2 * math.sin(phase/5))
                        phase += 0.25
                    elif pattern == "pause":
                        angle = max_angle * math.sin(phase)
                        if random.random() < 0.1:
                            time.sleep(random.uniform(0.1, 0.3))
                        phase += 0.15
                    elif pattern == "smooth":
                        angle = max_angle * math.sin(phase) * (0.8 + 0.2 * math.sin(phase/3))
                        phase += 0.18
                    elif pattern == "random":
                        angle = max_angle * math.sin(phase) * random.uniform(0.8, 1.2)
                        phase += random.uniform(0.15, 0.25)
                    
                    self.set_angle(angle, speed)
                    time.sleep(base_delay)
                    
            except Exception as e:
                print(f"Error during wagging: {e}")
                self.stop()
                
        self.wag_thread = Thread(target=_wag_motion, daemon=True)
        self.wag_thread.start()
        
    def _start_idle_movement(self, base_angle: float, amplitude: float, 
                           frequency: float, pattern: str = "smooth") -> None:
        """
        Start subtle idle movements around a base angle.
        
        Args:
            base_angle: Center position for movements
            amplitude: Maximum deviation from base angle
            frequency: Movement frequency
            pattern: Movement pattern ("smooth", "sharp", "trembling")
        """
        def _idle_motion():
            try:
                phase = 0.0
                while not self.emergency_stop:
                    if pattern == "smooth":
                        offset = amplitude * math.sin(phase) * math.sin(phase/3)
                    elif pattern == "sharp":
                        offset = amplitude * (math.sin(phase) > 0.7)
                    elif pattern == "trembling":
                        offset = amplitude * math.sin(phase * 3) * math.sin(phase)
                    else:
                        offset = amplitude * math.sin(phase)
                        
                    angle = base_angle + offset
                    self.set_angle(angle, 0.3)
                    time.sleep(1/frequency)
                    phase += 0.1
                    
            except Exception as e:
                print(f"Error during idle movement: {e}")
                self.stop()
        
        self.idle_thread = Thread(target=_idle_motion, daemon=True)
        self.idle_thread.start()
        
    def _stop_current_movements(self):
        """Stop all current movement threads"""
        self.emergency_stop = True
        if self.wag_thread and self.wag_thread.is_alive():
            self.wag_thread.join(timeout=1.0)
        if self.idle_thread and self.idle_thread.is_alive():
            self.idle_thread.join(timeout=1.0)
        self.emergency_stop = False
        
    def set_angle(self, angle: float, speed: float) -> None:
        """Move tail to specific angle with smooth interpolation"""
        if self.emergency_stop:
            return
            
        with self.movement_lock:
            try:
                angle = max(self.config.min_angle,
                          min(self.config.max_angle, angle))
                delay = 0.01 * (1 - speed)
                self.servo.angle(angle)
                time.sleep(delay)
                self.current_angle = angle
            except Exception as e:
                print(f"Error setting angle: {e}")
                self.stop()
                
    def stop(self) -> None:
        """Emergency stop all movements"""
        self.emergency_stop = True
        with self.movement_lock:
            self.servo.angle(0)
            self.is_moving = False
            
    def cleanup(self) -> None:
        """Release hardware resources and stop all movements"""
        self.stop()
        self._stop_current_movements()
        self.servo.angle(0)