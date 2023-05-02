import time


def detect_motion(fgmask, motion_detected, motion_start_time, motion_stop_time, human_w_h_ration=1.25, min_contour_area=500, counter=0):
    event_id = 1
    # Apply morphological opening to remove noise
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN,
                              np.ones((3, 3), np.uint8))
    fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)

    # Find the contours in the binary image
    contours, _ = cv2.findContours(
        fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = None
    largest_contour_area = 0
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > min_contour_area and contour_area > largest_contour_area:
            largest_contour = contour
            largest_contour_area = contour_area

    # If motion is detected
    if largest_contour is not None:
        # event_id = 1
        # Draw a bounding box around the largest contour
        (_, _, w, h) = cv2.boundingRect(largest_contour)
        if h >= human_w_h_ration * w:
            event_id = 2

        # If motion was not detected previously, set the motion start time
        if not motion_detected:
            motion_detected = True
            motion_start_time = time.time()

        # Update motion stop time to current time
        motion_stop_time = time.time()

        return motion_detected, motion_start_time, motion_stop_time, event_id
    # If no motion is detected
    else:
        event_id = 1
        # If motion was detected previously and it has been more than 3 seconds, reset the motion detected flag
        resetToDefault = motion_detected and (
            time.time() - motion_start_time) > 1
        if resetToDefault:
            print("Resetting to default...")
            motion_detected = False
            motion_start_time = time.time()

    return motion_detected, motion_start_time, motion_stop_time, event_id
    # # If motion has not been detected for 5 seconds / if motion stop time has not been updated, exit the loop
    # if time.time() - motion_stop_time > 5:
    #     return motion_detected, motion_start_time, motion_stop_time, event_id


if __name__ == "__main__":
    import cv2
    import numpy as np
    import torch
    from infer import *
    import pathlib
    import os

    cwd = pathlib.Path(__file__).parent.resolve()
    # relative_weights_path = "weights/jester_mobilenetv2_0.7x_RGB_16_best.pth"
    relative_weights_path = "weights/jester_shufflenet_0.5x_G3_RGB_16_best.pth"
    weights_path = os.path.join(cwd, relative_weights_path)
    # model = create_mobilenetv2(pretrained_weights_path=weights_path)
    model = create_shufflenet(weights_path)
    # Initialize the webcam for Hand Gesture Recognition Python project
    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

    # Initialize variables for motion detection
    motion_detected = False
    motion_start_time = None
    motion_stop_time = 0
    input_dim = 112
    try:
        i = 0
        gathered_img = np.zeros((16, 3, input_dim, input_dim))
        pred_label = 0
        while True:
            # Read each frame from the webcam
            _, frame = cap.read()
            fgmask = fgbg.apply(frame)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # _, fgmask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

            reshaped, frame = preprocess_mobilenetv2_from_cv2(
                frame, reshape_size=(input_dim, input_dim))
            gathered_img[i % 16] = reshaped
            if i % 16 == 0:
                # Apply the background subtraction
                motion_detected, motion_start_time, motion_stop_time, event_id = detect_motion(fgmask, motion_detected,
                                                                                               motion_start_time=motion_start_time,
                                                                                               motion_stop_time=motion_stop_time,
                                                                                               counter=i)
                print("event id: ", event_id)
            if i != 0 and i % 16 == 0 and motion_detected:
                input_tensor = preprocess_mobilenetv2_queued(gathered_img)
                pred = model(input_tensor)
                pred_label = int(torch.argmax(pred))
                gathered_img = np.zeros((16, 3, input_dim, input_dim))
            # show the prediction on the frame
            cv2.putText(frame, JESTER_LABELS[pred_label], (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
            # cv2.imshow("Output", frame)
            cv2.imshow("Output", fgmask)

            if cv2.waitKey(1) == ord('q'):
                break
            i += 1
    finally:
        # release the webcam and destroy all active windows
        print("Cleaning up...")
        cap.release()
        cv2.destroyAllWindows()
