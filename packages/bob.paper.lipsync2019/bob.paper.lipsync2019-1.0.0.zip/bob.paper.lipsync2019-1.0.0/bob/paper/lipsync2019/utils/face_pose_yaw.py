#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import print_function

import numpy

import math
import cv2


# face 3D model estimation taken from:
# https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/

# 3D model points.
model_points = numpy.array([
    (0.0, 0.0, 0.0),  # Nose tip
    (0.0, -330.0, -65.0),  # Chin
    (-225.0, 170.0, -135.0),  # Left eye left corner
    (225.0, 170.0, -135.0),  # Right eye right corne
    (-150.0, -150.0, -125.0),  # Left Mouth corner
    (150.0, -150.0, -125.0)  # Right mouth corner

], dtype=numpy.float32)

# corresponding indexes in 2D face landmarks from dlib
# The dlib shape predictor returns 68 points, we are interested only in a few of those
tracked_points_from_dlib = [30, 8, 36, 45, 48, 54]


def camera_matrix(frame_dim):
    # camera matrix estimation
    focal_length = frame_dim[0]  # width of the frame
    # first width, then height
    center = (frame_dim[0] / 2, frame_dim[1] / 2)
    camera_matrix = numpy.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype=numpy.float32
    )
    return camera_matrix


# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
# taken from:
# https://programtalk.com/vs2/python/8766/deepgaze/deepgaze/head_pose_estimation.py
def rotationMatrixToEulerAngles(R):
    # assert(isRotationMatrix(R))

    # To prevent the Gimbal Lock it is possible to use
    # a threshold of 1e-6 for discrimination
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return numpy.array([x, y, z])


def face_pose_yaw(lmk, frame_dim):
    if numpy.all(lmk) == 0:
        return 0.9  # assume a 90 degrees yaw
    # 2D image points. If you change the image, you need to change vector
    image_points = lmk[tracked_points_from_dlib]
    camera_distortion_coeff = numpy.zeros((4, 1))  # Assuming no lens distortion
    success, rotation_vector, translation_vector = cv2.solvePnP(model_points, image_points,
                                                                camera_matrix(frame_dim), camera_distortion_coeff,
                                                                flags=cv2.SOLVEPNP_ITERATIVE)
    rmat, _ = cv2.Rodrigues(rotation_vector)
    # pitch, yaw, and roll
    angles = rotationMatrixToEulerAngles(rmat)
    return angles[1]  # return yaw
