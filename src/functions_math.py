import math


# constants
SQRT3 = math.sqrt(3)


# functions

def world2screen(point, offset_x, offset_y, scale = 1):
# calculate coordinates from world coordinate system to screen coordinate system
# return coordinates in the screen coordinate system
    return ((point[0] + offset_x)*scale, (point[1] + offset_y)*scale)


def screen2world(point, offset_x, offset_y, scale = 1):
# calculate coordinates from screen coordinate system to world coordinate system
# return coordinates in the world coordinate system
    return (point[0]/scale - offset_x, point[1]/scale - offset_y)


def move_point(point, offset, angle):
# function that change coordinates of point by angle and offset
    return (point[0] + offset * math.cos(angle), point[1] + offset * math.sin(angle))


def dist_two_points(point1, point2):
# function that calculate distance between two points
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def dist_two_points_square(point1, point2):
# function that calculate square of distance between two points
    return (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2