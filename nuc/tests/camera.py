import cv2
import sys
import numpy as np

class Camera:

    def __init__(self, vid_index, resize, preBlur, postBlur, pFilter, sFilter):
        self.camera = cv2.VideoCapture(vid_index, cv2.CAP_DSHOW)
        self.resize = resize
        self.preBlur = preBlur
        self.postBlur = postBlur
        self.total_mask = resize[0]*resize[1]*2.56
        self.primaryFilter = pFilter
        self.secondaryFilter = sFilter

    def getImage(self):
        ret, img = self.camera.read()
        if not ret or not self.camera.isOpened():
            self.camera.release()
            sys.exit(0)

        img = cv2.GaussianBlur(img, (self.preBlur, self.preBlur), 0)
        img = cv2.resize(img, (self.resize[0], self.resize[1]))
        img = cv2.GaussianBlur(img, (self.postBlur, self.postBlur), 0)
        return img

    def toHSV(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def applyFilter(self, hsv, filter):
        if filter[0][0] < 0:
            filter1 = [filter[0].copy(), filter[1].copy()]
            filter2 = [filter[0].copy(), filter[1].copy()]

            filter1[0][0] = 0
            filter2[0][0] += 180
            filter2[1][0] = 180

            mask1 = cv2.inRange(hsv, np.array(filter1[0]), np.array(filter1[1]))
            mask2 = cv2.inRange(hsv, np.array(filter2[0]), np.array(filter2[1]))
            return cv2.bitwise_or(mask1, mask2)
        else:
            return cv2.inRange(hsv, np.array(filter[0]), np.array(filter[1]))
    
    def getPercentFilter(self, filter):
        mask = self.applyFilter(self.toHSV(self.getImage()), filter)
        return np.sum(mask)/self.total_mask
    
    def getAngle(self):
        return 0
    
    def destroy(self):
        self.camera.release()