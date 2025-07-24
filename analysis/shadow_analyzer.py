# In analysis/shadow_analyzer.py

import cv2
import numpy as np


def analyze_shadow_properties(image, block_size=51, c_value=8, gradient_threshold=15):
    """
    Analyzes the background image to find and classify hard and soft shadows.

    Returns:
        tuple: (hard_shadow_mask, soft_shadow_mask)
    """
    # Convert to LAB color space and get the L (Lightness) channel
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel = lab_image[:, :, 0]

    # Use adaptive thresholding to create a mask of all shadow areas
    shadow_mask = cv2.adaptiveThreshold(
        cv2.medianBlur(l_channel, 5), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, block_size, c_value
    )

    # Calculate the image gradient to find edge sharpness
    sobelx = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(l_channel, cv2.CV_64F, 0, 1, ksize=5)
    gradient_magnitude = cv2.magnitude(sobelx, sobely)
    gradient_normalized = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # Find contours of the shadow regions
    contours, _ = cv2.findContours(shadow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create empty masks for hard and soft shadows
    h, w = image.shape[:2]
    hard_shadow_mask = np.zeros((h, w), dtype=np.uint8)
    soft_shadow_mask = np.zeros((h, w), dtype=np.uint8)

    for cnt in contours:
        if cv2.contourArea(cnt) < 100: continue

        # Get the average gradient magnitude along the shadow's edge
        edge_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.drawContours(edge_mask, [cnt], -1, 255, 3)
        avg_gradient = cv2.mean(gradient_normalized, mask=edge_mask)[0]

        # Classify and draw the filled contour on the appropriate mask
        if avg_gradient > gradient_threshold:
            cv2.drawContours(hard_shadow_mask, [cnt], -1, 255, -1)
        else:
            cv2.drawContours(soft_shadow_mask, [cnt], -1, 255, -1)

    print("✅ Background shadow analysis complete.")
    return hard_shadow_mask, soft_shadow_mask