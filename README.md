# Gesture Controlled Lamp

## Notes

- On local computer, the `jester_shufflenet_0.5x_G3_RGB_16_best.pth` has prediction times ranging from roughly 0.1-0.2s.
  - On the Pi, the prediction times shoot up to 2-2.5s. Hence, it's roughly 10x slower.
    - But, on Pi, the memory consumed is really little (only 20% while script is running).
  - For real-time gesture recognition, 2.5s is far too slow.
