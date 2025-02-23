from enum import Enum
import random
import time
import threading
from core.enums import Position, ServoConfig, Emotion
from typing import Optional
from controllers.head import HeadController


class Head_Emotions:
    def __init__(self, head_controller):
        """
        Initialize the EmotionController with a reference to the HeadController
        
        Args:
            head_controller: Instance of HeadController to manipulate
        """
        self.head = head_controller
        self.current_emotion = Emotion.NEUTRAL
        self.last_emotion_time = time.time()
        self._running = False
        self._emotion_thread = None
        self._stop_event = threading.Event()
        
    def express(self, emotion: Emotion) -> None:
        """
        Express the given emotion continuously until stopped
        
        Args:
            emotion: The emotion to express
        """
        # Stop any currently running emotion
        self.stop()
        
        # Update current emotion
        self.current_emotion = emotion
        self.last_emotion_time = time.time()
        
        # Start emotion expression in a new thread
        self._stop_event.clear()
        self._running = True
        self._emotion_thread = threading.Thread(target=self._emotion_loop, args=(emotion,))
        self._emotion_thread.daemon = True
        self._emotion_thread.start()
    
    def stop(self) -> None:
        """Stop the current emotion expression"""
        if self._running:
            self._stop_event.set()
            if self._emotion_thread and self._emotion_thread.is_alive():
                self._emotion_thread.join(timeout=1.0)
            self._running = False
            
            # Return to neutral position
            self.head.move_to(Position(0, 0), 1.0)
    
    def _emotion_loop(self, emotion: Emotion) -> None:
        """
        Continuously express an emotion until stopped
        
        Args:
            emotion: The emotion to express
        """
        # First express the emotion fully
        self._express_emotion_once(emotion)
        
        # Then enter a loop of milder expressions
        while not self._stop_event.is_set():
            # Add some randomness to timing between expressions
            wait_time = random.uniform(1.0, 3.0)
            
            # Use Event.wait() with a timeout so we can check if we should stop
            if self._stop_event.wait(timeout=wait_time):
                break
                
            # Express the emotion in a milder way
            self._express_emotion_once(emotion, is_continuation=True)
    
    def _express_emotion_once(self, emotion: Emotion, is_continuation: bool = False) -> None:
        """
        Express the emotion once
        
        Args:
            emotion: The emotion to express
            is_continuation: Whether this is a continuation (milder version)
        """
        # Call the appropriate method based on the emotion
        if emotion == Emotion.HAPPY:
            self._express_happy(is_continuation)
        elif emotion == Emotion.SAD:
            self._express_sad(is_continuation)
        elif emotion == Emotion.EXCITED:
            self._express_excited(is_continuation)
        elif emotion == Emotion.ALERT:
            self._express_alert(is_continuation)
        elif emotion == Emotion.CURIOUS:
            self._express_curious(is_continuation)
        elif emotion == Emotion.SLEEPY:
            self._express_sleepy(is_continuation)
        elif emotion == Emotion.LOVING:
            self._express_loving(is_continuation)
        elif emotion == Emotion.GRUMPY:
            self._express_grumpy(is_continuation)
        elif emotion == Emotion.SCARED:
            self._express_scared(is_continuation)
        elif emotion == Emotion.MISCHIEVOUS:
            self._express_mischievous(is_continuation)
        elif emotion == Emotion.NEUTRAL:
            self._express_neutral(is_continuation)
    
    def _express_happy(self, is_continuation: bool) -> None:
        """
        Express happiness through gentle nodding and slight upward tilt
        """
        # Slightly upward tilt for happy expression
        base_position = Position(0, -8)
        
        if is_continuation:
            self.head.move_to(base_position, 0.8)
            time.sleep(0.1)
            
            if random.choice([True, False]):
                self.head.move_to(Position(random.uniform(-5, 5), base_position.y + 6), 0.7)
                time.sleep(0.1)
                self.head.move_to(base_position, 0.6)
            else:
                self.head.move_to(Position(7, base_position.y - 12), 0.7)
                time.sleep(0.1)
                self.head.move_to(base_position, 0.6)
        else:
            self.head.move_to(base_position, 0.9)
            time.sleep(0.2)
            self.head.nod_yes(cycles=1, base_tilt=base_position.y)
            self.head.move_to(Position(5, base_position.y - 3), 0.8)
            time.sleep(0.1)
            self.head.move_to(base_position, 0.7)
    
    def _express_sad(self, is_continuation: bool) -> None:
        """
        Express sadness through downward tilt and slow, minimal movement
        """
        # Downward tilt for sad expression - milder
        tilt_value = 18  # Increased tilt
        
        if is_continuation:
            current_pos = self.head.current_position
            self.head.move_to(Position(random.uniform(-4, 4), tilt_value), 0.8)
            time.sleep(0.2)
            self.head.move_to(Position(random.uniform(-3, 3), tilt_value + 4), 0.6)
            time.sleep(0.3)
        else:
            self.head.move_to(Position(0, tilt_value), 1)
            time.sleep(0.3)
            
            self.head.move_to(Position(-4, tilt_value + 2), 0.8)
            time.sleep(0.3)
            self.head.move_to(Position(4, tilt_value + 3), 0.8)
            time.sleep(0.3)
            
            self.head.move_to(Position(0, tilt_value + 4), 0.6)
            time.sleep(0.2)
            self.head.move_to(Position(0, tilt_value), 0.6)
    
    def _express_excited(self, is_continuation: bool) -> None:
        """
        Express excitement through more frequent but gentler movements
        """
        # Milder upward tilt
        base_tilt = -8
        
        if is_continuation:
            # Shorter, milder movements for continuation
            # Quick but small side-to-side movement
            pan = random.choice([-8, 8])
            self.head.move_to(Position(pan, base_tilt + random.uniform(-2, 2)), 1.2)
            time.sleep(0.8)
            self.head.move_to(Position(0, base_tilt), 1.0)
        else:
            # Initial expression
            # Quick upward tilt
            self.head.move_to(Position(0, base_tilt), 1.2)
            
            # Mix of nodding and side-to-side movements, but milder
            for i in range(2):  # Fewer cycles
                # Smaller movements
                self.head.move_to(Position(random.choice([-8, 8]), base_tilt + random.uniform(-3, 3)), 1.2)
                self.head.move_to(Position(random.choice([-8, 8]), base_tilt - 2 + random.uniform(-2, 2)), 1.2)
                
                # Quick side movement
                pan = 10 if i % 2 == 0 else -10  # Reduced pan amount
                self.head.move_to(Position(pan, base_tilt + random.uniform(-2, 2)), 1.2)
            
            # Return to base position
            self.head.move_to(Position(0, base_tilt), 1.0)
    
    def _express_alert(self, is_continuation: bool) -> None:
        """
        Express alertness through gentle scanning
        """
        # Milder upward movement
        base_tilt = -10
        
        if is_continuation:
            # For continuation, just do a single random scan
            scan_direction = random.choice([-1, 1])
            scan_range = 15  # Reduced range
            
            # Quick scan in chosen direction
            self.head.move_to(Position(scan_range * scan_direction, base_tilt), 1.0)
            time.sleep(0.2)
            self.head.move_to(Position(0, base_tilt), 0.8)
        else:
            # Initial expression
            # Upward and centered movement
            self.head.move_to(Position(0, base_tilt), 1.2)
            time.sleep(0.1)
            
            # Milder scanning movements
            scan_range = 15  # Reduced range
            
            # Perform a scanning pattern
            positions = [
                Position(-scan_range, base_tilt),  # Left
                Position(0, base_tilt),            # Center
                Position(scan_range, base_tilt),   # Right
                Position(0, base_tilt),            # Center
            ]
            
            for pos in positions:
                self.head.move_to(pos, 0.9)
                time.sleep(0.1)
    
    def _express_curious(self, is_continuation: bool) -> None:
        """
        Express curiosity through gentle tilted head and small investigative movements
        """
        # Milder head tilt
        tilt = 5
        
        if is_continuation:
            # For continuation, just do a small investigative movement
            side = random.choice([-1, 1])
            # Small movement to one side with slight tilt
            self.head.move_to(Position(8 * side, tilt), 0.7)
            time.sleep(0.2)
            # Small adjustment as if examining
            self.head.move_to(Position(10 * side, tilt - 2), 0.6)
            time.sleep(0.2)
            # Return to center
            self.head.move_to(Position(0, 0), 0.7)
        else:
            # Initial expression
            # Pan to one side with tilt
            self.head.move_to(Position(8, tilt), 0.8)
            time.sleep(0.2)
            
            # Small adjustments as if examining something
            self.head.move_to(Position(10, tilt - 2), 0.7)
            time.sleep(0.2)
            self.head.move_to(Position(6, tilt - 3), 0.7)
            time.sleep(0.2)
            
            # Move to opposite side as if checking from different angle
            self.head.move_to(Position(-8, tilt), 0.9)
            time.sleep(0.2)
            self.head.move_to(Position(-6, tilt - 2), 0.7)
            time.sleep(0.2)
            
            # Return to slightly tilted position
            self.head.move_to(Position(0, 2), 0.8)
    
    def _express_sleepy(self, is_continuation: bool) -> None:
        """
        Express sleepiness through drooping head and slow movements
        """
        # Milder drooping head position
        droop = 15  # Increased droop
        
        if is_continuation:
            current_pos = self.head.current_position
            # Gentler droop motion with slower speed
            self.head.move_to(Position(current_pos.x, droop + 3), 0.7)  # Increased from 0.4 to 0.7
            time.sleep(0.6)  # Increased from 0.4 to 0.6
            
            # Very subtle side movement, slower
            self.head.move_to(Position(current_pos.x + random.uniform(-2, 2), droop + 2), 0.7)  # Increased from 0.4 to 0.7
            time.sleep(0.5)  # Increased from 0.3 to 0.5
            self.head.move_to(Position(current_pos.x, droop), 0.8)  # Increased from 0.5 to 0.8
        else:
            # Initial gentle droop, slower
            self.head.move_to(Position(0, droop), 0.8)  # Increased from 0.5 to 0.8
            time.sleep(0.7)  # Increased from 0.5 to 0.7
            
            # Single subtle nodding cycle, slower
            self.head.move_to(Position(random.uniform(-2, 2), droop + 4), 0.7)  # Increased from 0.4 to 0.7
            time.sleep(0.5)  # Increased from 0.3 to 0.5
            self.head.move_to(Position(0, max(0, droop - 2)), 0.8)  # Increased from 0.5 to 0.8
            time.sleep(0.4)  # Increased from 0.2 to 0.4
            
            # Return to gentle drooped position, slower
            self.head.move_to(Position(0, droop), 0.7)  # Increased from 0.4 to 0.7
    
    def _express_loving(self, is_continuation: bool) -> None:
        """
        Express love/affection through gentle tilting and mild nuzzling movements
        """
        # Milder upward tilt
        base_tilt = -7  # More pronounced tilt
        
        if is_continuation:
            side = random.choice([-1, 1])
            self.head.move_to(Position(6 * side, base_tilt - 2), 0.4)
            time.sleep(0.2)
            
            # Add gentle nuzzle movement
            self.head.move_to(Position(4 * side, base_tilt - 4), 0.3)
            time.sleep(0.1)
            self.head.move_to(Position(0, base_tilt), 0.4)
        else:
            self.head.move_to(Position(0, base_tilt), 0.6)
            time.sleep(0.2)
            
            self.head.move_to(Position(7, base_tilt - 2), 0.5)
            time.sleep(0.2)
            self.head.move_to(Position(-7, base_tilt + 2), 0.5)
            time.sleep(0.2)
            
            self.head.move_to(Position(0, base_tilt + 4), 0.4)
            time.sleep(0.1)
            self.head.move_to(Position(0, base_tilt), 0.5)
    
    def _express_grumpy(self, is_continuation: bool) -> None:
        """
        Express grumpiness through mild downward tilt and subtle abrupt movements
        """
        # Milder downward position
        tilt = 8
        
        if is_continuation:
            # For continuation, just do a small grumpy movement
            # Quick look away
            side = random.choice([-1, 1])
            self.head.move_to(Position(6 * side, tilt), 0.7)
            time.sleep(0.2)
            
            # Optional small shake
            if random.choice([True, False]):
                other_side = -1 * side
                self.head.move_to(Position(3 * other_side, tilt), 0.7)
        else:
            # Initial expression
            # Movement to downward position
            self.head.move_to(Position(-5, tilt), 0.8)
            time.sleep(0.2)
            
            # Milder head shake
            # Do a manual smaller shake instead of using shake_no
            self.head.move_to(Position(5, tilt), 0.8)
            time.sleep(0.1)
            self.head.move_to(Position(-5, tilt), 0.8)
            
            # Quick look away movement
            self.head.move_to(Position(8, tilt + 3), 0.9)
            time.sleep(0.2)
            
            # Final grumpy position - slightly down and away
            self.head.move_to(Position(5, tilt), 0.7)
    
    def _express_scared(self, is_continuation: bool) -> None:
        """
        Express fear through milder retreating movements and scanning
        """
        # Milder recoil position
        recoil_tilt = 15
        
        if is_continuation:
            # For continuation, just do a small nervous movement
            # Quick scan
            pan = random.uniform(-15, 15)
            self.head.move_to(Position(pan, recoil_tilt), 0.9)
            time.sleep(0.1)
            
            # Optional small shake
            if random.choice([True, False]):
                shake_amount = 2
                self.head.move_to(Position(pan + shake_amount, recoil_tilt), 0.8)
                self.head.move_to(Position(pan - shake_amount, recoil_tilt), 0.8)
                self.head.move_to(Position(pan, recoil_tilt), 0.6)
        else:
            # Initial expression
            # More gentle backward motion
            self.head.move_to(Position(0, recoil_tilt), 1.2)
            time.sleep(0.1)
            
            # Milder scanning movements
            for _ in range(2):  # Fewer scans
                # Less extreme movements
                pan = random.uniform(-15, 15)
                tilt = random.uniform(10, recoil_tilt)
                self.head.move_to(Position(pan, tilt), 0.9)
                time.sleep(0.1)
            
            # Small shake
            shake_amount = 2
            self.head.move_to(Position(shake_amount, recoil_tilt), 0.7)
            self.head.move_to(Position(-shake_amount, recoil_tilt), 0.7)
            
            # End in slightly recoiled position
            self.head.move_to(Position(0, 10), 0.6)
    
    def _express_mischievous(self, is_continuation: bool) -> None:
        """
        Express mischievousness through milder playful, sneaky movements
        """
        # Milder sneaky position
        base_tilt = 3
        
        if is_continuation:
            # For continuation, just do a small sneaky glance
            # Quick side glance
            side = random.choice([-1, 1])
            self.head.move_to(Position(10 * side, base_tilt), 0.7)
            time.sleep(0.2)
            
            # Small playful movement
            if random.choice([True, False]):
                self.head.move_to(Position(10 * side, base_tilt - 3), 0.6)
                time.sleep(0.1)
                self.head.move_to(Position(10 * side, base_tilt), 0.5)
        else:
            # Initial expression
            # Slightly lowered, sneaky position
            self.head.move_to(Position(0, base_tilt), 0.7)
            time.sleep(0.2)
            
            # Milder sneaky side-to-side movements
            # Sneaky side glances
            self.head.move_to(Position(12, base_tilt), 0.8)  # Look right sneakily
            time.sleep(0.2)
            self.head.move_to(Position(-12, base_tilt), 0.8)  # Look left sneakily
            time.sleep(0.2)
            
            # Milder playful up-down movement
            self.head.move_to(Position(0, base_tilt - 5), 0.8)  # Look up
            time.sleep(0.1)
            self.head.move_to(Position(0, base_tilt + 5), 0.9)  # Look down
            
            # End with slight tilt, as if up to something
            self.head.move_to(Position(5, base_tilt), 0.6)
    
    def _express_neutral(self, is_continuation: bool = False) -> None:
        """
        Express neutral state - return to center position with slight variance
        """
        # Add very slight variance so it's not too robotic
        random_offset = random.uniform(-12, 12)
        self.head.move_to(Position(random_offset, 0), 0.8)