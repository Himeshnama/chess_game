import numpy as np
import cv2
import glob
import sys
import os

nline = 7
ncol = 7

img = cv2.imread("img1.png")

## termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

## processing
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find the chessboard corners
ret, corners = cv2.findChessboardCorners(gray, (nline, ncol), None)
print(corners)
corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)