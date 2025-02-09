from enum import Enum
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

from drivers.util import Intensity,Position


from drivers.audio import AudioController
from drivers.face import FaceController
from drivers.head import HeadController
from drivers.legs import LegController
from drivers.tail import TailController



class Mode(Enum):
    PLAYFUL = "playful"      # More energetic responses, frequent happy movements
    SLEEPY = "sleepy"        # Slower movements, more yawning, calmer responses
    CURIOUS = "curious"      # More head tilts, alert responses, investigative
    CLINGY = "clingy"        # Seeks attention, more whimpers, follows closely
    GUARD = "guard"          # More alert, responsive to sounds, protective
    NORMAL = "normal"        # Standard balanced behavior
    SLEEP = "sleep"          # Full sleep mode, minimal movement, sleeping face





class EmotionEngine:
    """
    Manages emotional state, modes, and idle behaviors.
    
    Implementation Requirements:
    - State machine implementation
    - Smooth emotional transitions
    - Personality configuration
    - Mood persistence
    - Event-based triggers
    - Background behaviors
    - Idle animations
    - Sleep mode handling
    """
    def __init__(self):
        # Current state
        self.current_emotion = "neutral"
        self.current_intensity = Intensity.NORMAL
        self.current_mode = Mode.NORMAL
        self.is_sleeping = False
        
        # Timers
        self.last_interaction = time.time()
        self.last_idle_action = time.time()
        self.sleep_start_time = None
        
        # Sleep animations
        self.sleep_patterns = {
            "deep_sleep": {
                "face": "sleeping_zzz",
                "breathing_rate": 0.2,  # Slow breathing
                "movement_chance": 0.05  # Rare movement
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
        
        # Emotion palette
        self.emotions = {
            "happy": {"idle_actions": ["tail_wag", "happy_pant", "playful_bounce"]},
            "sad": {"idle_actions": ["head_low", "sad_whimper", "paw_scratch"]},
            "excited": {"idle_actions": ["bounce", "spin", "playful_bark"]},
            "alert": {"idle_actions": ["ears_perk", "head_tilt", "scan_movement"]},
            "curious": {"idle_actions": ["investigate", "sniff", "head_tilt"]},
            "sleepy": {"idle_actions": ["yawn", "stretch", "lay_down"]},
            "loving": {"idle_actions": ["gentle_wag", "soft_eyes", "nuzzle"]},
            "grumpy": {"idle_actions": ["grumble", "slow_move", "side_eye"]},
            "scared": {"idle_actions": ["hide", "tremble", "whimper"]},
            "mischievous": {"idle_actions": ["playful_growl", "pounce_ready", "tail_chase"]}
        }
        
        # Mode-specific behaviors
        self.mode_behaviors = {
            Mode.PLAYFUL: {
                "idle_frequency": 15,  # seconds
                "default_emotion": "happy",
                "intensity_boost": 0.2
            },
            Mode.SLEEPY: {
                "idle_frequency": 30,
                "default_emotion": "sleepy",
                "intensity_reduction": 0.3
            },
            Mode.CURIOUS: {
                "idle_frequency": 20,
                "default_emotion": "alert",
                "head_movement_boost": 0.3
            },
            Mode.CLINGY: {
                "idle_frequency": 10,
                "default_emotion": "loving",
                "attention_seeking": True
            },
            Mode.GUARD: {
                "idle_frequency": 25,
                "default_emotion": "alert",
                "reaction_boost": 0.4
            },
            Mode.NORMAL: {
                "idle_frequency": 20,
                "default_emotion": "neutral",
                "balanced": True
            }
        }
        
    def handle_sleep_disturbance(self, disturbance_type: str) -> Dict:
        """
        Handles interruptions during sleep mode.
        Returns appropriate response sequence.
        
        disturbance_type: 
        - "name_called": Someone said the bot's name
        - "loud_noise": Loud environmental noise
        - "touch": Physical touch detected
        - "command": Direct command given
        """
        # Get current sleep state
        sleep_duration = time.time() - self.sleep_start_time
        is_deep_sleep = sleep_duration > 300  # 5 minutes
        
        if disturbance_type == "name_called":
            return {
                "sequence": [
                    {
                        "action": "sleepy_acknowledge",
                        "expression": "sleepy_eyes",
                        "sound": "soft_mmm",
                        "speak": "mmm sleepy" if is_deep_sleep else "chopsticks tired",
                        "duration": 2.0
                    }
                ],
                "should_wake": False,
                "next_action": "return_to_sleep"
            }
        elif disturbance_type == "command":
            return {
                "sequence": [
                    {
                        "action": "wake_up",
                        "expression": "sleepy_eyes",
                        "sound": "yawn",
                        "speak": "chopsticks waking up",
                        "duration": 3.0
                    }
                ],
                "should_wake": True,
                "next_action": "process_command"
            }
        # Add other disturbance types...
        
        return None
    
    def exit_sleep_mode(self):
        """Wake up sequence"""
        if self.is_sleeping:
            self.is_sleeping = False
            self.current_mode = Mode.SLEEPY  # Start in sleepy mode
            self.sleep_start_time = None
            
            # Wake up sequence
            return {
                "sequence": [
                    {
                        "action": "open_eyes",
                        "duration": 1.0
                    },
                    {
                        "action": "stretch",
                        "duration": 3.0
                    },
                    {
                        "action": "sit_up",
                        "duration": 2.0
                    }
                ],
                "final_state": {
                    "pose": "sitting",
                    "face": "sleepy_eyes",
                    "breathing_rate": 0.4
                }
            }
    
    def get_sleep_action(self) -> Optional[Dict]:
        """Get sleep-related actions (breathing, occasional movement)"""
        if not self.is_sleeping:
            return None
            
        current_time = time.time()
        sleep_duration = current_time - self.sleep_start_time
        
        # Determine sleep phase based on duration
        if sleep_duration < 300:  # First 5 minutes
            pattern = self.sleep_patterns["light_sleep"]
        elif random.random() < 0.2:  # 20% chance of REM
            pattern = self.sleep_patterns["dreaming"]
        else:
            pattern = self.sleep_patterns["deep_sleep"]
            
        # Random sleep movements
        if random.random() < pattern["movement_chance"]:
            if "actions" in pattern:
                return {
                    "action": random.choice(pattern["actions"]),
                    "intensity": 0.2,
                    "duration": 1.0
                }
        
        # Regular breathing
        return {
            "action": "breathing",
            "rate": pattern["breathing_rate"],
            "face": pattern["face"]
        }
    
    def set_mode(self, mode: Mode):
        """Change the current behavioral mode"""
        self.current_mode = mode
        # Initial emotion for the mode
        self.update_emotion(
            self.mode_behaviors[mode]["default_emotion"],
            Intensity.NORMAL
        )
    
    def get_idle_action(self) -> Optional[Dict]:
        """Get next idle action based on current mode and emotion"""
        current_time = time.time()
        mode_params = self.mode_behaviors[self.current_mode]
        
        # Check if it's time for idle action
        if (current_time - self.last_idle_action) > mode_params["idle_frequency"]:
            self.last_idle_action = current_time
            
            # Get possible actions for current emotion
            actions = self.emotions[self.current_emotion]["idle_actions"]
            
            # Select random action
            action = random.choice(actions)
            
            # Calculate intensity based on mode and time since interaction
            base_intensity = 0.5
            time_factor = min(1.0, (current_time - self.last_interaction) / 300)  # 5 minutes max
            
            return {
                "action": action,
                "intensity": base_intensity * time_factor,
                "emotion": self.current_emotion
            }
        return None
    
    def get_expression_parameters(self) -> Dict:
        """Get current expression parameters influenced by mode"""
        params = {
            "emotion": self.current_emotion,
            "intensity": self.current_intensity,
            "mode": self.current_mode,
            "tail_speed": 0.5,
            "tail_amplitude": 0.5,
            "head_pan": 0,
            "head_tilt": 0,
            "head_speed": 0.5,
            "pose": "neutral",
            "pose_speed": 0.5
        }
        
        # Adjust parameters based on mode
        mode_params = self.mode_behaviors[self.current_mode]
        if "head_movement_boost" in mode_params:
            params["head_speed"] *= (1 + mode_params["head_movement_boost"])
        
        return params
