if __name__ == "__main__":
    import cv2
    import mediapipe as mp

    from time import time

    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
    VisionRunningMode = mp.tasks.vision.RunningMode

    model_path = '/home/pi/gesture-controlled-lamp/gesture_recognizer.task'
    base_options = BaseOptions(model_asset_path=model_path)

    # Create a gesture recognizer instance with the live stream mode:

    def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        for gesture in result.gestures:
            for pred_cat in gesture:
                print("Gesture: ", pred_cat.category_name)

    options = GestureRecognizerOptions(
        base_options=base_options,
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result)

    # Initialize the webcam for Hand Gesture Recognition Python project
    cap = cv2.VideoCapture(0)

    with GestureRecognizer.create_from_options(options) as recognizer:

        try:
            while True:
                # Read each frame from the webcam
                _, frame = cap.read()
                x, y, c = frame.shape
                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB, data=frame)
                frame_timestamp_ms = int(time() * 1000)
                recognizer.recognize_async(mp_image, frame_timestamp_ms)
        finally:
            # release the webcam and destroy all active windows
            print("Cleaning up...")
            cap.release()
            cv2.destroyAllWindows()
