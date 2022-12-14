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

        if lmList[14][3] < lmList[13][3]:

            right_elbow_angle = detector.findAngle(img, 12, 14, 16, 25, 25)
            right_elbow_percentage = np.interp(right_elbow_angle, (70,130), (0,100))
            right_hip_angle = detector.findAngle(img, 12, 24, 26, 25, 25)   

            if right_elbow_percentage == 100:

                if right_hip_angle >= 160 and right_hip_angle <= 180:

                    if dir == 1:
                        right_count += 0.5
                        dir = 0

                else:

                    if dir == 1:
                        wrong_count += 0.5
                        dir = 0

            if right_elbow_percentage == 0:

                if right_hip_angle >= 160 and right_hip_angle <= 180:

                    if dir == 0:
                        right_count += 0.5
                        dir = 1

                else:

                    if dir == 0:
                        wrong_count += 0.5
                        dir = 1

        else: 

            left_elbow_angle = detector.findAngle(img, 11, 13, 15, 25, 25)
            left_elbow_percentage =  np.interp(left_elbow_angle, (290,230), (0,100))
            left_hip_angle = detector.findAngle(img, 11, 23, 25, 25, 25) 

            if left_elbow_percentage == 100:

                if left_hip_angle >= 180 and left_hip_angle <= 200:

                    if dir == 0:
                        right_count += 0.5
                        dir = 1
                else:

                    if dir == 0:
                        wrong_count += 0.5
                        dir = 1

            if left_elbow_percentage == 0:

                if left_hip_angle >= 180 and left_hip_angle <= 200:

                    if dir == 1:
                        right_count += 0.5
                        dir = 0
                else:

                    if dir == 1:
                        wrong_count += 0.5
                        dir = 0

    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    cv2.putText(img, f'Right: {int(right_count)}', (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.putText(img, f'Wrong: {int(wrong_count)}', (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    cv2.putText(img, str(int(fps)), (600,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.namedWindow("Pushup Evaluation", WINDOW_NORMAL)
    
    cv2.imshow("Pushup Evaluation", img)
    cv2.waitKey(1) 