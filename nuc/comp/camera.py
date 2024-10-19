import cv2
import sys

class Camera:

    def __init__(self, running_nuc, resizeWidth, resizeHeight, preBlur, postBlur):
        if running_nuc:
            self.camera = cv2.VideoCapture(0)
        else:
            self.camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.resizeWidth = resizeWidth
        self.resizeHeight = resizeHeight
        self.preBlur = preBlur
        self.postBlur = postBlur
        self.getHSVImage()

    def getHSVImage(self):
        ret, img = self.camera.read()
        if not ret or not self.camera.isOpened():
            self.camera.release()
            sys.exit(0)

        img = cv2.GaussianBlur(img, (self.preBlur, self.preBlur), 0)
        img = cv2.resize(img, (self.resizeWidth, self.resizeHeight))
        img = cv2.GaussianBlur(img, (self.postBlur, self.postBlur), 0)
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    def destroy(self):
        self.camera.release()