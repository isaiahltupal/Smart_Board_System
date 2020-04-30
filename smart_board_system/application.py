"""
Author: Ding Bayeta and Isaiah Tupal

This is the main python fail and its task is to manage the functions and processes.

"""
import cv2
import numpy as np


#frames
raw_frame, mask_frame, canvas_bg, canvas_full =[],[],[],[]

#video
video = None



def none(x):
    pass


"""
    Given a point from the get point function and the canvas, return the canvas with the newly written thing
    This version of the function will write a 
"""


def draw_on_canvas_point(canvas, black_canvas, point):

    cv2.circle(canvas, (point[0],point[1]), 4, (166, 0, 163), cv2.FILLED)
    cv2.circle(black_canvas, (point[0], point[1]), 4, (0, 0, 0), cv2.FILLED)
    return black_canvas, canvas


def draw_on_canvas(canvas, black_canvas, point, previous_point):

    """
    :param canvas: canvas layer to write on
    :param point:point for the line
    :param previous_point: previous point for the line
    :return: nothing


    the conditional statement is as follows:
    1st condition: if no point is extracted, skip this loop
    2nd condition: if the previous point is a non point, then this must be the first loop, just draw a circle
    3rd loop: draw a line since both parameters are acceptable points
    """
    if point == [-1, -1]:
        pass
    elif previous_point == [-1, -1]:
        black_canvas, canvas = draw_on_canvas_point(canvas, black_canvas,  point)
    else:
        point1 = (point[0], point[1])
        point2 = (previous_point[0], previous_point[1])
        canvas = cv2.line(canvas, point1, point2, (166, 0, 163), 4)
        black_canvas = cv2.line(black_canvas, point1, point2, (0, 0, 0), 4)
    return black_canvas, canvas


def display_frame_with_overlay(canvas_frame, black_canvas, video_frame):

    canvas_frame = cv2.cvtColor(canvas_frame, cv2.COLOR_BGR2HLS_FULL)
    w = len(canvas_frame[0])
    h = len(canvas_frame)
    for i in range(0, h):
        for j in range(0, w):

            if canvas_frame[i, j].all(0):
                video_frame[i, j] = canvas_frame[i, j]

    #cv2.addWeighted(canvas_frame, 1.0, video_frame, 1.0, 0, video_frame)
    cv2.imshow("Video",video_frame)


"""
    gets the coordinates of the object being tracked
"""


def get_pen_point(mask,point):
    try:
        mask_blur = cv2.GaussianBlur(mask, (7, 7), 1)
        mask_canny = cv2.Canny(mask_blur,50,50)
        contours,h = cv2.findContours(mask_canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        contour = contours[0]

        if cv2.contourArea(contour) > 5:
            perimeter = cv2.arcLength(contour, True)
            approxPoly = cv2.approxPolyDP(contour,0.02*perimeter,True)
            x,y,w,h = cv2.boundingRect(approxPoly)
            #for debugging purpose
            point1 = (x,y)
            point2 =( int(x+w), int(y+h) )
            cv2.rectangle(mask,point1,point2,(255,0,255),10)
            #cv2.imshow("Mask",mask)
            return [ int(x+w/2), int(y+h/2) ]
        else:
            return point

    except:
        return point


def get_mask(frame):

    lower = np.array([48, 98, 93])
    upper = np.array([90,255,180])

    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv,lower,upper)
    return mask


def main():

    """
        Initialize video object, first frame, and canvas
    """
    video = cv2.VideoCapture(0)
    alert, frame = video.read()  # initial read to get dimensions
    canvas = (np.zeros((len(frame), len(frame[0]), 4), dtype=np.uint8))
    black_canvas = (np.zeros((len(frame), len(frame[0]), 4), dtype=np.uint8))
    previous_point = [-1,-1]


    while True:
        #looping statement
        """
            General function of the loop:
            Read frame -> isolate object -> write on the position of the object
        """
        alert, frame = video.read()
        frame = cv2.flip(frame,1)
        mask = get_mask(frame)
        point = get_pen_point(mask, previous_point)
        black_canvas, canvas = draw_on_canvas(canvas, black_canvas , point, previous_point) #returns the canvas
        display_frame_with_overlay(canvas, black_canvas, frame)
        # set point to previous_point before overwriting it in the next loop
        previous_point = point
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break
        cv2.waitKey(1)


main()