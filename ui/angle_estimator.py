# In ui/angle_estimator.py

import cv2
import numpy as np


def get_sun_angle_from_boxes(image):
    """
    Opens a window for the user to draw boxes around an object and its shadow
    to calculate the sun's elevation angle.

    Returns:
        tuple: (The calculated angle in degrees, a list of the two rectangles).
    """
    rects = []
    current_rect = None
    drawing = False
    clone = image.copy()
    angle_deg = None  # Variable to hold the calculated angle

    instructions = [
        "Step 1: Draw a box on a TALL OBJECT (e.g., a tree).",
        "Step 2: Draw a box on that object's SHADOW."
    ]

    def draw_ui_text(img, angle):
        # Draw main instructions
        instruction_text = instructions[len(rects)] if len(rects) < 2 else "Boxes confirmed."
        cv2.putText(img, instruction_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Draw secondary instructions
        cv2.putText(img, "Press [r] to reset, [Enter] to confirm.", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (255, 255, 255), 2, cv2.LINE_AA)

        # --- NEW: Draw the angle on screen if it has been calculated ---
        if angle is not None:
            angle_text = f"Calculated Angle: {angle:.1f} degrees"
            cv2.putText(img, angle_text, (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

    def mouse_callback(event, x, y, flags, param):
        nonlocal current_rect, drawing, rects, clone, angle_deg

        if len(rects) == 2:  # Don't allow drawing more than 2 boxes
            return

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            current_rect = [(x, y), (x, y)]

        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            current_rect[1] = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            rects.append(tuple(current_rect))

            # --- NEW: Calculate angle as soon as the second box is drawn ---
            if len(rects) == 2:
                object_box = rects[0]
                shadow_box = rects[1]
                h = abs(object_box[0][1] - object_box[1][1])
                obj_center_x = (object_box[0][0] + object_box[1][0]) // 2
                obj_bottom_y = max(object_box[0][1], object_box[1][1])
                shadow_center_x = (shadow_box[0][0] + shadow_box[1][0]) // 2
                shadow_center_y = (shadow_box[0][1] + shadow_box[1][1]) // 2
                L = np.sqrt((obj_center_x - shadow_center_x) ** 2 + (obj_bottom_y - shadow_center_y) ** 2)
                if L > 0:
                    angle_deg = np.degrees(np.arctan(h / L))
                else:
                    angle_deg = 90.0  # If shadow is directly under object

    cv2.namedWindow("Sun Angle Estimator")
    cv2.setMouseCallback("Sun Angle Estimator", mouse_callback)

    while True:
        temp_img = image.copy()

        # Draw existing rectangles
        for i, rect in enumerate(rects):
            color = (0, 255, 0) if i == 0 else (0, 0, 255)
            cv2.rectangle(temp_img, rect[0], rect[1], color, 2)

        # Draw the rectangle currently being drawn
        if drawing and current_rect:
            cv2.rectangle(temp_img, current_rect[0], current_rect[1], (0, 255, 0), 2)

        # Add all text to the image
        draw_ui_text(temp_img, angle_deg)

        cv2.imshow("Sun Angle Estimator", temp_img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):  # Reset
            rects = []
            angle_deg = None
        elif key == 13 and len(rects) == 2:  # Enter key
            break

    cv2.destroyAllWindows()

    print(f"✅ Sun elevation angle confirmed: {angle_deg:.2f} degrees")
    return angle_deg, rects