#!.../venv/lib/scripts python
"""
This is the main python fail and its task is to manage the functions and processes.
"""
import cv2
import numpy as np


def none(x):
    pass


"""
    Given a point from the get point function and the canvas, return the canvas with the newly written thing
    This version of the function will write a 
"""


def draw_on_canvas_point(canvas, black_canvas, point, erase_mode):

    if not erase_mode:
        cv2.circle(canvas, (point[0],point[1]), 4, (166, 0, 163), cv2.FILLED)
    else:
        cv2.circle(black_canvas, (point[0], point[1]), 10, (0, 0, 0), cv2.FILLED)
    return black_canvas, canvas


def draw_on_canvas(canvas, erase_canvas, point, previous_point, erase_mode):

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
        black_canvas, canvas = draw_on_canvas_point(canvas, erase_canvas,  point, erase_mode)
    else:
        point1 = (point[0], point[1])
        point2 = (previous_point[0], previous_point[1])
        if not erase_mode:
            canvas = cv2.line(canvas, point1, point2, (166, 0, 163), 4)
        else:
            erase_canvas = cv2.line(erase_canvas, point1, point2, (166, 0, 163), 10)
    return erase_canvas, canvas


def get_final_canvas(canvas_frame, erase_canvas):
    erase_canvas = cv2.bitwise_and(canvas_frame, erase_canvas)
    canvas_final = cv2.bitwise_xor(canvas_frame, erase_canvas)
    return canvas_final


def display_frame_with_overlay(canvas_frame, erase_canvas, video_frame):
    """
    Displays the output frame ( drawing on top of the  )
    :param canvas_frame:
    :param erase_canvas:
    :param video_frame:
    :return:
    """

    canvas_final = get_final_canvas(canvas_frame, erase_canvas)
    cv2.addWeighted(canvas_final, 1.0, video_frame, .4, .5, video_frame)

    cv2.putText(video_frame, "[W]WRITE [E]ERASE [Q]Quit [S]Save canvas as image", (75, 65), cv2.FONT_HERSHEY_SIMPLEX,
                0.4, (200, 200, 200), 1)
    cv2.putText(video_frame, "[F] Clear all [R]Start recording [T]Stop recording", (75, 85), cv2.FONT_HERSHEY_SIMPLEX,
                0.4, (200, 200, 200), 1)
    cv2.imshow("Video",video_frame)
    return canvas_final

"""
    gets the coordinates of the object being tracked
"""


def get_pen_point(mask,point):
    try:
        mask_blur = cv2.GaussianBlur(mask, (7, 7), 1)
        mask_canny = cv2.Canny(mask_blur,50, 50)
        contours, h = cv2.findContours(mask_canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        contour = contours[0]


        if cv2.contourArea(contour) > 5:
            perimeter = cv2.arcLength(contour, True)
            approx_poly = cv2.approxPolyDP(contour,0.02*perimeter,True)
            x, y, w, h = cv2.boundingRect(approx_poly)
            point1 = (x, y)
            point2 =(int(x+w), int(y+h))
            cv2.rectangle(mask, point1, point2, (255, 0, 255), 10)
            return [int(x+w/2), int(y+h/2)]
        else:
            return point
    except IndexError:
        return [-1,-1]


def get_settings():

    f = open("../resources/variables.txt", "r")
    lwr_string = f.readline()
    upr_string = f.readline()
    f.close()
    lower = list(map(int, lwr_string.split()))
    upper = list(map(int, upr_string.split()))
    print(lower, upper)
      #  lower = [48, 98, 93]list(map(int, test_list))
      #  upper = [90, 255, 180]
    return lower, upper


def get_mask(frame, l, u):
    """
    Returns the mask given the current frame and the
    settings to isolate a color
    :param frame:
    :param l:
    :param u:
    :return:
    """
    lower = np.array(l)
    upper = np.array(u)

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv, lower, upper)
    cv2.imshow("mask", mask)
    return mask


def display_canvas_with_bg(canvas):


    bg = np.zeros([len(canvas), len(canvas[0]), 3], dtype=np.uint8)
    bg.fill(255)
    cv2.cvtColor(bg, cv2.COLOR_BGR2HLS_FULL)

    bg_only_mark = cv2.bitwise_and(canvas, bg)
    bg_real = cv2.bitwise_xor(bg, bg_only_mark)
    cv2.imshow("Display", bg_real)
    return bg_real


def save_canvas(canvas_bg):
    """
    save the canvas to a file
    :param canvas_frame:
    :param erase_canvas:
    :return:
    """
    cv2.imwrite("drawing.jpg",canvas_bg)


def main():

    """
        Initialize video object, first frame, and canvas
    """
    video = cv2.VideoCapture(0)
    alert, frame = video.read()  # initial read to get dimensions
    canvas = (np.zeros((len(frame), len(frame[0]), 4), dtype=np.uint8))
    black_canvas = (np.zeros((len(frame), len(frame[0]), 4), dtype=np.uint8))
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2HLS_FULL)
    black_canvas = cv2.cvtColor(black_canvas, cv2.COLOR_BGR2HLS_FULL)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('recording.avi', fourcc, 20.0, (640,480))

    previous_point = [-1, -1]
    erase_mode = False
    record_mode = False
    lower, upper = get_settings()

    while True:
        #looping statement
        """
            General function of the loop:
            Read frame -> isolate object -> write on the position of the object
        """
        alert, frame = video.read()
        frame = cv2.flip(frame,1)
        mask = get_mask(frame, lower, upper)
        point = get_pen_point(mask, previous_point)
        erase_canvas, canvas = draw_on_canvas(canvas, black_canvas , point, previous_point, erase_mode) #returns the canvas
        canvas = display_frame_with_overlay(canvas, black_canvas, frame)
        canvas_with_bg = display_canvas_with_bg(canvas)

        if(record_mode):
            out.write(frame)

        # Set point to previous_point before overwriting it in the next loop
        previous_point = point
        k = cv2.waitKey(10)

        # Activate erase mode
        if k & 0xFF == ord('e'):
            erase_mode = True
        # Clear canvas
        if k & 0xFF == ord('f'):
            canvas = (np.zeros((len(frame), len(frame[0]), 4), dtype=np.uint8))
            black_canvas = (np.zeros((len(frame), len(frame[0]), 4), dtype=np.uint8))
            canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2HLS_FULL)
            black_canvas = cv2.cvtColor(black_canvas, cv2.COLOR_BGR2HLS_FULL)
        # Activate write mode
        elif k & 0xFF == ord('w'):
            erase_mode = False
            black_canvas = (np.zeros((len(frame), len(frame[0]), 4), dtype=np.uint8))
            black_canvas = cv2.cvtColor(black_canvas, cv2.COLOR_BGR2HLS_FULL)
        # Save current frame to project folder
        elif k & 0xFF == ord('s'):
            save_canvas(canvas_with_bg)
        # Quits program
        elif k & 0xFF == ord('q'):
            break
        # Starts recording
        elif k & 0xFF == ord('r'):
            record_mode = True
        # Stops recording, saving video output
        elif k & 0xFF == ord('t'):
            record_mode = False
            if (out.isOpened()): out.release()

if __name__ == '__main__':
    main()