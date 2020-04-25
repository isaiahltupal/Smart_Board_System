"""
Author: Ding Bayeta and Isaiah Tupal

This is the main python fail and its task is to manage the functions and processes.

"""
from math import floor
import cv2
import numpy as np

#global variables
mode = "Draw"
tracked_colors = [[48,98,93,90,255,180]]


def none(x):
    pass


def detect_palm_yolo(command_frame):
     command_frame_gray = cv2.cvtColor(command_frame, cv2.COLOR_BGR2GRAY)


def detect_palm(command_frame):
    palm_cascade = cv2.CascadeClassifier("../resources/haarcascades/palm.xml")
    command_frame_gray = cv2.cvtColor(command_frame, cv2.COLOR_BGR2GRAY)

    palm_square = palm_cascade.detectMultiScale(command_frame_gray,1.1,4)
    for (x,y,w,h) in palm_square:
        cv2.rectangle(command_frame, (int(x), int(y)),(int(x+w), int(y+h)), (255, 0, 255), 3)


# processes the frame of the file
def process_frame(frame):
    computed_value = floor(len(frame)*.25)
    command_frame = frame[0:len(frame),0:computed_value]
    detect_palm(command_frame)
    cv2.imshow("command frame", command_frame)


def show_hue(frame):
    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

  # h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
   # s_min = cv2.getTrackbarPos("Sat Min","TrackBars")
   # v_min = cv2.getTrackbarPos("Val Min","TrackBars")
   # h_max = cv2.getTrackbarPos("Hue Max","TrackBars")
   # s_max = cv2.getTrackbarPos("Sat Max","TrackBars")
   # v_max = cv2.getTrackbarPos("Val Max","TrackBars")

    lower = np.array([48,98,93])
    upper = np.array([90,255,180])
    mask = cv2.inRange(frame_hsv,lower,upper)

    frame_result = cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow("mask",mask)
    cv2.imshow("Color",frame_result)
    computed_points = 0
    computed_points2 = 0
    locations = []
    locations = cv2.findNonZero(mask)
    x=0
    try:
        for point in locations:
            for point1 in point:
                computed_points = point1[0]+computed_points
                computed_points2 = point1[1]+computed_points2
                x=x+1
        computed_points=computed_points/x
        computed_points2 =computed_points2/x
        print(computed_points)
        cv2.rectangle(frame, (0, 0), (int(computed_points),  int(computed_points2)), (255, 0, 255), 3)
    except:
        print("oop")



# contains the main loop of the program
def main():
    video = cv2.VideoCapture(0)
    # create trackbars for color change
    cv2.namedWindow("TrackBars")
    cv2.createTrackbar('Hue Min','TrackBars',0,179,none)
    cv2.createTrackbar('Hue Max','TrackBars',179,179,none)
    cv2.createTrackbar('Sat Min','TrackBars',0,255,none)
    cv2.createTrackbar('Sat Max','TrackBars',255,255,none)
    cv2.createTrackbar('Val Min','TrackBars',0,255,none)
    cv2.createTrackbar('Val Max','TrackBars',255,255,none)

    while True:
        alert, frame = video.read()
        computed_points = floor(len(frame[0])*.25)
        #process_frame(frame)
        #cv2.rectangle(frame, (0, 0), (computed_points, len(frame)), (255, 0, 255), 3)


        show_hue(frame)
        cv2.imshow("Video Capture", frame)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            break
        cv2.waitKey(50)


if __name__ == '__main__':
    main()
