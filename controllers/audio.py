from core.enums import Intensity, Emotion
from enum import Enum
from robot_hat import TTS, set_volume

class AudioController:
    """
    Handles async audio output with emotional text-to-speech capabilities.
    Only one audio request is processed at a time, others are ignored.
    """
    def __init__(self):
        # Initialize all attributes first
        self.tts = TTS(engine=TTS.ESPEAK)
        self.is_speaking = False
        self.current_request = None
        set_volume(95)
        
        # Fixed emotional parameters for each emotion
        self.emotion_params = {
            Emotion.HAPPY: {'speed': 180, 'pitch': 80, 'gap': 3},
            Emotion.SAD: {'speed': 120, 'pitch': 30, 'gap': 8},
            Emotion.EXCITED: {'speed': 200, 'pitch': 85, 'gap': 2},
            Emotion.ALERT: {'speed': 175, 'pitch': 75, 'gap': 3},
            Emotion.CURIOUS: {'speed': 150, 'pitch': 65, 'gap': 4},
            Emotion.SLEEPY: {'speed': 110, 'pitch': 40, 'gap': 7},
            Emotion.LOVING: {'speed': 140, 'pitch': 60, 'gap': 5},
            Emotion.GRUMPY: {'speed': 160, 'pitch': 45, 'gap': 4},
            Emotion.SCARED: {'speed': 190, 'pitch': 80, 'gap': 3},
            Emotion.MISCHIEVOUS: {'speed': 170, 'pitch': 70, 'gap': 3},
            Emotion.NEUTRAL: {'speed': 160, 'pitch': 50, 'gap': 5}
        }
        
    def _process_current_speech(self, text, emotion, intensity):
        """Processes speech requests"""
        self.is_speaking = True
        try:
            # Set volume based on intensity (0-100 scale)
            volume = int(50+ intensity.value/2 * 100)
            #set_volume(volume)
                        
            # Apply emotional parameters
            params = self.emotion_params[emotion]
            self.tts.espeak_params(
                amp=100,  # Fixed amplitude since volume is controlled by set_volume
                speed=params['speed'],
                pitch=params['pitch'],
                gap=params['gap']
                )
            self.tts.say(text)
        except Exception as e:
            print(f"Error during speech: {e}")
        finally:
            self.is_speaking = False

    def speak(self, text: str, emotion: Emotion, intensity: Intensity) -> None:
        """
        Queue speech request. If there's already a request being processed,
        this new request will be ignored.
        """
        if not self.is_speaking:
            self._process_current_speech(text, emotion, intensity)
        else:
            print("Speech in progress, ignoring new request")

    def cleanup(self) -> None:
        """Stop the audio processing thread"""
        pass