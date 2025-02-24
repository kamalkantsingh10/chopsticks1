from core.enums import Emotion, ServoConfig
from time import sleep
from controllers.tail import TailController
from robot_hat import Servo
# Initialize servo config
config = ServoConfig(
    pin=1,  # Assuming servo is connected to pin 1
    min_angle=-90,
    max_angle=90,
    default_speed= 1.0
)
# Servo("P1").angle(0)

# Create tail controller
tail = TailController(config)

try:
    print("Starting tail emotions demo...")
    
    # Happy
    print("\nHAPPY - Fast, medium amplitude wagging")
    tail.set_emotion(Emotion.HAPPY)
    sleep(4)
    
    # Excited
    print("\nEXCITED - Very fast, high amplitude wagging")
    tail.set_emotion(Emotion.EXCITED)
    sleep(4)
    
    # Alert
    print("\nALERT - Still, raised tail")
    tail.set_emotion(Emotion.ALERT)
    sleep(3)
    
    # Curious
    print("\nCURIOUS - Slow, questioning side-to-side movement")
    tail.set_emotion(Emotion.CURIOUS)
    sleep(4)
    
    # Loving
    print("\nLOVING - Gentle, rhythmic medium wagging")
    tail.set_emotion(Emotion.LOVING)
    sleep(4)
    
    # Mischievous
    print("\nMISCHIEVOUS - Random, unpredictable movements")
    tail.set_emotion(Emotion.MISCHIEVOUS)
    sleep(4)
    
    # Grumpy
    print("\nGRUMPY - Stiff, minimal movement, slightly raised")
    tail.set_emotion(Emotion.GRUMPY)
    sleep(3)
    
    # Sad
    print("\nSAD - Slow, small amplitude, droopy tail")
    tail.set_emotion(Emotion.SAD)
    sleep(3)
    
    # Sleepy
    print("\nSLEEPY - Very slow, minimal movement")
    tail.set_emotion(Emotion.SLEEPY)
    sleep(3)
    
    # Scared
    print("\nSCARED - Tucked tail")
    tail.set_emotion(Emotion.SCARED)
    sleep(3)
    
    # Back to neutral
    print("\nNEUTRAL - No movement, neutral position")
    tail.set_emotion(Emotion.NEUTRAL)
    sleep(2)
    
    print("\nDemo complete!")

except KeyboardInterrupt:
    print("\nDemo stopped by user")
finally:
    tail.cleanup()
    print("Tail controller cleaned up")