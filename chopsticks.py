
import time
from controllers.audio import AudioController
from controllers.face import FaceController
from controllers.head import HeadController
from controllers.legs import LegController
from controllers.tail import TailController

from emotions.engine import EmotionEngine

from typing import Dict, List, Optional
from dataclasses import dataclass

from emotions.enums import Emotion, Intensity,Position, ServoConfig



class RobotDog:
    """
    Main robot control class.
    
    Implementation Requirements:
    1. Component lifecycle management
    2. Configuration handling
    3. Command processing
    4. Error recovery
    5. Performance monitoring
    6. Background behaviors
    7. Sleep mode management
    
    Setup:
    1. Initialize all controllers
    2. Load configurations
    3. Start background tasks
    4. Monitor system health
    """
    
    def __init__(self, config: Dict):
        self._init_components(config)
        self.emotion_engine = EmotionEngine()
        self._running = True
        self._start_background_tasks()
        
    def _init_components(self, config: Dict) -> None:
        """Initialize all hardware components"""
        self.tail = TailController(config["tail"])
        self.head = HeadController(config["pan"], config["tilt"])
        self.display = FaceController(config["display_width"], config["display_height"])
        self.audio = AudioController(config["audio_device"])
        self.legs = LegController(config["leg_configs"])
    
    def _start_background_tasks(self) -> None:
        """Start background processing"""
        import threading
        self._idle_thread = threading.Thread(target=self._idle_loop, daemon=True)
        self._idle_thread.start()
    
    def _idle_loop(self) -> None:
        """Background loop for idle behaviors"""
        while self._running:
            action = self.emotion_engine.get_idle_action()
            if action:
                self._execute_action(action)
            time.sleep(0.1)
    
    def _execute_action(self, action: Dict) -> None:
        """Execute a single action across all components"""
        try:
            if "emotion" in action:
                # Coordinated emotional expression
                self.tail.wag(action.get("tail_speed", 0.5), 
                            action.get("tail_amplitude", 0.5),
                            action.get("intensity", Intensity.NORMAL))
                            
                self.head.move_to(Position(action.get("head_pan", 0),
                                         action.get("head_tilt", 0)),
                                action.get("head_speed", 0.5))
                                
                self.display.set_expression(action.get("expression", "neutral"),
                                         action.get("intensity", Intensity.NORMAL))
                                         
                if "sound" in action:
                    self.audio.play_sound(action["sound"], 
                                        action.get("volume", 0.5))
                                        
                if "speak" in action and action["speak"]:
                    self.audio.speak(action["speak"],
                                   action["emotion"],
                                   action.get("intensity", Intensity.NORMAL))
                                   
                self.legs.set_pose(action.get("pose", "neutral"),
                                 action.get("speed", 0.5))
                
        except Exception as e:
            print(f"Error executing action: {e}")
    
    def show_emotion(self, emotion: Emotion, intensity: Intensity, speak: Optional[str] = None) -> None:
        """Main method for LLM to trigger emotions"""
        params = self.emotion_engine.show_emotion(emotion, intensity, speak)
        self._execute_action(params)
    
    def enter_sleep_mode(self) -> None:
        """Put robot in sleep mode"""
        sequence = self.emotion_engine.enter_sleep_mode()
        for action in sequence["sequence"]:
            self._execute_action(action)
            time.sleep(action["duration"])
        self._execute_action(sequence["final_state"])
    
    def exit_sleep_mode(self) -> None:
        """Wake up robot"""
        sequence = self.emotion_engine.exit_sleep_mode()
        for action in sequence["sequence"]:
            self._execute_action(action)
            time.sleep(action["duration"])
        self._execute_action(sequence["final_state"])
     
    def cleanup(self) -> None:
        """Cleanup all components"""
        self.tail.cleanup()
        self.head.cleanup()
        self.display.cleanup()
        self.audio.cleanup()
        self.legs.cleanup()

# Example Configuration
config = {
    "tail": ServoConfig(pin=18, min_angle=0, max_angle=180, default_speed=0.5),
    "pan": ServoConfig(pin=19, min_angle=-90, max_angle=90, default_speed=0.3),
    "tilt": ServoConfig(pin=20, min_angle=-45, max_angle=45, default_speed=0.3),
    "display_width": 128,
    "display_height": 64,
    "audio_device": "default",
    "leg_configs": [
        [ServoConfig(pin=i, min_angle=-90, max_angle=90, default_speed=0.5) 
         for i in range(1, 4)]
        for _ in range(4)
    ]
}
