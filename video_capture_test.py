if __name__ == "__main__":
    # For testing if video capture works on the raspberry pi
    import numpy as np
    import cv2

    # Initialize the webcam for Hand Gesture Recognition Python project
    cap = cv2.VideoCapture(0)
    try:
        i = 0
        gathered_img = np.zeros((16, 3, 240, 320))
        pred_label = 0
        while True:
            # Read each frame from the webcam
            _, frame = cap.read()
            x, y, c = frame.shape
            print("Frame: ", frame.shape)
            # mp_image = mp.Image(
            #     image_format=mp.ImageFormat.SRGB, data=frame)
            # frame_timestamp_ms = int(time() * 1000)
            # recognizer.recognize_async(mp_image, frame_timestamp_ms)
            # cv2.imshow("Output", frame)

            # if cv2.waitKey(1) == ord('q'):
            #     break
            i += 1
    finally:
        # release the webcam and destroy all active windows
        print("Cleaning up...")
        cap.release()
        cv2.destroyAllWindows()
