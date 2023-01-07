import math
from functions_math import *


def test_turn_to_target_angle():
# function that checks the correctness of the function "turn_to_target_angle(origin_angle, target_angle, turn_speed)":
    # function that slowly (by turn_speed) changes origin_angle in target_angle_direction
    # return angle in radians - in the range of 0 to 2pi

    turn_speed_rad = math.radians(1)
    # origin_angle, target_angle, result
    test_variables = [
            (15, 0, 14),
            (15, 45, 16),
            (15, 90, 16),
            (15, 135, 16),
            (15, 180, 16),
            (15, 225, 14),
            (15, 270, 14),
            (15, 315, 14),
            (15, 360, 14),

            (75, 0, 74),
            (75, 45, 74),
            (75, 90, 76),
            (75, 135, 76),
            (75, 180, 76),
            (75, 225, 76),
            (75, 270, 74),
            (75, 315, 74),
            (75, 360, 74),

            (105, 0, 104),
            (105, 45, 104),
            (105, 90, 104),
            (105, 135, 106),
            (105, 180, 106),
            (105, 225, 106),
            (105, 270, 106),
            (105, 315, 104),
            (105, 360, 104),

            (165, 0, 164),
            (165, 45, 164),
            (165, 90, 164),
            (165, 135, 164),
            (165, 180, 166),
            (165, 225, 166),
            (165, 270, 166),
            (165, 315, 166),
            (165, 360, 164),

            (195, 0, 196),
            (195, 45, 194),
            (195, 90, 194),
            (195, 135, 194),
            (195, 180, 194),
            (195, 225, 196),
            (195, 270, 196),
            (195, 315, 196),
            (195, 360, 196),

            (255, 0, 256),
            (255, 45, 256),
            (255, 90, 254),
            (255, 135, 254),
            (255, 180, 254),
            (255, 225, 254),
            (255, 270, 256),
            (255, 315, 256),
            (255, 360, 256),

            (285, 0, 286),
            (285, 45, 286),
            (285, 90, 286),
            (285, 135, 284),
            (285, 180, 284),
            (285, 225, 284),
            (285, 270, 284),
            (285, 315, 286),
            (285, 360, 286),

            (345, 0, 346),
            (345, 45, 346),
            (345, 90, 346),
            (345, 135, 346),
            (345, 180, 344),
            (345, 225, 344),
            (345, 270, 344),
            (345, 315, 344),
            (345, 360, 346),
    ]

    test_pass = True

    for test_case in test_variables:
        origin_angle_deg, target_angle_deg, result_deg = test_case
        origin_angle_rad = math.radians(origin_angle_deg)
        target_angle_rad = math.radians(target_angle_deg)

        calculated_result_rad = turn_to_target_angle(origin_angle_rad, target_angle_rad, turn_speed_rad)
        
        calculated_result_deg = round(math.degrees(calculated_result_rad))
        if result_deg != calculated_result_deg: 
            print(str(origin_angle_deg) + "\t" + str(target_angle_deg) + "\t", end="")
            print(str(calculated_result_deg))
            test_pass = False
        # else: 
        #     print(str(origin_angle_deg) + "\t" + str(target_angle_deg) + "\t", end="")
        #     print("True")

    if test_pass: print("Test turn_to_target_angle() successfully completed")

if __name__ == "__main__":
    test_turn_to_target_angle()