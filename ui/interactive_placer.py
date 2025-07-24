# In ui/interactive_placer.py

import cv2
import numpy as np


def place_and_resize_cutout(bg_img, cutout_orig):
    """
    An interactive window to let the user place and manually resize the cutout.

    Returns:
        tuple: (top-left x, top-left y, final resized cutout image) or (None, None, None) if cancelled.
    """
    h_bg, w_bg, _ = bg_img.shape
    h_orig, w_orig, _ = cutout_orig.shape
    aspect_ratio = w_orig / h_orig

    # --- State Management Dictionary ---
    state = {
        "top_left": (w_bg // 2 - w_orig // 2, h_bg // 2 - h_orig // 2),
        "size": (w_orig, h_orig),
        "mode": "idle",  # Can be 'idle', 'dragging', or 'resizing'
        "offset": (0, 0)
    }

    handle_size = 20  # Size of the resize handle

    def mouse_callback(event, x, y, flags, param):
        w, h = state["size"]
        x1, y1 = state["top_left"]
        x2, y2 = x1 + w, y1 + h

        handle_x1, handle_y1 = x2 - handle_size // 2, y2 - handle_size // 2
        handle_x2, handle_y2 = x2 + handle_size // 2, y2 + handle_size // 2

        if event == cv2.EVENT_LBUTTONDOWN:
            if handle_x1 <= x <= handle_x2 and handle_y1 <= y <= handle_y2:
                state["mode"] = "resizing"
            elif x1 <= x <= x2 and y1 <= y <= y2:
                state["mode"] = "dragging"
                state["offset"] = (x - x1, y - y1)

        elif event == cv2.EVENT_LBUTTONUP:
            state["mode"] = "idle"

        elif event == cv2.EVENT_MOUSEMOVE:
            if state["mode"] == "dragging":
                state["top_left"] = (x - state["offset"][0], y - state["offset"][1])
            elif state["mode"] == "resizing":
                new_w = x - x1
                new_h = int(new_w / aspect_ratio)
                if new_w > 20 and new_h > 20:  # Set a minimum size
                    state["size"] = (new_w, new_h)

    cv2.namedWindow("Place and Resize Cutout")
    cv2.setMouseCallback("Place and Resize Cutout", mouse_callback)

    print("\n--- Interactive Placement & Sizing ---")
    print("🖱️ Drag the cutout to move. Drag the corner handle to resize.")
    print("✅ Press [Enter] to confirm. Press [Esc] to cancel.")

    while True:
        preview = bg_img.copy()
        w, h = state["size"]
        x1, y1 = state["top_left"]
        x2, y2 = x1 + w, y1 + h

        # Resize the original cutout to the current state size
        final_cutout = cv2.resize(cutout_orig, state["size"], interpolation=cv2.INTER_AREA)

        # Draw cutout with alpha blending
        if 0 < w and 0 < h:
            roi_x1, roi_y1 = max(0, x1), max(0, y1)
            roi_x2, roi_y2 = min(x2, w_bg), min(y2, h_bg)

            if roi_x1 < roi_x2 and roi_y1 < roi_y2:
                cutout_w, cutout_h = roi_x2 - roi_x1, roi_y2 - roi_y1

                cutout_slice = final_cutout[:cutout_h, :cutout_w]
                bg_slice = preview[roi_y1:roi_y2, roi_x1:roi_x2]

                alpha = cutout_slice[:, :, 3:] / 255.0
                blended = (cutout_slice[:, :, :3] * alpha) + (bg_slice * (1 - alpha))
                preview[roi_y1:roi_y2, roi_x1:roi_x2] = blended

        # Draw bounding box and handle
        cv2.rectangle(preview, (x1, y1), (x2, y2), (0, 255, 0), 1)
        cv2.circle(preview, (x2, y2), handle_size // 2, (0, 255, 0), -1)

        cv2.imshow("Place and Resize Cutout", preview)

        key = cv2.waitKey(20) & 0xFF
        if key == 13:  # Enter
            cv2.destroyAllWindows()
            return x1, y1, final_cutout
        elif key == 27:  # Escape
            cv2.destroyAllWindows()
            return None, None, None