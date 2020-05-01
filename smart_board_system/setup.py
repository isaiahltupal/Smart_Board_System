"""

    This is to set up the variables for the program to track the object
    Author: Isaiah and Ding Bayeta

"""
import cv2
import numpy as np


def none(x):
    """
        does nothing
    """
    pass


def initialize():
    """
    creates the trackbars
    :return: video object
    """

    cv2.namedWindow("SETUP")
    cv2.createTrackbar("HUE MIN", "SETUP", 0, 255, none)
    cv2.createTrackbar("HUE MAX", "SETUP", 255, 255, none)
    cv2.createTrackbar("SAT MIN", "SETUP", 0, 255, none)
    cv2.createTrackbar("SAT MAX", "SETUP", 255, 255, none)
    cv2.createTrackbar("VAL MIN", "SETUP", 0, 255, none)
    cv2.createTrackbar("VAL MAX", "SETUP", 255, 255, none)
    video = cv2.VideoCapture(0)
    return video


def get_mask(video_frame):
    """
       img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)
    :param video_frame:
    :return:
    """

    frame_hsv = cv2.cvtColor(video_frame, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("HUE MIN", "SETUP")
    h_max = cv2.getTrackbarPos("HUE MAX", "SETUP")
    s_min = cv2.getTrackbarPos("SAT MIN", "SETUP")
    s_max = cv2.getTrackbarPos("SAT MAX", "SETUP")
    v_min = cv2.getTrackbarPos("VAL MIN", "SETUP")
    v_max = cv2.getTrackbarPos("VAL MAX", "SETUP")
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask_frame = cv2.inRange(frame_hsv, lower, upper)
    color_frame = cv2.bitwise_and(video_frame, video_frame, mask=mask_frame)
    cv2.imshow("COLOR", color_frame)



def main():
    video=initialize()
    while True:
        alert, video_frame = video.read()
        get_mask(video_frame)
        k = cv2.waitKey(10)
        if k & 0xFF == ord('p'):
            break


if __name__ == "__main__":
    main()