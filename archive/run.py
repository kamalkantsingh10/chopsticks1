from trials.test_servo import run_servo
from robot_hat import Music, set_volume
import time


class GentleEmotionalSounds:
    def __init__(self):
        self.music = Music()
        self.SILENCE = 1
        
    def happy(self):
        """Soft, warm ascending notes"""
        self.music.tempo(120)
        # Gentle rising melody
        self.music.play_tone_for(self.music.note("C4"), self.music.beat(1/2))
        self.music.play_tone_for(self.music.note("E4"), self.music.beat(1/2))
        self.music.play_tone_for(self.music.note("F4"), self.music.beat(1/2))
        # Soft conclusion
        self.music.play_tone_for(self.music.note("G4"), self.music.beat(1))
        
    def sad(self):
        """Gentle descending melody"""
        self.music.tempo(80)
        # Soft descending notes
        self.music.play_tone_for(self.music.note("E4"), self.music.beat(3/4))
        self.music.play_tone_for(self.music.note("D4"), self.music.beat(3/4))
        self.music.play_tone_for(self.music.note("C4"), self.music.beat(1))
        
    def angry(self):
        """Low, subtle tension"""
        self.music.tempo(100)
        # Gentle tension pattern
        self.music.play_tone_for(self.music.note("D4"), self.music.beat(1/2))
        self.music.play_tone_for(self.music.note("C4"), self.music.beat(1/2))
        self.music.play_tone_for(self.music.note("D4"), self.music.beat(1/2))
        self.music.play_tone_for(self.music.note("C4"), self.music.beat(1))
        
    def excited(self):
        """Light, flowing upward pattern"""
        self.music.tempo(140)
        # Gentle flowing sequence
        notes = ["C4", "D4", "E4", "F4"]
        for note in notes:
            self.music.play_tone_for(self.music.note(note), self.music.beat(1/2))
        self.music.play_tone_for(self.music.note("G4"), self.music.beat(1))
        
    def sleepy(self):
        """Very soft, lullaby-like descent"""
        self.music.tempo(60)
        # Gentle lullaby pattern
        self.music.play_tone_for(self.music.note("G4"), self.music.beat(1))
        self.music.play_tone_for(self.music.note("E4"), self.music.beat(1))
        self.music.play_tone_for(self.music.note("C4"), self.music.beat(2))
        
    def curious(self):
        """Soft rising question"""
        self.music.tempo(100)
        # Gentle questioning pattern
        self.music.play_tone_for(self.music.note("C4"), self.music.beat(1/2))
        self.music.play_tone_for(self.SILENCE, self.music.beat(1/8))
        self.music.play_tone_for(self.music.note("E4"), self.music.beat(1/2))
        self.music.play_tone_for(self.music.note("G4"), self.music.beat(1))
        
    def confused(self):
        """Gentle wandering melody"""
        self.music.tempo(90)
        # Soft meandering pattern
        notes = ["E4", "D4", "F4", "E4", "D4"]
        for note in notes:
            self.music.play_tone_for(self.music.note(note), self.music.beat(1/2))
            self.music.play_tone_for(self.SILENCE, self.music.beat(1/16))
        
    def surprised(self):
        """Soft lifted notes"""
        self.music.tempo(100)
        # Gentle surprise
        self.music.play_tone_for(self.music.note("C4"), self.music.beat(1/4))
        self.music.play_tone_for(self.music.note("F4"), self.music.beat(1/2))
        self.music.play_tone_for(self.SILENCE, self.music.beat(1/8))
        self.music.play_tone_for(self.music.note("G4"), self.music.beat(1))

def demo_all_emotions():
    """Play all gentle emotional sounds with announcements"""
    sounds = GentleEmotionalSounds()
    emotions = [
        "happy", "sad", "angry", "excited",
        "sleepy", "curious", "confused", "surprised"
    ]
    
    print("Starting gentle emotion sounds demo...")
    for emotion in emotions:
        print(f"\nPlaying {emotion} sound...")
        getattr(sounds, emotion)()
        time.sleep(1)  # Longer pause for better separation
    print("\nDemo completed!")

if __name__ == "__main__":
    demo_all_emotions()