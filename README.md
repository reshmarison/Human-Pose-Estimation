# HUMAN POSE ESTIMATION
## Description
The Human Pose Estimator model detects humans and their poses in a given image or video.The model first detects the humans in the input video and then identifies the body parts, including nose, neck, eyes, shoulders elbows, wrists, hips, knees, and ankles. Each pair of associated body parts is connected by a pose line. The pose lines are assembled into full body poses for each of the humans detected in the image. Here we can also use our webcam for pose estimation. The model will predict a sudden fall and are immediately alerted by a push notification. Also a body part can be highlighted in our project.

## Installation
Here I used PyCharm for doing my pose estimation project. If you don't have it already, install PyCharm Community 2021.1.1, then follow the instructions.
* Open Pycharm and select new project. Then name it as Pose Estimation Project.
* Now install the recquired packages such as opencv, mediapipe, imutils, win10toast from File -> Settings -> Python Interpreter.
* Create a new python file in our project and name it as Pose Module.
* Also we want to download some videos for estimation.Then make a folder, pose videos in our project.

## Usage
A single pose or multiple poses can be estimated from an image or video. Each methodology has it own algorithm and set of parameters.

All keypoints are indexed by part id. The parts and their ids are:

| Id | Part |                               
|----|----|
|0.   |nose|                                              
|1.| left_eye_inner|
|2.| left_eye|
|3. |left_eye_outer|
|4.| right_eye_inner|
|5.| right_eye|
|6. |right_eye_outer|
|7.| left_ear|
|8.| right_ear|
|9.| mouth_left|
|10.| mouth_righ
|11.| left_shoulder|
|12.| right_shoulder|
|13.| left_elbow|
|14.| right_elbow|
|15.| left_wrist|
|16. |right_wrist|
|17.|left pinky|
|18.|right pinky|
|19.|left_index|
|20.|right_index|
|21.|left_thumb|
|22.|right_thumb|
|23.|left_hip|
|24.|right_hip|
|25.|left_knee|
|26.|right_knee|
|27.|left_ankle|
|28.|right_ankle|
|29.|left_heel|
|30.|right_heel|
|31.|left_foot_index|
|32.|right_foot_index|

