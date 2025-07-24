# In ui/horizon_definer.py

import cv2
import numpy as np


def define_horizon_interactively(image):
    """
    Opens a window for the user to click two points to define the horizon.

    Returns:
        list: A list containing two (x, y) tuples for the horizon line.
    """
    points = []
    clone = image.copy()

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 2:
            points.append((x, y))
            cv2.circle(clone, (x, y), 5, (0, 255, 0), -1)
            if len(points) == 2:
                cv2.line(clone, points[0], points[1], (0, 255, 0), 2)

    cv2.namedWindow("Horizon Definer")
    cv2.setMouseCallback("Horizon Definer", mouse_callback)

    while True:
        temp_img = clone.copy()

        # Add instructions
        instruction = "Click two points to define the horizon." if len(points) < 2 else "Horizon defined."
        cv2.putText(temp_img, instruction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(temp_img, "Press [r] to reset, [Enter] to confirm.", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Horizon Definer", temp_img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):  # Reset
            points = []
            clone = image.copy()
        elif key == 13 and len(points) == 2:  # Enter key
            break

    cv2.destroyAllWindows()

    print(f"✅ Horizon line defined by points: {points}")
    return points