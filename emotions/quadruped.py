import time
import math
import random
from threading import Thread, Lock
from core.enums import Emotion

class EmotionalBehaviors:
    def __init__(self, controller):
        self.controller = controller
        self.base_height = 38
        self.movement_thread = None
        self.stop_movement = False
        self.movement_lock = Lock()
        self.current_emotion = None
        
        # Safe movement limits (very conservative)
        self.MAX_X_OFFSET = 1.0  # Maximum x deviation from base position
        self.MAX_Y_OFFSET = 1.0  # Maximum y deviation from base position
        
        # Track base positions for each leg
        self.leg_base_positions = {
            'front_right': [0, self.base_height],
            'front_left': [0, self.base_height],
            'back_right': [0, self.base_height],
            'back_left': [0, self.base_height]
        }
        
    def _clamp_value(self, value, offset, max_offset):
        """Clamp offset to safe range"""
        return max(-max_offset, min(max_offset, offset))
        
    def _safe_move(self, leg_name, x, y):
        """Move leg with safety checks"""
        try:
            # Ensure x and y are valid numbers
            if x is None or y is None:
                return False
                
            # Apply movement
            self.controller.legs[leg_name].move(x, y)
            return True
        except Exception as e:
            print(f"Safe move error for {leg_name}: {e}")
            return False
            
    def express_emotion(self, emotion):
        """Express an emotion with minimal continuous movements"""
        if self.controller.current_pose != "stand":
            return
            
        print(f"Expressing emotion: {emotion}")
        
        # Stop any current movement
        self._stop_current_movement()
        
        # Set initial position
        self._set_emotion_pose(emotion)
        time.sleep(0.5)  # Allow initial pose to settle
        
        # Start subtle movement thread
        self.current_emotion = emotion
        self.stop_movement = False
        self.movement_thread = Thread(target=self._continuous_movement, daemon=True)
        self.movement_thread.start()
        
    def _stop_current_movement(self):
        """Stop current movement thread if running"""
        if self.movement_thread and self.movement_thread.is_alive():
            self.stop_movement = True
            self.movement_thread.join(timeout=1.0)
            
    def _continuous_movement(self):
        """Generate very subtle continuous movements"""
        phase = 0.0
        try:
            while not self.stop_movement:
                with self.movement_lock:
                    if self.current_emotion == Emotion.HAPPY:
                        # Tiny bouncing movement
                        offset = math.sin(phase) * 0.5
                        self._move_all_legs(y_offset=offset)
                        phase += 0.03
                        
                    elif self.current_emotion == Emotion.SAD:
                        # Minimal front leg movement
                        if random.random() < 0.05:
                            offset = random.uniform(-0.5, 0)
                            self._move_front_legs(y_offset=offset)
                        time.sleep(1.0)
                        
                    elif self.current_emotion == Emotion.EXCITED:
                        # Very small bounces
                        y_offset = math.sin(phase) * 0.4
                        x_offset = math.sin(phase/2) * 0.3
                        self._move_all_legs(x_offset=x_offset, y_offset=y_offset)
                        phase += 0.05
                        
                    elif self.current_emotion == Emotion.ALERT:
                        # Micro-movements
                        offset = math.sin(phase) * 0.2
                        self._move_all_legs(x_offset=offset)
                        phase += 0.02
                        
                    elif self.current_emotion == Emotion.CURIOUS:
                        # Tiny weight shifts
                        offset = math.sin(phase) * 0.3
                        self._move_front_legs(x_offset=offset)
                        self._move_back_legs(x_offset=-offset/2)
                        phase += 0.02
                        
                    elif self.current_emotion == Emotion.SLEEPY:
                        # Very slow, minimal sway
                        if random.random() < 0.03:
                            offset = random.uniform(-0.2, 0.2)
                            self._move_all_legs(x_offset=offset)
                        time.sleep(1.5)
                        
                    elif self.current_emotion == Emotion.LOVING:
                        # Gentle micro-sway
                        offset = math.sin(phase) * 0.3
                        self._move_all_legs(x_offset=offset)
                        phase += 0.02
                        
                    elif self.current_emotion == Emotion.GRUMPY:
                        # Tiny occasional shifts
                        if random.random() < 0.08:
                            offset = random.uniform(-0.3, 0.3)
                            self._move_all_legs(x_offset=offset)
                        time.sleep(0.5)
                        
                    elif self.current_emotion == Emotion.SCARED:
                        # Micro-trembles
                        offset = (random.random() - 0.5) * 0.2
                        self._move_all_legs(x_offset=offset, y_offset=offset)
                        time.sleep(0.2)
                        
                    elif self.current_emotion == Emotion.MISCHIEVOUS:
                        # Small random adjustments
                        if random.random() < 0.1:
                            x_offset = random.uniform(-0.3, 0.3)
                            y_offset = random.uniform(-0.2, 0.2)
                            self._move_all_legs(x_offset=x_offset, y_offset=y_offset)
                        time.sleep(0.5)
                        
                    elif self.current_emotion == Emotion.NEUTRAL:
                        # Barely perceptible movement
                        offset = math.sin(phase) * 0.15
                        self._move_all_legs(x_offset=offset)
                        phase += 0.01
                        
                time.sleep(0.1)  # Slower base movement rate
                
        except Exception as e:
            print(f"Error in continuous movement: {e}")
            self.stop_movement = True

    def _move_all_legs(self, x_offset=0, y_offset=0):
        """Move all legs with minimal safe offsets"""
        x_offset = self._clamp_value(x_offset, x_offset, self.MAX_X_OFFSET)
        y_offset = self._clamp_value(y_offset, y_offset, self.MAX_Y_OFFSET)
        
        for leg_name, base_pos in self.leg_base_positions.items():
            new_x = base_pos[0] + x_offset
            new_y = base_pos[1] + y_offset
            self._safe_move(leg_name, new_x, new_y)
            
    def _move_front_legs(self, x_offset=0, y_offset=0):
        """Move front legs with minimal safe offsets"""
        x_offset = self._clamp_value(x_offset, x_offset, self.MAX_X_OFFSET)
        y_offset = self._clamp_value(y_offset, y_offset, self.MAX_Y_OFFSET)
        
        for leg_name in ['front_right', 'front_left']:
            base_pos = self.leg_base_positions[leg_name]
            new_x = base_pos[0] + x_offset
            new_y = base_pos[1] + y_offset
            self._safe_move(leg_name, new_x, new_y)
            
    def _move_back_legs(self, x_offset=0, y_offset=0):
        """Move back legs with minimal safe offsets"""
        x_offset = self._clamp_value(x_offset, x_offset, self.MAX_X_OFFSET)
        y_offset = self._clamp_value(y_offset, y_offset, self.MAX_Y_OFFSET)
        
        for leg_name in ['back_right', 'back_left']:
            base_pos = self.leg_base_positions[leg_name]
            new_x = base_pos[0] + x_offset
            new_y = base_pos[1] + y_offset
            self._safe_move(leg_name, new_x, new_y)
            
    def _set_emotion_pose(self, emotion):
        """Set initial emotion pose"""
        if emotion == Emotion.HAPPY:
            positions = {
                'front_right': (1, self.base_height + 2),
                'front_left': (1, self.base_height + 2),
                'back_right': (-1, self.base_height),
                'back_left': (-1, self.base_height)
            }
        elif emotion == Emotion.SAD:
            positions = {
                'front_right': (0, self.base_height - 3),
                'front_left': (0, self.base_height - 3),
                'back_right': (0, self.base_height),
                'back_left': (0, self.base_height)
            }
        elif emotion == Emotion.EXCITED:
            positions = {
                'front_right': (2, self.base_height + 2),
                'front_left': (2, self.base_height + 2),
                'back_right': (-1, self.base_height + 1),
                'back_left': (-1, self.base_height + 1)
            }
        elif emotion == Emotion.ALERT:
            positions = {
                'front_right': (0, self.base_height + 2),
                'front_left': (0, self.base_height + 2),
                'back_right': (0, self.base_height + 1),
                'back_left': (0, self.base_height + 1)
            }
        elif emotion == Emotion.CURIOUS:
            positions = {
                'front_right': (2, self.base_height + 1),
                'front_left': (2, self.base_height + 1),
                'back_right': (-1, self.base_height - 1),
                'back_left': (-1, self.base_height - 1)
            }
        elif emotion == Emotion.SLEEPY:
            positions = {
                'front_right': (-2, self.base_height - 2),
                'front_left': (-2, self.base_height - 2),
                'back_right': (-2, self.base_height - 2),
                'back_left': (-2, self.base_height - 2)
            }
        elif emotion == Emotion.LOVING:
            positions = {
                'front_right': (1, self.base_height),
                'front_left': (1, self.base_height),
                'back_right': (-1, self.base_height - 2),
                'back_left': (-1, self.base_height - 2)
            }
        elif emotion == Emotion.GRUMPY:
            positions = {
                'front_right': (-1, self.base_height - 2),
                'front_left': (-1, self.base_height - 2),
                'back_right': (1, self.base_height - 1),
                'back_left': (1, self.base_height - 1)
            }
        elif emotion == Emotion.SCARED:
            positions = {
                'front_right': (-2, self.base_height),
                'front_left': (-2, self.base_height),
                'back_right': (-1, self.base_height - 2),
                'back_left': (-1, self.base_height - 2)
            }
        elif emotion == Emotion.MISCHIEVOUS:
            positions = {
                'front_right': (2, self.base_height - 2),
                'front_left': (2, self.base_height - 2),
                'back_right': (-1, self.base_height - 1),
                'back_left': (-1, self.base_height - 1)
            }
        else:  # NEUTRAL
            positions = {
                'front_right': (0, self.base_height),
                'front_left': (0, self.base_height),
                'back_right': (0, self.base_height),
                'back_left': (0, self.base_height)
            }
            
        # Update base positions and move legs
        for leg_name, pos in positions.items():
            self.leg_base_positions[leg_name] = list(pos)
            self._safe_move(leg_name, pos[0], pos[1])