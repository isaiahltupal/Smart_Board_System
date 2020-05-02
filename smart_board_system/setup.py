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


def update_settings(video_frame):
    """
     Displays and returns current color settings
    :param video_frame:
    :return: upper,lower
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
    return lower,upper


def save_settings(lower,upper):
    """
    saves the settings into a txt file
    :param lower: lower color threshold
    :param upper: upper color threshold
    :return:
    """
    lwr_string,upr_string = "", ""

    for l in lower:
        lwr_string = lwr_string+str(l)+" "

    for u in upper:
        upr_string = upr_string+str(u)+" "

    f = open("../resources/variables.txt", "w")
    f.write(lwr_string)
    f.write("\n")
    f.write(upr_string)
    f.close()



def main():
    video=initialize()
    while True:
        alert, video_frame = video.read()
        lower,upper = update_settings(video_frame)
        k = cv2.waitKey(10)
        if k & 0xFF == ord('p'):
            save_settings(lower, upper)
            break


if __name__ == "__main__":
    main()