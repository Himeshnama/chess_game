import cv2
def capture_img(path):
    cam = cv2.VideoCapture(2)
    ret, frame = cam.read()
    cv2.waitKey(delay=1)
    cv2.imwrite(path, frame)

if __name__ == "__main__":
    capture_img()

