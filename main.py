import cv2
import mediapipe as mp
import time
from directkeys import right_pressed,left_pressed
from directkeys import PressKey, ReleaseKey
#import os
#adb_path = r"C:\Users\shiva\Downloads\platform-tools-latest-windows\platform-tools\adb.exe"



break_key_pressed=left_pressed
accelerato_key_pressed=right_pressed

time.sleep(2.0)
current_key_pressed = set()

cap = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]
with mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)as hands:
    while True:
        keyPressed = False
        break_pressed = False
        accelerator_pressed = False
        key_count = 0
        key_pressed = 0



        ret,img = cap.read()
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        results = hands.process(imgRGB)
        imgRGB.flags.writeable = True
        imgRGB=cv2.cvtColor(imgRGB,cv2.COLOR_RGB2BGR)
        lmList = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:

                for id,lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
        fingers=[]
        if len(lmList)>0:
            if lmList[tipIds[0]][1] >lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2]< lmList[tipIds[id]-2][2] :
                    fingers.append(1)
                else:
                    fingers.append(0)

        total=fingers.count(1)
        if total==0:
            cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "BRAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 0, 0), 5)
            #os.system(f"{adb_path} shell input tap 500 1200")  # Replace (500, 1200) with your brake button coordinates
            PressKey(break_key_pressed)
            break_pressed = True
            current_key_pressed.add(break_key_pressed)
            key_pressed = break_key_pressed
            keyPressed = True
            key_count = key_count + 1
        elif total==5:
            cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "  GAS", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 0, 0), 5)
            #os.system(f"{adb_path} shell input tap 800 1200")  # Replace (800, 1200) with your gas button coordinates

            PressKey(accelerato_key_pressed)
            key_pressed = accelerato_key_pressed
            accelerator_pressed = True
            keyPressed = True
            current_key_pressed.add(accelerato_key_pressed)
            key_count = key_count + 1

        # RELEASE keys if not needed anymore
        if not break_pressed and break_key_pressed in current_key_pressed:
            ReleaseKey(break_key_pressed)
            current_key_pressed.remove(break_key_pressed)

        if not accelerator_pressed and accelerato_key_pressed in current_key_pressed:
            ReleaseKey(accelerato_key_pressed)
            current_key_pressed.remove(accelerato_key_pressed)


        cv2.imshow("Image",img)
        k=cv2.waitKey(1)
        if k==ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
