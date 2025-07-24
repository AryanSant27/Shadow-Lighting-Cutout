# In analysis/light_analyzer.py
# Make sure to have 'import cv2' and 'import numpy as np' at the top
import cv2
import numpy as np

def infer_light_from_shadows(shadow_mask, min_contour_area=500):
    """
    Infers the primary light source direction by analyzing shadow orientation.

    Args:
        shadow_mask (np.ndarray): The binary mask of shadows.
        min_contour_area (int): The minimum area for a shadow to be considered.

    Returns:
        np.ndarray: A normalized 2D vector representing the light direction,
                    or None if no suitable shadows are found.
    """
    # Find contours of all the shadow regions
    contours, _ = cv2.findContours(shadow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    orientations = []
    weights = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Filter out small, noisy contours and ensure the contour is large enough to fit an ellipse
        if area > min_contour_area and len(cnt) >= 5:
            # Fit an ellipse to the contour. This gives us its orientation.
            _, _, angle = cv2.fitEllipse(cnt)

            # The angle of the major axis of the ellipse indicates the shadow's stretch direction
            orientations.append(angle)
            weights.append(area)  # Use the area as the weight

    if not orientations:
        print("⚠️ Could not infer light direction. No significant shadows found.")
        return None

    # Calculate the weighted average of the angles
    # We convert angles to vectors to average them correctly, then convert back
    avg_rad = np.deg2rad(np.average(orientations, weights=weights))

    # Create the 2D light vector from the average angle
    # This vector points in the direction of the shadow's stretch
    light_vector = np.array([np.cos(avg_rad), np.sin(avg_rad)], dtype=np.float32)

    print(f"✅ Inferred Light Vector (2D): {light_vector}")
    return light_vector