"""
Author: Ding Bayeta and Isaiah Tupal

This is the main python fail and its task is to manage the functions and processes.

"""
from math import floor
import cv2


def main():
    video = cv2.VideoCapture(0)
    while True:
        alert,frame = video.read()
        computedPoints =floor(len(frame)*.25)

        cv2.rectangle(frame,(0,0),(computedPoints,len(frame)),10,3)
        cv2.imshow("Video Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break



if __name__ == '__main__':
    main()
