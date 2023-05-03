if __name__ == "__main__":
    import cv2
    import numpy as np
    import torch
    from infer import *
    from config import read_config
    import pathlib
    import os
    import time
    from lamp import lamp_driver

    cwd = pathlib.Path(__file__).parent.resolve()
    # relative_weights_path = "weights/jester_mobilenetv2_0.7x_RGB_16_best.pth"
    relative_weights_path = "weights/jester_shufflenet_0.5x_G3_RGB_16_best.pth"
    weights_path = os.path.join(cwd, relative_weights_path)
    # model = create_mobilenetv2(pretrained_weights_path=weights_path)
    model = create_shufflenet(weights_path)

    # Read config
    lamp_cfg = read_config(os.path.join(cwd, "config.yaml"))
    print("Lamp Config: ", lamp_cfg)

    # Driver
    driver = lamp_driver.LampDriver()
    # Initialize the webcam for hand gesture recognition
    cap = cv2.VideoCapture(1)
    input_dim = 112
    try:
        i = 0
        gathered_img = np.zeros((16, 3, input_dim, input_dim))
        while True:
            # Read each frame from the webcam
            _, frame = cap.read()
            reshaped, frame = preprocess_mobilenetv2_from_cv2(
                frame, reshape_size=(input_dim, input_dim))
            gathered_img[i % 16] = reshaped
            if i != 0 and i % 20 == 0:
                input_tensor = preprocess_mobilenetv2_queued(gathered_img)
                first_time = time.time()
                pred = model(input_tensor)
                after_pred_time = time.time()
                pred_label = int(torch.argmax(pred))
                pred_parsed = JESTER_LABELS[pred_label]
                print("Predicted Label: ", pred_parsed,
                      after_pred_time - first_time, " seconds")
                if pred_parsed != "No gesture":
                    print("Turn lamp on!")
                    driver.set_lamp_state(1, 1, 1, 1)
                elif pred_parsed == "No gesture":
                    print("Turn lamp off!")
                    driver.set_lamp_state(1, 1, 1, 0)
                # if pred_parsed == lamp_cfg.on_gesture:
                #     print("Turn lamp on!")
                #     driver.set_lamp_state(1, 1, 1, 1)
                # elif pred_parsed == lamp_cfg.off_gesture:
                #     print("Turn lamp off!")
                #     driver.set_lamp_state(1, 1, 1, 0)

                gathered_img = np.zeros((16, 3, input_dim, input_dim))
            i += 1
            time.sleep(0.1)
    finally:
        # release the webcam and destroy all active windows
        print("Cleaning up...")
        cap.release()
        cv2.destroyAllWindows()
