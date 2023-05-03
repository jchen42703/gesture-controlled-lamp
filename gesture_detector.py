import cv2
from lamp_common import *
from lamp_service import LampService


class GestureDetector:
    """This class is used to keep track of collections of frames to detect
    gestures when a motion starts.
    """

    def __init__(self, lampi=False, abs_diff_thresh=0.02) -> None:
        self.lampi = lampi
        self.prev_mask = None
        self.prev_contour_area = None
        self.abs_diff_thresh = abs_diff_thresh
        self.lampi_service = LampService()

    def detect_gesture_type(self, curr_mask, curr_contour_area):
        """Collects differences in contour area sizes in the current window
        and detects the gesture from those contour area size changes.
        """
        # Do nothing
        if self.prev_mask is None or self.prev_contour_area is None:
            self.prev_mask = curr_mask
            self.prev_contour_area = curr_contour_area
            return

        percent_diff = (curr_contour_area -
                        self.prev_contour_area) / self.prev_contour_area
        print("percent diff", percent_diff)
        self.prev_contour_area = curr_contour_area
        self.prev_mask = curr_mask

        # If the area size change isn't big enough, do nothing
        if abs(percent_diff) < self.abs_diff_thresh:
            # return SUPPORTED_GESTURES[0]
            return self.lampi_service.run_from_gesture(SUPPORTED_GESTURES[0])

        # If contour area size changes are increasing -> Move hand in
        if percent_diff > 0:
            # return SUPPORTED_GESTURES[2]
            return self.lampi_service.run_from_gesture(SUPPORTED_GESTURES[2])

        # If decreasing -> move hand away
        if percent_diff < 0:
            # return SUPPORTED_GESTURES[3]
            return self.lampi_service.run_from_gesture(SUPPORTED_GESTURES[3])

        return self.lampi_service.run_from_gesture(SUPPORTED_GESTURES[-1])


def get_mask_basic(initial_frame, curr_frame, threshold):
    # Check if motion is detected -> diff between frames is > frameDiffThreshold
    frameDelta = cv2.absdiff(initial_frame, curr_frame)
    thresh = cv2.threshold(frameDelta, threshold, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    return thresh, frameDelta


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
