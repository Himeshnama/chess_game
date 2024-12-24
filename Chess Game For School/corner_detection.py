# import the necessary packages
import numpy as np
import argparse
import cv2
# construct the argument parse and parse the arguments

corners = []
       
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
# load the image
# image = cv2.imread(args["image"])
image = cv2.imread("img1.png")
# boundaries = [
#    ([60, 78, 202], [0, 131, 255]),
# ]

boundaries = [
	([20, 20, 150], [120, 100, 255])
]

lower = boundaries[0][0]
upper = boundaries[0][1]

# create NumPy arrays from the boundaries
lower = np.array(lower, dtype = "uint8")
upper = np.array(upper, dtype = "uint8")
# find the colors within the specified boundaries and apply
# the mask
mask = cv2.inRange(image, lower, upper)
output = cv2.bitwise_and(image, image, mask = mask)
# show the images
contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
for c in contour:
    area = cv2.contourArea(c)

    if area > 3:
        x, y, w, h = cv2.boundingRect(c)
        corners.append((round(x + w/2), round(y + h/2)))

        cv2.rectangle(image, (round(x + w/2), round(y + h/2)), (x + w, y + h), (255, 0, 0), 2)
        cv2.drawContours(image, c, -1, (255, 0, 0), 2)
print(corners)

cv2.imshow("images", np.hstack([image, output]))
cv2.waitKey(0)