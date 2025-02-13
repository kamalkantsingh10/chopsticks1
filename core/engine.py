from enum import Enum
import random
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

from core.enums import EmotionConfig, Intensity,Position, Emotion,Mode




class EmotionEngine:
    """
    Manages emotional state and behaviors.
    
    Implementation Requirements:
    1. State management
    2. Smooth transitions
    3. Event handling
    4. Mode management
    5. Background behaviors
    6. Sleep state handling
    7. Idle animations
    """
    
    def __init__(self):
        self.current_emotion = Emotion.NEUTRAL
        self.current_mode = Mode.NORMAL
        self.is_sleeping = False
        self.last_interaction = time.time()
        self.last_idle_action = time.time()
        self.sleep_start_time = None
        
        # Sleep patterns
        self.sleep_patterns = {
            "deep_sleep": {
                "face": "sleeping_zzz",
                "breathing_rate": 0.2,
                "movement_chance": 0.05
            },
            "light_sleep": {
                "face": "sleeping_eyes",
                "breathing_rate": 0.3,
                "movement_chance": 0.1
            },
            "dreaming": {
                "face": "sleeping_rem",
                "breathing_rate": 0.4,
                "movement_chance": 0.2,
                "actions": ["paw_twitch", "soft_whimper", "ear_flick"]
            }
        }
        
        self._setup_emotion_configs()
        self._setup_mode_behaviors()
        
    def _setup_emotion_configs(self) -> None:
        """Initialize emotion configurations"""
        self.emotion_configs = {
            Emotion.HAPPY: EmotionConfig(
                idle_actions=["tail_wag", "happy_pant", "playful_bounce"],
                sounds=["happy_bark", "playful_bark", "panting"],
                expressions=["happy_eyes", "big_smile", "playful_face"],
                default_intensity=Intensity.NORMAL
            ),
            # Add other emotions...
        }
    
    def _setup_mode_behaviors(self) -> None:
        """Initialize mode-specific behaviors"""
        self.mode_behaviors = {
            Mode.PLAYFUL: {
                "idle_frequency": 15,
                "default_emotion": Emotion.HAPPY,
                "intensity_boost": 0.2
            },
            Mode.SLEEPY: {
                "idle_frequency": 30,
                "default_emotion": Emotion.SLEEPY,
                "intensity_reduction": 0.3
            },
            Mode.SLEEP: {
                "idle_frequency": 60,
                "default_emotion": Emotion.SLEEPY,
                "intensity_reduction": 0.8
            }
            # Add other modes...
        }
    
    def enter_sleep_mode(self) -> Dict:
        """Transition to sleep mode"""
        if not self.is_sleeping:
            self.is_sleeping = True
            self.current_mode = Mode.SLEEP
            self.sleep_start_time = time.time()
            
            return {
                "sequence": [
                    {"action": "yawn", "duration": 2.0},
                    {"action": "lay_down", "duration": 3.0},
                    {"action": "close_eyes", "duration": 1.0}
                ],
                "final_state": {
                    "pose": "sleeping",
                    "face": "sleeping_zzz",
                    "breathing_rate": 0.2
                }
            }
    
    def exit_sleep_mode(self) -> Dict:
        """Wake up sequence"""
        if self.is_sleeping:
            self.is_sleeping = False
            self.current_mode = Mode.SLEEPY
            self.sleep_start_time = None
            
            return {
                "sequence": [
                    {"action": "open_eyes", "duration": 1.0},
                    {"action": "stretch", "duration": 3.0},
                    {"action": "sit_up", "duration": 2.0}
                ],
                "final_state": {
                    "pose": "sitting",
                    "face": "sleepy_eyes",
                    "breathing_rate": 0.4
                }
            }
    
    def handle_sleep_disturbance(self, disturbance_type: str) -> Dict:
        """Handle interruptions during sleep"""
        sleep_duration = time.time() - self.sleep_start_time
        is_deep_sleep = sleep_duration > 300
        
        if disturbance_type == "name_called":
            return {
                "sequence": [{
                    "action": "sleepy_acknowledge",
                    "expression": "sleepy_eyes",
                    "sound": "soft_mmm",
                    "speak": "mmm sleepy" if is_deep_sleep else "chopsticks tired",
                    "duration": 2.0
                }],
                "should_wake": False,
                "next_action": "return_to_sleep"
            }
        elif disturbance_type == "command":
            return {
                "sequence": [{
                    "action": "wake_up",
                    "expression": "sleepy_eyes",
                    "sound": "yawn",
                    "speak": "chopsticks waking up",
                    "duration": 3.0
                }],
                "should_wake": True,
                "next_action": "process_command"
            }
    
    def get_idle_action(self) -> Optional[Dict]:
        """Get next idle action based on current state"""
        current_time = time.time()
        
        if self.is_sleeping:
            return self._get_sleep_action()
            
        mode_params = self.mode_behaviors[self.current_mode]
        if (current_time - self.last_idle_action) > mode_params["idle_frequency"]:
            self.last_idle_action = current_time
            
            config = self.emotion_configs[self.current_emotion]
            base_intensity = 0.5
            time_factor = min(1.0, (current_time - self.last_interaction) / 300)
            
            return {
                "action": random.choice(config.idle_actions),
                "intensity": base_intensity * time_factor,
                "emotion": self.current_emotion
            }
        return None
    
    def _get_sleep_action(self) -> Optional[Dict]:
        """Get sleep-related actions"""
        if not self.is_sleeping:
            return None
            
        sleep_duration = time.time() - self.sleep_start_time
        
        if sleep_duration < 300:
            pattern = self.sleep_patterns["light_sleep"]
        elif random.random() < 0.2:
            pattern = self.sleep_patterns["dreaming"]
        else:
            pattern = self.sleep_patterns["deep_sleep"]
            
        if random.random() < pattern["movement_chance"]:
            if "actions" in pattern:
                return {
                    "action": random.choice(pattern["actions"]),
                    "intensity": 0.2,
                    "duration": 1.0
                }
        
        return {
            "action": "breathing",
            "rate": pattern["breathing_rate"],
            "face": pattern["face"]
        }
        
    def show_emotion(self, emotion: Emotion, intensity: Intensity, speak: Optional[str] = None) -> Dict:
        """Express emotion with mode influence"""
        if self.is_sleeping:
            return self.handle_sleep_disturbance("emotion_trigger")
            
        self.last_interaction = time.time()
        self.current_emotion = emotion
        
        # Adjust intensity based on mode
        mode_params = self.mode_behaviors[self.current_mode]
        if "intensity_boost" in mode_params:
            intensity = Intensity(min(1.0, intensity.value + mode_params["intensity_boost"]))
        elif "intensity_reduction" in mode_params:
            intensity = Intensity(max(0.1, intensity.value - mode_params["intensity_reduction"]))
        
        config = self.emotion_configs[emotion]
        return {
            "emotion": emotion,
            "intensity": intensity,
            "action": random.choice(config.idle_actions),
            "sound": random.choice(config.sounds),
            "expression": random.choice(config.expressions),
            "speak": speak
        }
    
    def set_mode(self, mode: Mode) -> None:
        """Change behavioral mode"""
        self.current_mode = mode
        behavior = self.mode_behaviors[mode]
        self.show_emotion(behavior["default_emotion"], Intensity.NORMAL)