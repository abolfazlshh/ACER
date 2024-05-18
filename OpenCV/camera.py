import cv2
import numpy as np
import csv
import time

with open('ball_position.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "X", "Y"])

def track_ball(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_range = np.array([25, 100, 100])
    upper_range = np.array([35, 255, 255])

    mask = cv2.inRange(hsv, lower_range, upper_range)

    M = cv2.moments(mask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    return cX, cY

cap = cv2.VideoCapture('Hello.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret == True:
        cX, cY = track_ball(frame)

        cv2.rectangle(frame, (cX, cY), (cX + 20, cY + 20), (0, 255, 0), 2)

        with open('ball_position.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.time(), cX, cY])

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()

cv2.destroyAllWindows()
