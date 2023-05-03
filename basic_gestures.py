import cv2


def get_frame_rate(video: cv2.VideoCapture):
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.

    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print(
            "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else:
        fps = video.get(cv2.CAP_PROP_FPS)
        print(
            "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))


def get_mask_basic(initial_frame, curr_frame, threshold):
    # Check if motion is detected -> diff between frames is > frameDiffThreshold
    frameDelta = cv2.absdiff(initial_frame, curr_frame)
    thresh = cv2.threshold(frameDelta, threshold, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    return thresh, frameDelta


# def get_mask(initial_frame, curr_frame):
#     fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
#     fg_mask = fgbg.apply(curr_frame)
#     return fg_mask


def get_largest_contour_area(initial_frame, curr_frame, threshold) -> bool:
    """Gets the largest contour area of the thresholded object
    """
    # Check if motion is detected -> diff between frames is > frameDiffThreshold
    thresh, _ = get_mask_basic(initial_frame, curr_frame, threshold)

    # Find the largest contour
    # Find the contours in the binary image
    # contours, _ = cv2.findContours(
    #     frameDelta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    largest_contour_area = 0
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        contour_area = cv2.contourArea(c)
        largest_contour_area = max(contour_area, largest_contour_area)
    return largest_contour_area


def detect_motion(initial_frame, curr_frame, threshold=180) -> bool:
    """
    The gesture detection algorithm is as follows:
    1. Register initial frame.
    2. Check the difference between the current frame and initial frame.
    3. Start "recording" after the current frame's object's area exceeds `AREA_THRESHOLD`.
    4. Record the next 16 frames.
        1. If the area decreases over those 16 frames, decrease the brightness.
        2. If the area increases over those 16 frames, increase the brightness.
    5. After 16 frames, re-check the object's size in the frame. If it exceeds `AREA_THRESHOLD`, start recording again and repeat.
    """
    largest_contour_area = get_largest_contour_area(
        initial_frame, curr_frame, threshold)
    print("Largest contour area: ", largest_contour_area)
    START_RECORDING_AREA_THRESH = 700
    return largest_contour_area > START_RECORDING_AREA_THRESH, largest_contour_area


if __name__ == "__main__":
    import cv2
    import numpy as np
    import pathlib
    import time
    import imutils
    from gesture_detector import GestureDetector
    import argparse
    parser = argparse.ArgumentParser(
        prog='gesture-lamp',
        description='Runs gesture controlled lamp',
        epilog='Text at the bottom of help')
    parser.add_argument('video')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-l', '--is-lampi', action='store_true')
    args = parser.parse_args()

    cwd = pathlib.Path(__file__).parent.resolve()
    # video_path_or_idx = "/dev/video2"
    if args.video.isdigit():
        args.video = int(args.video)
    cap = cv2.VideoCapture(args.video)
    detector = GestureDetector(
        abs_diff_thresh=0.05, lampi=args.is_lampi)

    # Initialize variables for motion detection
    motion_detected = False
    motion_start_time = 0
    motion_stop_time = 0
    num_frame_collect = 16
    OPERATIONS = [
        "Do nothing",
        "Increase Brightness",
        "Decrease Brightness",
    ]

    pred_label = 0
    initial_frame_gray = None
    INITIAL_DELTA_MAX = 80
    initial_max = INITIAL_DELTA_MAX
    gesture = OPERATIONS[0]
    try:
        i = 0
        while True:
            # Read each frame from the webcam
            _, frame = cap.read()
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # gray = cv2.GaussianBlur(gray, (21, 21), 0)
            if initial_frame_gray is None:
                initial_frame_gray = gray
                continue

            detected, contour_area = detect_motion(
                initial_frame_gray, gray, initial_max)
            # Record for the next 16 frames and see the changes in motion
            mask, delta = get_mask_basic(initial_frame_gray, gray, initial_max)
            # Set the threshhold
            if initial_max == INITIAL_DELTA_MAX:
                # This needs to be calibrated
                # Sometimes the initial delta.max() is far too low to be good
                # enough
                initial_max = max(delta.max()*1.75, INITIAL_DELTA_MAX-30)

            if detected:
                gesture = detector.detect_gesture_type(
                    mask, contour_area)
                print("Detected motion! Gesture: ", gesture)
            else:
                print("Stopped detecting...")

            if args.debug:
                # show the prediction on the frame
                cv2.putText(frame, detector.get_operation_from_gesture(gesture),
                            (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.imshow("Output", frame)
                cv2.imshow("Gray", gray)
                cv2.imshow("Mask", mask)

                if cv2.waitKey(1) == ord('q'):
                    break
            i += 1
            time.sleep(0.1)
    finally:
        # release the webcam and destroy all active windows
        print("Cleaning up...")
        cap.release()
        cv2.destroyAllWindows()
