# Example usage:
from controllers.audio import AudioController
from controllers.face import FaceController
from controllers.head import HeadController
from controllers.indicator import indicator
from core.enums import Emotion, Intensity,ServoConfig, Position
import time

from hw_drivers.legs.leg_movement import QuadrupedController



def demo_head_movements():
    """Demonstrate various head movements"""
    # Create servo configurations
    pan_config = ServoConfig(
        pin=2,
        min_angle=-65,
        max_angle=65,
        default_speed=1.0
    )
    
    tilt_config = ServoConfig(
        pin=3,
        min_angle=-30,
        max_angle=30,
        default_speed=1.0
    )
    
    # Initialize head controller
    head = HeadController(pan_config, tilt_config)
    
    try:
        print("Starting head movement demo...")
        
        # Test yes/no movements with different intensities
        print("Nodding yes (LOW intensity)...")
        head.nod_yes(cycles=2, intensity=Intensity.MILD)
        time.sleep(0.5)
        
        print("Nodding yes (HIGH intensity)...")
        head.nod_yes(cycles=2, intensity=Intensity.INTENSE)
        time.sleep(0.5)
        
        print("Shaking no (LOW intensity)...")
        head.shake_no(cycles=2, intensity=Intensity.MILD)
        time.sleep(0.5)
        
        print("Shaking no (HIGH intensity)...")
        head.shake_no(cycles=2, intensity=Intensity.INTENSE)
        time.sleep(0.5)
        
        # Test some additional movements
        print("Looking around...")
        head.move_to(Position(30, 0), 1.0)  # Look right
        time.sleep(0.5)
        head.move_to(Position(-30, 0), 1.0)  # Look left
        time.sleep(0.5)
        head.move_to(Position(0, 20), 1.0)   # Look up
        time.sleep(0.5)
        head.move_to(Position(0, -20), 1.0)  # Look down
        time.sleep(0.5)
        
        # Return to center
        print("Returning to center...")
        head.move_to(Position(0, 0), 1.0)
        
    finally:
        # Ensure cleanup happens even if demo is interrupted
        pass

def demo_audio():
    controller = AudioController()
    
    # These calls will return immediately (non-blocking)
    controller.speak("Life is very cool", Emotion.HAPPY, Intensity.NORMAL)
    
    # Wait a bit to let the speech complete
    import time
    time.sleep(3)
    
    # This one will be processed since previous speech is done
    controller.speak("Chopsticks happy", Emotion.EXCITED, Intensity.INTENSE)
    print("Even more work...")
    
    time.sleep(2)
    controller.cleanup()


def demo_face():
    """Run the display"""
    display = FaceController()
    try:
        display.run()
    except KeyboardInterrupt:
        print("Display stopped by user")
        display.cleanup()



def demo_body():
    robot = QuadrupedController()
    
    # # Test sequence
    # print("Testing poses...")
    
    # # Stand
    # print("Standing...")
    # robot.move_to_pose('stand')
    # time.sleep(1)
    
    # # Sit
    # print("Sitting...")
    # robot.move_to_pose('bow')
    # time.sleep(1)
    
    # # Lie down
    # print("Lying down...")
    # robot.move_to_pose('lie')
    # time.sleep(1)
    
    # # Bow
    # print("Bowing...")
    # robot.move_to_pose('bow')
    # time.sleep(1)
    
    # # Alert
    # print("Alert stance...")
    # robot.move_to_pose('alert')
    # time.sleep(1)
    
    # # Back to stand
    # print("Standing...")
    # robot.move_to_pose('stand')


   
    robot.walk(
    num_steps=8,
    step_height=20,
    step_length=50,
    neutral_height=40
    )

    

if __name__ == "__main__":
    #demo_face()
    
    indicator()
