# import packages
from cv2 import WINDOW_NORMAL
import cv2
import numpy as np
import time
import EstimatePoseModule as epm

cap = cv2.VideoCapture(0)

detector = epm.poseDetector()

previous_time = 0 
count = 0
dir = 0

while True:

    success, img = cap.read()
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:

        if lmList[24][3] < lmList[23][3]:

            right_hip_angle = detector.findAngle(img, 12, 24, 26, -25, -25)
            right_hip_percentage = np.interp(right_hip_angle, (120, 80), (0, 100))

            if right_hip_percentage == 100:

                if dir == 0:
                    count += 0.5
                    dir = 1

            if right_hip_percentage == 0:

                if dir == 1:
                    count += 0.5
                    dir = 0
        else:

            left_hip_angle = detector.findAngle(img, 11, 23, 25, 25, 25)
            left_hip_percentage = np.interp(left_hip_angle, (240, 280), (0, 100))

            if left_hip_percentage == 100:

                if dir == 0:
                    count += 0.5
                    dir = 1

            if left_hip_percentage == 0:

                if dir == 1:
                    count += 0.5
                    dir = 0

    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    cv2.putText(img, f'Situp Count: {(int(count))}', (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.putText(img, str(int(fps)), (600,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    cv2.namedWindow("Situp Evaluation", WINDOW_NORMAL)
    cv2.imshow("Situp Evaluation", img)
    
    cv2.waitKey(1)