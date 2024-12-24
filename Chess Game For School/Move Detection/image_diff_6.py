from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import cv2
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import math


################### HELP FUNCTIONS ######################

def find_corners(image):
    corners = []

    boundaries = [
        ([20, 20, 130], [120, 100, 255])
    ]

    lower = boundaries[0][0]
    upper = boundaries[0][1]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    # show the images
    contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
    for c in contour:
        area = cv2.contourArea(c)

        if area > 3:
            x, y, w, h = cv2.boundingRect(c)
            corners.append((round(x + w/2), round(y + h/2)))
            #cv2.rectangle(image, (round(x + w/2), round(y + h/2)), (x + w, y + h), (255, 0, 0), 2)
            #cv2.drawContours(image, c, -1, (255, 0, 0), 2)

    return corners

def arrange_clockwise(pts):
    top_points = []
    bottom_points = []
    for point in pts:
        if point[1] < 200:
            top_points.append(point)
        else:
            bottom_points.append(point)
    
    if top_points[0][0] > top_points[1][0]:
        top_points.append(top_points[0])
        top_points.remove(top_points[0])
    
    if bottom_points[1][0] > bottom_points[0][0]:
        bottom_points.append(bottom_points[0])
        bottom_points.remove(bottom_points[0])

    arranged = top_points + bottom_points

    return arranged

def detect_square(pix, corners):
    # point = Point(125, 27)
    # polygon = Polygon(arrange_clockwise(find_corners(imageA)))
    # corners = arrange_clockwise(corners)
    # print(corners)
    # divided_top_coordinates = divide_line([corners[0], corners[1]])
    # divided_bottom_coordinates = divide_line([corners[3], corners[2]])
    corners = arrange_clockwise(corners)

    x = detect_column(pix, corners)
    y = detect_row(pix, corners)

    print((x, y))

def detect_column(pix, corners):
    divided_top_coordinates = divide_line_into_column([corners[0], corners[1]])
    divided_bottom_coordinates = divide_line_into_column([corners[3], corners[2]])

    point = Point(pix[0], pix[1])

    for i in range(0,8):
        A = divided_top_coordinates[i]
        B = divided_top_coordinates[i+1]
        C = divided_bottom_coordinates[i+1]
        D = divided_bottom_coordinates[i]
        polygon = Polygon([A, B, C, D])
        if polygon.contains(point):
            return i + 1

def detect_row(pix, corners):
    divided_left_coordinates = divide_line_into_row([corners[0], corners[3]])
    divided_right_coordinates = divide_line_into_row([corners[1], corners[2]])

    point = Point(pix[0], pix[1])

    for i in range(0,8):
        A = divided_left_coordinates[i]
        B = divided_right_coordinates[i]
        C = divided_right_coordinates[i+1]
        D = divided_left_coordinates[i+1]
        polygon = Polygon([A, B, C, D])
        if polygon.contains(point):
            return i + 1

def divide_line_into_row(corners):
    coordintates = []
    x1, y1 = corners[0][0], corners[0][1]
    x2, y2 = corners[1][0], corners[1][1]

    try:
        m = (y1 - y2) / (x1 - x2)
    except:
        m = 0

    c = y1 - x1 * m

    dist = round((y2 - y1)/8)
    
    for y in range(y1, y2, dist):
        try:
            x = round((y - c)/ m)
        except:
            x = 0
        coordintates.append((x, y))

    if len(coordintates) < 9:
        coordintates.append((x2, y2))

    return coordintates


def divide_line_into_column(corners):
    coordintates = []
    x1, y1 = corners[0][0], corners[0][1]
    x2, y2 = corners[1][0], corners[1][1]

    try:
        m = (y1 - y2) / (x1 - x2)
    except:
        m = 0

    c = y1 - x1 * m

    dist = round((x2 - x1)/8)
    
    for x in range(x1, x2, dist):
        y = round((m * x) + c)
        coordintates.append((x, y))

    if len(coordintates) < 9:
        coordintates.append((x2, y2))

    return coordintates

###############################################################

#corners = [(77,27), (482, 20), ((500,450)), (32, 447)]

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True,
	help="first input image")
ap.add_argument("-s", "--second", required=True,
	help="second")
args = vars(ap.parse_args())

# load the two input images
imageA = cv2.imread(args["first"])
imageB = cv2.imread(args["second"])

# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if len(cnts) == 2 else cnts[1]

contour_sizes = [(cv2.contourArea(contour), contour) for contour in cnts]

result = imageB.copy()
# The largest contour should be the new detected difference
if len(contour_sizes) > 0:
    largest_contour_size = max(contour_sizes, key=lambda x: x[0])
    largest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    contour_sizes.remove(largest_contour_size)
    x,y,w,h = cv2.boundingRect(largest_contour)
    pix1 = (round(x + w/2), round(y +  h/2))
    cv2.rectangle(result, (x, y), (x + w, y + h), (36,255,12), 2)
    cv2.rectangle(result, (pix1[0] -1, pix1[1]-1), (pix1[0] +1, pix1[1]+1), (36,255,12), 2)

    largest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    x,y,w,h = cv2.boundingRect(largest_contour)
    pix2 = (round(x + w/2), round(y +  h/2))
    cv2.rectangle(result, (x, y), (x + w, y + h), (36,255,12), 2)
    cv2.rectangle(result, (pix2[0] -1, pix2[1]-1), (pix2[0] +1, pix2[1]+1), (36,255,12), 2)

print(find_corners(imageA))

sq1 = detect_square(pix1, find_corners(imageA))
sq2 = detect_square(pix2, find_corners(imageB))

cv2.imshow('result', result)
cv2.imshow('diff', diff)
cv2.waitKey()


