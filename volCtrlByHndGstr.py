'''
Project name: Volume Control By Hand Gesture
Starting Date: 04 April 2023
Finishing Date: 06 April 2023
Author name: Thakar Atri Kamleshkumar
'''

import cv2 as cv
import mediapipe as mp
import numpy as np
import keyboard
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

frame = cv.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(False,1,1,0.7,0.5)
mpDraw = mp.solutions.drawing_utils

px1,py1,px2,py2=0,0,0,0
mx1, my1 =0,0
length = 0
volBar=400
volPer=0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while True:
    success, img = frame.read()

    cv.putText(img,f"Press 'S' key to save the volume level",(40,40),cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)
    cv.putText(img,f"Press 'Q' key to exit the code",(40,60),cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)
    cv.rectangle(img,(50,150),(85,400),(255,0,0),3)
    cv.rectangle(img,(400,400),(600,450),(0,0,0),-1)
    cv.putText(img,f"(C) Atri Thaker",(405,430),cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)

    imgRGB= cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 4:
                    cv.circle(img,(cx,cy),15,(0,255,0),-1)
                    px1, py1 = cx, cy
                if id == 8:
                    cv.circle(img,(cx,cy),15,(0,255,0),-1)
                    px2, py2 = cx, cy
        cv.line(img,(px1,py1),(px2,py2),(255,0,0),2)
        length = (((px1-px2)**2)+((py1-py2)**2))**(1/2)
        mx1 = (px1+px2)//2
        my1 = (py1+py2)//2
        cv.circle(img,(mx1,my1),15,(0,0,255),-1)
        
        vol = np.interp(length,[50,200],[minVol,maxVol])
        volBar = np.interp(length,[50,200],[400,150])
        volPer = np.interp(length,[50,200],[0,100])

        if length < 50:
            cv.circle(img,(mx1,my1),15,(0, 255, 255),-1)

    cv.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),-1)
    cv.putText(img,f'{int(volPer)}%',(40,450),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)   
    cv.imshow("webcam", img)

    if keyboard.is_pressed('s'):
        volume.SetMasterVolumeLevel(vol, None)
        setted = volume.GetMasterVolumeLevel()
        showVol = np.interp(setted,[-65.25,0],[0,100])
        print(f"Volume level {int(showVol)} saved")
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

frame.release()
cv.destroyAllWindows()