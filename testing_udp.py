from core.enums import Position, ServoConfig, Emotion
from controllers.head import HeadController
from emotions.head import Head_Emotions
import time


# Initialize the head controller with your servo configurations
pan_config = ServoConfig(pin=2, min_angle=-90, max_angle=90,default_speed=1.0)
tilt_config = ServoConfig(pin=3, min_angle=-45, max_angle=45,default_speed=1.0)
head = HeadController(pan_config, tilt_config)

# Create the emotion controller
emotion_ctrl = Head_Emotions(head)
print ("happy")

# Start expressing an emotion (will continue until stopped or changed)
emotion_ctrl.express(Emotion.HAPPY)

time.sleep(10)
print ("sad")

# Later, change to another emotion
emotion_ctrl.express(Emotion.SAD)
print ("excited")
# Stop expressing emotions
time.sleep(10)
emotion_ctrl.express(Emotion.EXCITED)

# Stop expressing emotions
print ("alert")
time.sleep(10)
emotion_ctrl.express(Emotion.ALERT)

# Stop expressing emotions
print ("curious")
time.sleep(10)
emotion_ctrl.express(Emotion.CURIOUS)

# Stop expressing emotions
print ("sleepy")
time.sleep(10)
emotion_ctrl.express(Emotion.SLEEPY)

# Stop expressing emotions
print ("loving")
time.sleep(10)
emotion_ctrl.express(Emotion.LOVING)

# Stop expressing emotions
print ("grumpy")
time.sleep(10)
emotion_ctrl.express(Emotion.GRUMPY)

# Stop expressing emotions
print ("scared")
time.sleep(10)
emotion_ctrl.express(Emotion.SCARED)

# Stop expressing emotions
print ("mischievious")
time.sleep(10)
emotion_ctrl.express(Emotion.MISCHIEVOUS)

# Stop expressing emotions
time.sleep(10)
print ("neutral")
emotion_ctrl.express(Emotion.NEUTRAL)

# Stop expressing emotions
time.sleep(10)
emotion_ctrl.stop()