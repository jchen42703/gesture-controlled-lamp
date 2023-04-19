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

    input_dim = 112
    try:
        i = 0
        gathered_img = np.zeros((16, 3, input_dim, input_dim))
        pred_label = 0
        while True:
            # Read each frame from the webcam
            _, frame = cap.read()
            reshaped, frame = preprocess_mobilenetv2_from_cv2(
                frame, reshape_size=(input_dim, input_dim))
            gathered_img[i % 16] = reshaped
            if i != 0 and i % 16 == 0:
                input_tensor = preprocess_mobilenetv2_queued(gathered_img)
                pred = model(input_tensor)
                pred_label = int(torch.argmax(pred))
                gathered_img = np.zeros((16, 3, input_dim, input_dim))
                # show the prediction on the frame
            cv2.putText(frame, JESTER_LABELS[pred_label], (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("Output", frame)

            if cv2.waitKey(1) == ord('q'):
                break
            i += 1
    finally:
        # release the webcam and destroy all active windows
        print("Cleaning up...")
        cap.release()
        cv2.destroyAllWindows()