![2-Figure3-1.png](https://d3i71xaburhd42.cloudfront.net/c9bcea08fb81c041ed6d2b7576d8f0e47c1c850f/2-Figure3-1.png)

## Pose Module 
The model first detects the humans in the input video and then identifies the body parts, including nose, neck, eyes, shoulders elbows, wrists, hips, knees, and ankles. Each pair of associated body parts is connected by a pose line. The pose lines are assembled into full body poses for each of the human detected in the video. Here we also detect the landmarks of corresponding body parts with Id. For pose estimation, here we are using mediapipe library.

![Image2.gif](https://1.bp.blogspot.com/-3y9qZTiQ-Xg/XzVsslu98RI/AAAAAAAAGXg/hpkLt16_qmoeqtdW1NBlryODgA-6Wq-RACLcBGAsYHQ/s427/Image2.gif)



    import cv2
    import mediapipe as mp
    import imutils
    import time


    class poseDetector():

        def __init__(self, mode=False, upBody=False, smooth=True,
                      detectionCon=0.5, trackCon=0.5):

            self.mode = mode
            self.upBody = upBody
            self.smooth = smooth
            self.detectionCon =  detectionCon
            self.trackCon = trackCon
            self.mpDraw = mp.solutions.drawing_utils
            self.mpPose = mp.solutions.pose
            self.pose = self.mpPose.Pose(self.mode, self.upBody, 
                          self.smooth, self.detectionCon, self.trackCon)

        def findPose(self, img, draw=True):
            imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.results = self.pose.process(imgRGB)
            if self.results.pose_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,
                                            self.mpPose.POSE_CONNECTIONS)

            return img

        def  getPosition(self, img, draw=True):
            lmList = []
            if self.results.pose_landmarks:
               for id, lm in enumerate(self.results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    #print(id, lm)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx,cy), 5, (255, 0, 0), cv2.FILLED)
            return lmList
    def main():
        cap = cv2.VideoCapture('posevideos/2.mp4')
        pTime = 0
        detector = poseDetector()
        while True:
            success, img = cap.read()
            img = detector.findPose(img)
            lmList = detector.getPosition(img)
            print(lmList)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (78, 50),
                            cv2FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
            img = imutils.resize(img, 500)
            cv2.imshow("Image", img)
            cv2.waitKey(10)
    if __name__ == "__main__":
        main()



The output consists of landmarks of each key points in the form of (Id, cx, cy), where cx and cy is defined in the input. Here the first function is used to find the pose and the scond function is used to find the position. Atlast the third function is used to show the output video.


## To Find Pose
Here we can highlight a specified body part such as right hand elbow, right knee etc. Only the landmarks of  that specified part is detected with the Id. Also all other key points will show and that are connected by pose line.



    import cv2
    import time
    import PoseModule as pm
    import imutils


    cap = cv2.VideoCapture('posevideos/1.mp4')
    pTime = 0
    detector =pm.poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img, draw=False)
        if len(lmList) !=0:
            print(lmList[12])
            cv2.circle(img,(lmList[12][1],lmList[12][2]),
                         15,(0, 0,255),cv2.FILLED)


        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (78, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                           (255, 0, 0), 3)
        img = imutils.resize(img, 500)

        cv2.imshow("Image", img)

        cv2.waitKey(10)


         
         
Here we import pose module as pm and we only highlight the landmark  of 12th key position i.e right elbow.



## Webcam Pose
The model first detects the humans in the webcam  and then identifies the body parts, including nose, neck, eyes, shoulders elbows, wrists, hips, knees, and ankles.All key points will be detected. Each pair of associated body parts is connected by a pose line. Here we also detect the landmarks of corresponding body parts with Id.

    import cv2
    import time
    import PoseModule as pm
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector =pm.poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        print(lmList)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (78, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                          (255, 0, 0), 3)


        cv2.imshow("Webcam", img)

        cv2.waitKey(10)


The output consists of landmarks of each key points in the form of (Id, cx, cy), where cx and cy is defined in the input.

## Fall Detection and Alert

The main aim of this part is to detect the sudden fall of human in the video and produce  alert. The model detects the human in the video and all keypoints will be marked. Also each pair of associated body parts is connected by a pose line. The landmarks of each part will be detected. This part will predict the changes in postures  and are immediately alerted by a push notification.

![https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLzk00ctDnaUTNVtA8kkFMm7QH_y6_0YU-8P4vXoFTLUILllUu6z7yyRQnm0tnZUFLgHc&usqp=CAU](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLzk00ctDnaUTNVtA8kkFMm7QH_y6_0YU-8P4vXoFTLUILllUu6z7yyRQnm0tnZUFLgHc&usqp=CAU)



    import cv2
    import time
    import PoseModule as pm
    import imutils
    from win10toast import ToastNotifier

    cap = cv2.VideoCapture('posevideos/3.mp4')
    pTime = 0
    detector = pm.poseDetector()
    fgbg = cv2.createBackgroundSubtractorMOG2()
    j=0
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        print(lmList)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (78, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 0), 3)
        img = imutils.resize(img, 500)
        try:

            fgmask = fgbg.apply(img)

        # Find contours
            contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE,
                             cv2.CHAIN_APPROX_SIMPLE)

            if contours:

            # List to hold all areas
                areas = []

                for contour in contours:
                    ar = cv2.contourArea(contour)
                    areas.append(ar)

                max_area = max(areas, default=0)
                max_area_index = areas.index(max_area)
                cnt = contours[max_area_index]
                M = cv2.moments(cnt)
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 
                                      3,   maxLevel=0)

                if h < w:
                    j += 1

                if j > 10:
                    cv2.rectangle(img, (x, y), (x + w, y + h), 
                                    (0, 0, 255),  2)
                    hr=ToastNotifier()
                    hr.show_toast("Alert","Fall detected")
                if h > w:
                    j = 0
                    cv2.rectangle(img, (x, y), (x + w, y + h), 
                                     (0, 255, 0), 2)




                img = imutils.resize(img, 500)
                cv2.imshow('Image', img)

                if cv2.waitKey(10) == 0:
                    break
        except Exception as e:
            break

At first, the boundary of human is in green colour. When the human falls, the boundary values changes and it turns into red colour. Also alert message will appear as fall detected. 