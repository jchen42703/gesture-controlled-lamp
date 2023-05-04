# Lamp Bluetooth Peripheral

## Plan

1. Create GATT characteristic that can be read, written, and notified.
   1. It should store a JSON configuration of the mapped gestures.
2. The peripheral should listen and serve this gesture.

## User Stories

1. When the user changes the configuration on their mobile phone, they should be able to send that configuration over bluetooth to the lampi.
   1. When the lampi receives the payload, it should validate the payload and write it to `config.yaml`.
2. When the user starts their mobile app, they should be able to read the current gesture mapping over bluetooth.
