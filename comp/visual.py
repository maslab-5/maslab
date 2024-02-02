import numpy as np
import cv2

class Visual:
    def __init__(self, camera, offsetX, green_mask, red_mask):
        self.camera = camera
        self.cameraMiddleX = camera.resizeWidth/2+offsetX
        self.colorFilters = [green_mask, red_mask]
        self.total_mask = camera.resizeWidth*camera.resizeHeight*2.56

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

    def getMedianX(self, bottomRed):
        mask = self.applyFilter(self.camera.getHSVImage(), self.colorFilters[bottomRed])
        coords = np.column_stack(np.where(mask))
 
        return np.median(coords[:, 1]) - self.cameraMiddleX
    
    def getPercent(self, topRed):
        mask = self.applyFilter(self.camera.getHSVImage(), self.colorFilters[topRed])
        return np.sum(mask)/self.total_mask

    def getAngle(self):
        return 0