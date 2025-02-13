import sys
from robot_hat import TTS, set_volume

class EmotionalTTS:
    def __init__(self):
        self.tts = TTS(engine=TTS.ESPEAK)
        self.emotions = {
            'happy': {
                'amp': 180,    # Very loud and energetic
                'speed': 220,  # Fast and bouncy
                'pitch': 95,   # Very high pitch
                'gap': 2       # Short gaps for excitement
            },
            'sad': {
                'amp': 60,     # Very quiet and subdued
                'speed': 100,  # Very slow and dragging
                'pitch': 20,   # Very low pitch
                'gap': 10      # Long pauses between words
            },
            'angry': {
                'amp': 195,    # Nearly maximum volume
                'speed': 250,  # Very fast speaking
                'pitch': 90,   # High pitch for intensity
                'gap': 1       # Minimal gaps for intensity
            },
            'excited': {
                'amp': 190,    # Very loud
                'speed': 255,  # Maximum speed
                'pitch': 98,   # Nearly maximum pitch
                'gap': 1       # Quick speech with minimal gaps
            },
            'calm': {
                'amp': 70,     # Quiet and soothing
                'speed': 90,   # Very slow and measured
                'pitch': 35,   # Low, soothing pitch
                'gap': 8       # Long, peaceful gaps
            },
            'scared': {
                'amp': 160,    # Loud for emphasis
                'speed': 245,  # Very fast for panic
                'pitch': 85,   # High pitch for fear
                'gap': 3       # Irregular gaps for nervousness
            },
            'surprised': {
                'amp': 185,    # Very loud for shock
                'speed': 240,  # Fast for surprise
                'pitch': 95,   # Very high pitch
                'gap': 2       # Short gaps for emphasis
            },
            'neutral': {
                'amp': 100,    # Default amplitude
                'speed': 160,  # Default speed
                'pitch': 50,   # Default pitch
                'gap': 5       # Default gap
            }
        }

    def say_with_emotion(self, text, emotion):
        """
        Say text with specified emotion.
        
        Args:
            text (str): The text to speak
            emotion (str): One of: happy, sad, angry, excited, calm, scared, surprised, neutral
        """
        if emotion not in self.emotions:
            raise ValueError(f"Emotion must be one of: {', '.join(self.emotions.keys())}")
        
        params = self.emotions[emotion]
        self.tts.espeak_params(
            amp=params['amp'],
            speed=params['speed'],
            pitch=params['pitch'],
            gap=params['gap']
        )
        self.tts.say(text)

# Example usage:
if __name__ == "__main__":
    emotional_tts = EmotionalTTS()
    
    # Example text to demonstrate different emotions
    text = "I can speak with different emotions"
    
    # Demonstrate all emotions
    for emotion in emotional_tts.emotions.keys():
        print(f"\nSpeaking with {emotion} emotion:")
        emotional_tts.say_with_emotion(text, emotion)
        
        # Add a small delay between emotions (you might want to import time and use time.sleep(2))
