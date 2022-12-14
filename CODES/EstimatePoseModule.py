#for image processing 
import cv2
from cv2 import WINDOW_NORMAL

#for pose estimation
import mediapipe as mp  
import time
from pip import main
import math

class poseDetector():

    def __init__(self, mode=False, model_complexity = 1, upBody=False, smooth=True, detectionConfidence=0.5, trackConfidence=0.5):
        self.modelComplex = model_complexity
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence

        self.mpDraw = mp.solutions.drawing_utils

        #Create the object for pose estimation.
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.modelComplex,  self.upBody, self.smooth, self.detectionConfidence, self.trackConfidence)

    def findPose(self, img, draw=True):
        #convert the image from BGR to RGB so that we can give it to the object for pose estimation.
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

        #give the image to the object for pose estimation. 
        self.results = self.pose.process(imgRGB) 

        if self.results.pose_landmarks:

            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []

        if self.results.pose_landmarks:

            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy, cz = int(lm.x*w), int(lm.y*h), lm.z
                self.lmList.append([id, cx, cy ,cz])

                if draw:
                    cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)
        return self.lmList
    
    def findAngle(self, img, id1, id2, id3, dx, dy,draw=True):

        #get the landmarks.
        x1, y1 = self.lmList[id1][1], self.lmList[id1][2]
        x2, y2 = self.lmList[id2][1], self.lmList[id2][2]
        x3, y3 = self.lmList[id3][1], self.lmList[id3][2]

        #calculate the angle.
        angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))

        if angle<0:
            angle += 360

        if draw:
            
            cv2.line(img, (x1, y1), (x2, y2), (255,255,255), 3)
            cv2.line(img, (x2, y2), (x3, y3), (255,255,255), 3)
            cv2.circle(img, (x1,y1), 10, (0,0,255), cv2.FILLED)
            cv2.circle(img, (x1,y1), 15, (0,0,255), 2)
            cv2.circle(img, (x2,y2), 10, (0,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (0,0,255), 2)
            cv2.circle(img, (x3,y3), 10, (0,0,255), cv2.FILLED)
            cv2.circle(img, (x3,y3), 15, (0,0,255), 2) 
            cv2.putText(img, str(int(angle)), (x2+dx,y2+dy), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)

        return angle

def main():

    #read video 
    cap = cv2.VideoCapture(0)

    previous_time = 0 
    detector = poseDetector()

    while True:

        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:

            print(lmList[14])
            cv2.circle(img, (lmList[14][1],lmList[14][2]), 15, (0,0,255), cv2.FILLED)

        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time

        cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
        cv2.namedWindow("Pushup Evaluation", WINDOW_NORMAL)
        cv2.imshow("Pushup Evaluation", img)
        cv2.waitKey(1) 

if __name__ == "__main__":
    main()