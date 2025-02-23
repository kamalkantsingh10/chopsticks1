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
        self.base_tilt_angle = 0  # Variable to store base tilt angle
        
        # Initialize servos
        self.pan_servo = Servo(f"P{pan_config.pin}")
        self.tilt_servo = Servo(f"P{tilt_config.pin}")
        
        # Movement parameters
        self.min_step_delay = 0.01  # Base timing for smoother movement
        self.acceleration_factor = 0.18  # Slightly higher to allow more dynamic movement
        self.base_steps = 22  # Good balance of smoothness and responsiveness
        
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
        Smooth easing function
        Args:
            t: Input value between 0 and 1
        Returns:
            Eased value between 0 and 1
        """
        # Combined easing function: mixture of sine and cubic for expressiveness while remaining smooth
        cubic = 3 * t**2 - 2 * t**3
        sine = (1 - math.cos(t * math.pi)) / 2
        return cubic * 0.7 + sine * 0.3
        
    def _calculate_smooth_steps(self, start: float, end: float, speed: float) -> list[float]:
        """
        Calculate intermediate steps with acceleration/deceleration
        """
        distance = abs(end - start)
        distance_factor = max(distance, 10)
        
        # More steps for longer distances, but maintain responsiveness
        num_steps = int(max(distance_factor / (speed * 1.5), self.base_steps))
        
        if distance > 30:
            num_steps = int(num_steps * 1.7)
        elif distance > 60:
            num_steps = int(num_steps * 2.2)
        
        steps = []
        for i in range(num_steps + 1):
            t = i / num_steps
            smoothed_t = self._ease_function(t)
            position = start + (end - start) * smoothed_t
            
            # Add very subtle micro-expressions for more lifelike movement
            # Only add micro-expressions in the middle 60% of the movement
            # and make them extremely subtle to maintain smoothness
            if 0.2 < t < 0.8 and distance > 10 and i % 3 == 0:
                micro_jitter = random.uniform(-0.08, 0.08) * (distance / 30)
                position += micro_jitter
            
            steps.append(position)
            
        return steps
        
    def _move_servo_thread(self, servo: Servo, config: ServoConfig, 
                          start: float, end: float, speed: float) -> None:
        """Move a single servo smoothly in its own thread"""
        steps = self._calculate_smooth_steps(start, end, speed)
        
        for angle in steps:
            safe_angle = self._safe_angle(angle, config)
            servo.angle(safe_angle)
            
            # Dynamic timing for natural movement
            progress = steps.index(angle) / len(steps)
            
            # Acceleration and deceleration curve
            if progress < 0.15:
                # Starting acceleration
                delay_factor = 1.4 - progress * 2  # Gradually speed up
            elif progress > 0.85:
                # Ending deceleration
                delay_factor = 1 + (progress - 0.85) * 3  # Gradually slow down
            else:
                # Middle movement - subtle variations for lifelike quality
                delay_factor = 0.95 + 0.1 * math.sin(progress * 5)
                
            delay = self.min_step_delay / speed * delay_factor
            time.sleep(delay)
            
    def move_to(self, position: Position, speed: float) -> None:
        """
        Move head to specified position with given speed, using simultaneous servo movement
        """
        # Ensure speed is within reasonable limits
        speed = max(0.1, min(speed, 5.0))
        
        # Don't move if we're already at the target position (with small tolerance)
        if (abs(self.current_position.x - position.x) < 0.3 and 
            abs(self.current_position.y - position.y) < 0.3):
            return
        
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
            Intensity.MILD: 10,    # Mild but still expressive
            Intensity.NORMAL: 18,  # Good balance
            Intensity.INTENSE: 28  # Expressive but controlled
        }
        tilt_amount = amplitudes.get(intensity, 18)
        current_tilt = base_tilt if base_tilt is not None else self.current_position.y
        
        for i in range(cycles):
            # Calculate safe bounds for nodding
            down_tilt = min(current_tilt + tilt_amount, self.tilt_config.max_angle)
            up_tilt = max(current_tilt - tilt_amount * 0.7, self.tilt_config.min_angle)
            
            # First nod is slightly larger for expressiveness
            first_cycle_multiplier = 1.15 if i == 0 else 1.0
            
            # Each successive nod gets slightly smaller for natural effect
            cycle_decay = 1.0 - (i * 0.1)
            
            # Down movement (slightly faster)
            self.move_to(
                Position(self.current_position.x, 
                        down_tilt * first_cycle_multiplier * cycle_decay), 1.4
            )
            
            # Up movement (slightly slower)
            self.move_to(
                Position(self.current_position.x,
                        up_tilt * first_cycle_multiplier * cycle_decay), 1.2
            )
            
        # Gentle return to original position with slight overshoot for natural feel
        slight_overshoot = current_tilt - (tilt_amount * 0.1)
        self.move_to(Position(self.current_position.x, slight_overshoot), 0.8)
        time.sleep(0.1)
        self.move_to(Position(self.current_position.x, current_tilt), 0.7)
        
    def shake_no(self, cycles: int = 2, intensity: Intensity = Intensity.NORMAL) -> None:
        """
        Perform a natural head shake motion
        """
        amplitudes = {
            Intensity.MILD: 14,    # Mild but still visible
            Intensity.NORMAL: 22,  # Good balance
            Intensity.INTENSE: 32  # Expressive but controlled
        }
        pan_amount = amplitudes.get(intensity, 22)
        original_position = self.current_position
        
        # Initial turn with slight tilt for expressiveness
        slight_tilt = original_position.y + random.uniform(0, 2) if intensity != Intensity.MILD else original_position.y
        self.move_to(Position(pan_amount * 0.7, slight_tilt), 1.2)
        
        for i in range(cycles):
            # Each shake gets slightly smaller for natural motion
            cycle_multiplier = 1 - (i * 0.12)
            
            # Slight tilt variations for expressiveness
            tilt_variation = random.uniform(-1, 1) if intensity != Intensity.MILD else 0
            
            # Right movement
            self.move_to(
                Position(-pan_amount * cycle_multiplier,
                        original_position.y + tilt_variation), 1.2
            )
            
            # Left movement
            tilt_variation = random.uniform(-1, 1) if intensity != Intensity.MILD else 0
            self.move_to(
                Position(pan_amount * cycle_multiplier,
                        original_position.y + tilt_variation), 1.2
            )
            
        # Return to center with natural motion - slight overshoot then correction
        self.move_to(Position(-pan_amount * 0.15, original_position.y), 0.9)
        time.sleep(0.1)
        self.move_to(original_position, 0.7)