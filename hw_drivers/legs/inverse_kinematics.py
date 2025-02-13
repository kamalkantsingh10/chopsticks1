from robot_hat import Servo
import time
import math
import numpy as np

SERVO_SEPARATION = 20   # Distance between servo centers
HORN_LENGTH = 40       # Servo horn length
LOWER_BAR = 71        # Lower bar length
DEFAULT_STAND_Y=40


class FiveBarLinkage:
    def __init__(self, inner_pin, outer_pin):
        self.servo_a = Servo(f"P{inner_pin}")  # Left servo
        self.servo_b = Servo(f"P{outer_pin}")  # Right servo

        self.d = SERVO_SEPARATION  # Distance between servos
        self.l1 = HORN_LENGTH     # Horn length (both servos)
        self.l2 = LOWER_BAR       # Lower bar length (both sides)

        self.current_a = 0
        self.current_b = 0

    def _ik_solve(self, x, y):
        try:
            x_a = x            # Left servo is reference at (0,0)
            x_b = x - self.d   # Right servo is offset by -d

            r_a = math.sqrt(x_a**2 + y**2)     # Distance from left servo
            r_b = math.sqrt(x_b**2 + y**2)     # Distance from right servo

            if r_a > (self.l1 + self.l2) or r_b > (self.l1 + self.l2):
                raise ValueError("Target point out of reach")

            cos_a2 = (r_a**2 - self.l1**2 - self.l2**2) / (-2 * self.l1 * self.l2)
            a2 = math.acos(max(-1, min(1, cos_a2)))
            a1 = math.atan2(y, x_a) + math.atan2(self.l2 * math.sin(a2),
                                                self.l1 + self.l2 * math.cos(a2))
            angle_a = -math.degrees(a1)

            cos_b2 = (r_b**2 - self.l1**2 - self.l2**2) / (-2 * self.l1 * self.l2)
            b2 = math.acos(max(-1, min(1, cos_b2)))
            b1 = math.atan2(y, x_b) - math.atan2(self.l2 * math.sin(b2),
                                                self.l1 + self.l2 * math.cos(b2))
            angle_b = math.degrees(b1)

            return angle_a+90, 90-angle_b

        except Exception as e:
            print(f"IK calculation error: {str(e)}")
            return None, None

    def move_to(self, x, y):
        angles = self.solve_ik(x, y)
        print(f"Target: ({x}, {y}), Angles: {angles}")
        if angles[0] is not None and angles[1] is not None:
            self.servo_a.angle(angles[0])
            self.servo_b.angle(angles[1])
            self.current_a = angles[0]
            self.current_b = angles[1]
            return True
        return False

    def solve_ik(self, x, y):
        pass


class FiveBarLinkageLeftleg(FiveBarLinkage):
    def __init__(self, inner_pin, outer_pin):
        super().__init__(inner_pin, outer_pin)

    def solve_ik(self, x, y):
        angle_a, angle_b = self._ik_solve(x,y)
        return angle_a, angle_b


class FiveBarLinkageRightleg(FiveBarLinkage):
    def __init__(self, inner_pin, outer_pin):
        super().__init__(outer_pin, inner_pin)

    def solve_ik(self, x, y):
        angle_a, angle_b = self._ik_solve(x,y)
        return -1*angle_a, -1*angle_b


class QuadrupedLeg_left:
    def __init__(self, servo_a_pin, servo_b_pin):
        self.linkage = FiveBarLinkageLeftleg(servo_a_pin, servo_b_pin)
        self.current_x = SERVO_SEPARATION/2
        self.current_y = DEFAULT_STAND_Y  # Default height

    def move(self, x, y):
        actual_x = x + SERVO_SEPARATION/2
        success = self.linkage.move_to(actual_x, y)
        if success:
            self.current_x = x
            self.current_y = y
        return success


class QuadrupedLeg_right:
    def __init__(self, servo_a_pin, servo_b_pin):
        self.linkage = FiveBarLinkageRightleg(servo_a_pin, servo_b_pin)
        self.current_x = SERVO_SEPARATION/2
        self.current_y = DEFAULT_STAND_Y  # Default height

    def move(self, x, y):
        actual_x = x + SERVO_SEPARATION/2
        success = self.linkage.move_to(actual_x, y)
        if success:
            self.current_x = x
            self.current_y = y
        return success