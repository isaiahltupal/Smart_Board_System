"""
Author: Ding Bayeta and Isaiah Tupal

This is the main python fail and its task is to manage the functions and processes.

"""

import cv2


def main():
    video = cv2.VideoCapture(0)
    while True:
        success,img = video.read()
        cv2.imshow("Video Capture", img)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break

if __name__ == '__main__':
    main()
