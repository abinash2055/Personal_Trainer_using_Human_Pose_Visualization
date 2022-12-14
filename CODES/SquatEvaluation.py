#import packages
from cv2 import WINDOW_NORMAL
import numpy as np
import cv2
import time
import EstimatePoseModule as epm

#read video
cap = cv2.VideoCapture(0)

detector = epm.poseDetector()

previous_time = 0
right_count = 0
wrong_count = 0
dir = 0

while True:

    success, img = cap.read()
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:

        if lmList[26][3] < lmList[25][3]:
            right_knee_angle = detector.findAngle(img, 24, 26, 28, 25, 25)
            right_knee_percentage = np.interp(right_knee_angle, (180, 250), (0, 100))

            if right_knee_percentage == 0:  

                if dir == 0:
                    right_count += 0.5
                    dir = 1

            if right_knee_percentage == 100:

                if dir == 1:
                    right_count += 0.5
                    dir = 0
        else:

            left_knee_angle = detector.findAngle(img, 23, 25, 27, 25, 25)
            left_knee_percentage = np.interp(left_knee_angle, (180, 110), (0, 100))

            if left_knee_percentage == 0:

                if dir == 0:
                    right_count += 0.5
                    dir = 1

            if left_knee_percentage == 100:

                if dir == 1:
                    right_count += 0.5
                    dir = 0 

    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    cv2.putText(img, f'Right: {(int(right_count))}', (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.putText(img, f'Wrong: {(int(wrong_count))}', (70, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    cv2.namedWindow("Squat Evaluation", WINDOW_NORMAL)
    cv2.imshow("Squat Evaluation", img)
    
    cv2.waitKey(1)