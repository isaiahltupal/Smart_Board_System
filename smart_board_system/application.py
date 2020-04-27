"""
Author: Ding Bayeta and Isaiah Tupal

This is the main python fail and its task is to manage the functions and processes.

"""
import cv2
import numpy as np


#frames
raw_frame, mask_frame, canvas, canvas_bg, canvas_full =[],[],[],[],[]

#video
video = None

#point
previous_point = [-1,-1]


def none(x):
    pass

def draw_on_canvas(canvas,point):
    none_array = [-1, -1]
    try:
        cv2.circle(canvas, (point[0],point[1]), 4, (255, 0, 255), cv2.FILLED)
        previous_point[0] = point[0]
        previous_point[1] = point[1]
    except:
        print("nopoint")
    return canvas

def get_pen_point(mask):
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
            cv2.imshow("Mask",mask)
            return [ int(x+w/2), int(y+h/2) ]
        else:
            return [-1,-1]
    except:
        return [-1,-1]


def get_mask(frame):

    lower = np.array([48, 98, 93])
    upper = np.array([90,255,180])

    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv,lower,upper)
    return mask



def main():
    video = cv2.VideoCapture(0)
    alert, frame = video.read()  # initial read to get dimensions
    canvas = (np.zeros((len(frame), len(frame[0]), 4), dtype=np.uint8))
    while True:
        alert, frame = video.read()
        frame = cv2.flip(frame,1)
        mask = get_mask(frame)
        point = get_pen_point(mask)
        canvas = draw_on_canvas(canvas, point)
        cv2.imshow("canvas",canvas)
        cv2.imshow("Frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break
        cv2.waitKey(10)


main()