import cv2
import sys

class Camera:

    def __init__(self, vid_index, resizeWidth, resizeHeight, preBlur, postBlur):
        self.camera = cv2.VideoCapture(vid_index, cv2.CAP_DSHOW)
        self.resizeWidth = resizeWidth
        self.resizeHeight = resizeHeight
        self.preBlur = preBlur
        self.postBlur = postBlur

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