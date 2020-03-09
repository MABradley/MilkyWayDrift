import kivy
import numpy
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