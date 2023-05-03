import time


def detect_motion(fgmask, prev_fgmask, motion_detected, motion_start_time, motion_stop_time, min_contour_area=500, counter=0):
    # Apply morphological opening to remove noise
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN,
                              np.ones((3, 3), np.uint8))
    # fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)

    # Check if motion is detected -> diff between frames is > frameDiffThreshold
    frameDelta = cv2.absdiff(fgmask, prev_fgmask)
    frameDelta = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # Find the largest contour
    # Find the contours in the binary image
    contours, _ = cv2.findContours(
        frameDelta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = None
    largest_contour_area = 0
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > min_contour_area and contour_area > largest_contour_area:
            largest_contour = contour
            largest_contour_area = contour_area

    print("largest contour area: ", largest_contour_area)
    # If motion is detected
    FRAME_DELTA_THRESH = 10000
    if largest_contour is not None and largest_contour_area > FRAME_DELTA_THRESH:
        # event_id = 1
        # Draw a bounding box around the largest contour
        (_, _, w, h) = cv2.boundingRect(largest_contour)
        # If motion was not detected previously, set the motion start time
        if not motion_detected:
            motion_detected = True
            motion_start_time = time.time()

        # Update motion stop time to current time
        motion_stop_time = time.time()

        return motion_detected, motion_start_time, motion_stop_time
    # If no motion is detected
    else:
        # If motion was detected previously and it has been more than 3 seconds, reset the motion detected flag
        timeDiff = time.time() - motion_start_time
        # print("time difference: ", timeDiff)
        resetToDefault = motion_detected and (timeDiff) > 1
        if resetToDefault:
            # print("Resetting to default...")
            motion_detected = False
            motion_start_time = time.time()
        print("No motion detected")

    return motion_detected, motion_start_time, motion_stop_time


if __name__ == "__main__":
    import cv2
    import numpy as np
    import torch
    from ml_scripts.infer import *
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
    motion_start_time = 0
    motion_stop_time = 0
    input_dim = 112
    num_frame_collect = 16
    try:
        i = 0
        gathered_img = np.zeros((num_frame_collect, 3, input_dim, input_dim))
        pred_label = 0
        # prev_fg_mask = None
        while True:
            # Read each frame from the webcam
            _, frame = cap.read()
            # fgmask = fgbg.apply(frame)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # _, fgmask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

            reshaped, frame = preprocess_mobilenetv2_from_cv2(
                frame, reshape_size=(input_dim, input_dim))
            gathered_img[i % num_frame_collect] = reshaped
            # if i != 0 and i % 2 == 0:
            #     motion_detected, motion_start_time, motion_stop_time = detect_motion(fgmask, prev_fg_mask, motion_detected,
            #                                                                          motion_start_time=motion_start_time,
            #                                                                          motion_stop_time=motion_stop_time,
            #                                                                          counter=i)
            if i != 0 and i % num_frame_collect == 0:
                # if motion_detected:
                # print("Motion Detected: ", motion_detected)
                input_tensor = preprocess_mobilenetv2_queued(gathered_img)
                first_time = time.time()
                pred = model(input_tensor)
                after_pred_time = time.time()
                print("Prediction time: ", after_pred_time - first_time)
                pred_label = int(torch.argmax(pred))
                gathered_img = np.zeros(
                    (num_frame_collect, 3, input_dim, input_dim))

                cv2.putText(frame, JESTER_LABELS[pred_label], (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2, cv2.LINE_AA)

            # show the prediction on the frame
            cv2.putText(frame, JESTER_LABELS[pred_label], (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("Output", frame)
            # cv2.imshow("Output", fgmask)
            # prev_fg_mask = fgmask

            if cv2.waitKey(1) == ord('q'):
                break
            i += 1
            time.sleep(0.05)
    finally:
        # release the webcam and destroy all active windows
        print("Cleaning up...")
        cap.release()
        cv2.destroyAllWindows()
