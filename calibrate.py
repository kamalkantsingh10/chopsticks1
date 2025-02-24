
from robot_hat import Servo
import time


for i in range(0,12):
    Servo(f"P{i}").angle(0)
    time.sleep(1)
    print (f"setting 0 to servo: {i} ")