"""
Data
================

data storage and manipulation classes, should be sufficient to run the game without display
"""
from enum import Enum
import numpy


class Facing(Enum):
    YP = 0
    XP = 1
    ZN = 2
    YN = 3
    XN = 4
    ZP = 5


# gives a directional delta array in hex coordinates for given Facing
def facing_array(enum):
    if enum == Facing.YP:
        return [0, 1, 0]
    if enum == Facing.XP:
        return [1, 0, 0]
    if enum == Facing.ZN:
        return [0, 0, -1]
    if enum == Facing.YN:
        return [0, -1, 0]
    if enum == Facing.XN:
        return [-1, 0, 0]
    if enum == Facing.ZP:
        return [0, 0, 1]
    raise Exception(f'{enum} is not a valid Facing')


class Body:
    def __init__(self, position=None, momentum=None, facing=Facing.YP, image=''):
        if momentum is None:
            momentum = [0, 0, 0]
        if position is None:
            position = [[0, 0]]
        self.facing = facing
        self.position = position  # hex x y positions
        self.momentum = momentum  # hex x y z velocities
        self._momentum_next = [0, 0, 0]  # hex  x y z velocities
        self.image = image

    # single hex movement by provided direction, none or 0 for inaction
    def move(self, direction=None):
        if direction is None:
            direction = [0, 0, 0]
        else:
            direction = facing_array(direction)
        numpy.add(self.position, direction)
        numpy.add(self.momentum_next, direction)

    # positive rotations are clockwise
    def rotate(self, rotations, pivot=None):
        if pivot is None:
            pivot = self.position[0]
        self.facing += rotations
        if len(self.position) > 1:
            for r in range(0, abs(rotations)):
                if rotations > 0:
                    for i in range(0, len(self.position)):
                        p = numpy.subtract(self.position[i], pivot)
                        p = [-p[2], -p[0], -p[1]]
                        self.position[i] = numpy.add(p, pivot)
                else:
                    for i in range(0, len(self.position)):
                        p = numpy.subtract(self.position[i], pivot)
                        p = [-p[1], -p[2], -p[10]]
                        self.position[i] = numpy.add(p, pivot)

    # 1 = 60°, 6 rotations in a 360° turn
    def degree_facing(self):
        return self.facing * 60

    def elapse_turn(self):
        self.momentum = self._momentum_next
        self._momentum_next = [0, 0, 0]


class Ship(Body):
    def __init__(self, position=None, momentum=None, facing=Facing.YP,
                 image='', speed=1, rotation_speed=1, move_directions=[Facing.YP]):
        super().__init__(position, momentum, facing, image)
        self.speed = speed  # number of movement/rotation actions you can make in a turn
        self.action_points = speed
        self.rotation_speed = rotation_speed  # number of 60 degree turns allowed in one rotation action
        self.move_directions = move_directions  # legal directions to make moves in

    def move(self, direction=None):
        if direction is None:
            direction = [0, 0, 0]
        elif direction in self.move_directions:
            super().move(self, direction)
        else:
            raise Exception(f'Invalid move direction {direction}, valid directions are {self.move_directions}')
        self.action_points -= 1

    def rotate(self, rotations, pivot=None):
        return


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bodies = []






# NOTES FROM INITIAL GAME PLAY MECHANICS REVIEW:
#
# Body():
# (x, y)[]
# position
# (x1, x2, y)
# momentum
# (x1, x2, y)
# momentum_next
#
#
# def rotate((x, y)pivot, rotations
#
# ):
#
# # updates position
#
# def move((x1, x2, y)direction
#
# ):
# # updates position and momentum_next
#
#
# ImmutableBody(Body):
#
#
# def rotate((x, y)pivot, rotations
#
# ):
# return
#
#
# def move((x1, x2, y)direction
#
# ):
# return
#
# Ship(Body):
# rotation_speed
# speed
# Facing[]
# legal_moves  # which direction thrusters can take us, 1 non zero value in tuple
#
#
# def rotate((x, y)pivot, rotations
#
# ):
# # if you rotate your legal_moves must update
#
#
# Map():
# x_width
# y_width
# []
# bodies
#
#
# class Facing(Enum):
#     YP = 0
#     X1P = 1
#     X2P = 2
#     YN = 3
#     X1N = 4
#     X2N = 5
