# Gesture Controlled Lamp

## Getting Started

Run the Kivy UI:

```bash
python3 run_ui.py
```

Run the gesture detection:

```bash
python3 basic_gestures.py 1 -l

# With debug mode (see camera feed)
python3 basic_gestures.py 1 -d -l

# On local
python3 basic_gestures.py /dev/video2 -d
```

Run the bluetooth service:

```bash
cd bluetooth
node peripheral.js
```

For the IOS app, open the XCode project in `app/Lampi/Lampi.xcodeproj`.

Run the ML gesture detection:

```bash
cd ml_scripts
python3 demo.py
```

## Notes

- On local computer, the `jester_shufflenet_0.5x_G3_RGB_16_best.pth` has prediction times ranging from roughly 0.1-0.2s.
  - On the Pi, the prediction times shoot up to 2-2.5s. Hence, it's roughly 10x slower.
    - But, on Pi, the memory consumed is really little (only 20% while script is running).
  - For real-time gesture recognition, 2.5s is far too slow.
- With TFLite, able to get around 0.5s prediction times on the Pi, but that's still way too slow (ends up processing at roughly 1 frame per second)
  - Need around 100-200ms prediction speed to be viable.

## Back-Up Plan 1

Scope out complicated gesture detection and just use basic computer vision.

1. Register initial frame.
2. Check the difference between the current frame and initial frame.
3. Start "recording" after the current frame's object's area exceeds `AREA_THRESHOLD`.
4. While reading each frame:
   1. If the area decreases, decrease the brightness.
   2. If the area increases, increase the brightness.
   3. What if they don't move?
      1. Brightness doesn't change
   4. Quick swipe left: toggle lamp
   5. If the area is `<= AREA_THRESHOLD`, stop recording.
5. Repeat!

## Back-Up Plan 2

WS API with GPU Model Prediction EC2 Instance
