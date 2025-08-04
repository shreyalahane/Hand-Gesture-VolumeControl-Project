import cv2
import mediapipe as mp
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time

# Setup webcam
webcam = cv2.VideoCapture(0)

# Mediapipe hand detection
my_hands = mp.solutions.hands.Hands(min_detection_confidence=0.7)
draw_utils = mp.solutions.drawing_utils

# Volume control setup using Pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]  # (-63.5, 0.0)

prev_action_time = 0
delay = 0.5  # seconds

while True:
    ret, img = webcam.read()
    if not ret:
        break
    img = cv2.flip(img, 1)
    frame_height, frame_width, _ = img.shape
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = my_hands.process(rgb_img)
    hands = result.multi_hand_landmarks

    x1 = y1 = x2 = y2 = None

    if hands:
        for hand in hands:
            draw_utils.draw_landmarks(img, hand)
            landmarks = hand.landmark
            for id, lm in enumerate(landmarks):
                x = int(lm.x * frame_width)
                y = int(lm.y * frame_height)

                if id == 8:
                    x1, y1 = x, y
                    cv2.circle(img, (x1, y1), 8, (0, 255, 0), cv2.FILLED)
                if id == 4:
                    x2, y2 = x, y
                    cv2.circle(img, (x2, y2), 8, (0, 0, 255), cv2.FILLED)

        if x1 is not None and x2 is not None:
            length = hypot(x2 - x1, y2 - y1)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # Map distance to volume range
            vol = np.interp(length, [30, 200], [volMin, volMax])
            vol_bar = np.interp(length, [30, 200], [400, 150])
            vol_per = np.interp(length, [30, 200], [0, 100])

            volume.SetMasterVolumeLevel(vol, None)

            # Draw volume bar
            cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 3)
            cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, f'{int(vol_per)} %', (40, 430), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 3)

    cv2.imshow("Volume Control", img)

    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
