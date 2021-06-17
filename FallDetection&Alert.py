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
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

            cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 3, maxLevel=0)

            if h < w:
                j += 1

            if j > 10:

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                hr=ToastNotifier()
                hr.show_toast("Alert","Fall detected")
            if h > w:
                j = 0
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)




            img = imutils.resize(img, 500)
            cv2.imshow('Image', img)

            if cv2.waitKey(10) == 0:
                break
    except Exception as e:
        break

