from core.enums import Intensity, Position, ServoConfig
from robot_hat import Servo
import time
from typing import Optional, Tuple
import math
import threading
import random

class HeadController:
    def __init__(self, pan_config: ServoConfig, tilt_config: ServoConfig):
        self.pan_config = pan_config
        self.tilt_config = tilt_config
        self.current_position = Position(0, 0)
        self.base_tilt_angle = 0  # New variable to store base tilt angle
        
        # Initialize servos
        self.pan_servo = Servo(f"P{pan_config.pin}")
        self.tilt_servo = Servo(f"P{tilt_config.pin}")
        
        # Movement parameters
        self.min_step_delay = 0.008
        self.acceleration_factor = 0.2
        self.base_steps = 20
        
    def set_base_tilt(self, tilt_angle: float, speed: float = 1.0) -> None:
        """
        Set a new base tilt angle for the head (useful for different postures like sitting)
        Args:
            tilt_angle: The desired base tilt angle
            speed: Movement speed (0.1 to 5.0)
        """
        # Ensure tilt angle is within safe limits
        safe_tilt = self._safe_angle(tilt_angle, self.tilt_config)
        self.base_tilt_angle = safe_tilt
        
        # Move to new base tilt position while maintaining current pan
        self.move_to(Position(self.current_position.x, safe_tilt), speed)

    def _safe_angle(self, angle: float, config: ServoConfig) -> float:
        """Ensure angle stays within configured limits"""
        return max(min(angle, config.max_angle), config.min_angle)
        
    def _ease_function(self, t: float) -> float:
        """
        Smooth easing function using sine wave
        Args:
            t: Input value between 0 and 1
        Returns:
            Eased value between 0 and 1
        """
        return (1 - math.cos(t * math.pi)) / 2
        
    def _calculate_smooth_steps(self, start: float, end: float, speed: float) -> list[float]:
        """
        Calculate intermediate steps with acceleration/deceleration
        """
        distance = abs(end - start)
        distance_factor = max(distance, 10)
        num_steps = int(max(distance_factor / (speed * 2), self.base_steps))
        
        if distance > 30:
            num_steps = int(num_steps * 1.5)
        elif distance > 60:
            num_steps = int(num_steps * 2)
        
        steps = []
        for i in range(num_steps + 1):
            t = i / num_steps
            smoothed_t = self._ease_function(t)
            position = start + (end - start) * smoothed_t
            jitter = random.uniform(-0.2, 0.2) if i != 0 and i != num_steps else 0
            steps.append(position + jitter)
            
        return steps
        
    def _move_servo_thread(self, servo: Servo, config: ServoConfig, 
                          start: float, end: float, speed: float) -> None:
        """Move a single servo smoothly in its own thread"""
        steps = self._calculate_smooth_steps(start, end, speed)
        
        for angle in steps:
            safe_angle = self._safe_angle(angle, config)
            servo.angle(safe_angle)
            
            progress = steps.index(angle) / len(steps)
            base_delay = self.min_step_delay / speed
            acceleration_curve = 1 + 2 * math.sin(progress * math.pi)
            position_factor = 1 + 0.5 * abs(math.sin(2 * math.pi * progress))
            
            delay = base_delay * acceleration_curve * position_factor
            time.sleep(delay)
            
    def move_to(self, position: Position, speed: float) -> None:
        """
        Move head to specified position with given speed, using simultaneous servo movement
        """
        speed = max(0.1, min(speed, 5.0))
        
        pan_thread = threading.Thread(
            target=self._move_servo_thread,
            args=(self.pan_servo, self.pan_config, 
                  self.current_position.x, position.x, speed)
        )
        
        tilt_thread = threading.Thread(
            target=self._move_servo_thread,
            args=(self.tilt_servo, self.tilt_config,
                  self.current_position.y, position.y, speed)
        )
        
        pan_thread.start()
        tilt_thread.start()
        pan_thread.join()
        tilt_thread.join()
        
        self.current_position = position
        
    def nod_yes(self, cycles: int = 2, intensity: Intensity = Intensity.NORMAL, base_tilt: Optional[float] = None) -> None:
        """
        Perform a natural nodding motion from specified base tilt angle
        Args:
            cycles: Number of nod cycles
            intensity: Intensity of the nodding motion
            base_tilt: Base tilt angle to nod from. If None, uses current position
        """
        amplitudes = {
            Intensity.MILD: 10,
            Intensity.NORMAL: 20,
            Intensity.INTENSE: 30
        }
        tilt_amount = amplitudes.get(intensity, 20)
        current_tilt = base_tilt if base_tilt is not None else self.current_position.y
        
        for i in range(cycles):
            # Calculate safe bounds for nodding
            down_tilt = min(current_tilt + tilt_amount, self.tilt_config.max_angle)
            up_tilt = max(current_tilt - tilt_amount * 0.8, self.tilt_config.min_angle)
            
            # First nod is slightly larger
            first_cycle_multiplier = 1.2 if i == 0 else 1.0
            
            # Down movement (slightly faster)
            self.move_to(
                Position(self.current_position.x, 
                        down_tilt * first_cycle_multiplier), 1.8
            )
            
            # Up movement (slightly slower)
            self.move_to(
                Position(self.current_position.x,
                        up_tilt * first_cycle_multiplier), 1.4
            )
            
        # Gentle return to original position
        self.move_to(Position(self.current_position.x, current_tilt), 0.8)
        
    def shake_no(self, cycles: int = 2, intensity: Intensity = Intensity.NORMAL) -> None:
        """
        Perform a natural head shake motion
        """
        amplitudes = {
            Intensity.MILD: 15,
            Intensity.NORMAL: 25,
            Intensity.INTENSE: 35
        }
        pan_amount = amplitudes.get(intensity, 25)
        original_position = self.current_position
        
        # Initial quick turn
        self.move_to(Position(pan_amount * 0.7, original_position.y), 2.0)
        
        for i in range(cycles):
            cycle_multiplier = 1 - (i * 0.15)
            
            # Right movement
            self.move_to(
                Position(-pan_amount * cycle_multiplier,
                        original_position.y + random.uniform(-2, 2)), 1.6
            )
            
            # Left movement
            self.move_to(
                Position(pan_amount * cycle_multiplier,
                        original_position.y + random.uniform(-2, 2)), 1.6
            )
            
        # Gentle return to center with slight overshoot
        self.move_to(Position(-pan_amount * 0.2, original_position.y), 1.0)
        time.sleep(0.1)
        self.move_to(original_position, 0.7)