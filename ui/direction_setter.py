# In ui/direction_setter.py

import cv2
import numpy as np


def get_light_source_position(image):
    """
    Opens a window for the user to click a point for the light source.

    Returns:
        tuple: The (x, y) coordinate of the light source.
    """
    light_pos = None
    clone = image.copy()

    def mouse_callback(event, x, y, flags, param):
        nonlocal light_pos
        if event == cv2.EVENT_LBUTTONDOWN:
            light_pos = (x, y)

    cv2.namedWindow("Set Light Source Position")
    cv2.setMouseCallback("Set Light Source Position", mouse_callback)

    while True:
        temp_img = clone.copy()

        if light_pos:
            cv2.circle(temp_img, light_pos, 15, (0, 255, 255), 2)
            cv2.putText(temp_img, "Sun Position Set", (light_pos[0] + 20, light_pos[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        instruction = "Click to mark the light source (the sun)." if not light_pos else "Press [Enter] to confirm."
        cv2.putText(temp_img, instruction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Set Light Source Position", temp_img)
        key = cv2.waitKey(20) & 0xFF
        if key == 13 and light_pos:  # Enter
            break

    cv2.destroyAllWindows()

    print(f"☀️ Light source set at: {light_pos}")
    return light_pos