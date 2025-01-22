from robot_hat import Servo, Motors
import time

delay=0.005

def run_servo(n, angle=20): 
    """test servo and set them to 1"""
    servo0= Servo(f"P{n}")
    print("Setting servo",{n},"to 1")
    for i in range(0, angle):
        servo0.angle(i)
        time.sleep(delay)
    for i in range(angle, (-1*angle), -1):
        servo0.angle(i)
        time.sleep(delay)
    for i in range(-1*angle, 1):
        servo0.angle(i)
        time.sleep(delay)

    servo0.angle(0)                                                                                                                                                                                                                                                                                                                                                                                                                                           
    time.sleep(1)
    


