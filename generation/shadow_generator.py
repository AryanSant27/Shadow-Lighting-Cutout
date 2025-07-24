# In generation/shadow_generator.py

import cv2
import numpy as np


def generate_shadow_from_polygon(shadow_polygon, output_shape):
    """
    Creates a blurred shadow by directly filling a polygon.
    """
    h_out, w_out = output_shape

    # Create a transparent canvas
    shadow_layer = np.zeros((h_out, w_out, 4), dtype=np.uint8)

    # Check if the polygon has a valid area
    if shadow_polygon is not None and len(shadow_polygon) > 0:
        # Create a mask by drawing and filling the polygon in white on a black canvas
        mask = np.zeros((h_out, w_out), dtype=np.uint8)
        cv2.fillPoly(mask, [shadow_polygon.astype(np.int32)], 255)

        # Blur the mask to create soft, feathered edges
        blurred_mask = cv2.GaussianBlur(mask, (55, 55), 0)

        # Set the alpha channel of our shadow layer to this blurred mask
        # Apply opacity cap of 50%
        shadow_layer[:, :, 3] = (blurred_mask * 0.5).astype(np.uint8)
        # The color channels (0, 1, 2) are already 0 (black).

    print("✅ Shadow generated from polygon.")
    return shadow_layer