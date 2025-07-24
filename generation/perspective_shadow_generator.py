# In generation/perspective_shadow_generator.py

import cv2
import numpy as np


def generate_perspective_shadow(cutout, shadow_polygon, output_shape):
    """
    Creates a realistic shadow by warping the cutout's silhouette into
    the provided 4-point shadow polygon with final stylistic adjustments.
    """
    # --- Final Tweakable Parameters ---
    blur_kernel_size = (21, 21)

    # Opacity set to 35%
    max_opacity = 0.35

    # HEX #052d47 converted to BGR is (71, 45, 5)
    shadow_color_bgr = (71, 45, 5)
    # ------------------------------------

    h_out, w_out = output_shape
    h_co, w_co, _ = cutout.shape

    if shadow_polygon is None or len(shadow_polygon) < 4:
        return np.zeros((h_out, w_out, 4), dtype=np.uint8)

    cutout_alpha = cutout[:, :, 3]

    src_rect = np.array([[0, 0], [w_co, 0], [w_co, h_co], [0, h_co]], dtype=np.float32)
    dst_poly = np.array([
        shadow_polygon[3], shadow_polygon[2], shadow_polygon[1], shadow_polygon[0]
    ], dtype=np.float32)

    if cv2.contourArea(dst_poly) < 5.0:
        print("☀️ Shadow is too small to render.")
        return np.zeros((h_out, w_out, 4), dtype=np.uint8)

    M = cv2.getPerspectiveTransform(src_rect, dst_poly)
    warped_mask = cv2.warpPerspective(cutout_alpha, M, (w_out, h_out), flags=cv2.INTER_AREA)

    blurred_mask = cv2.GaussianBlur(warped_mask, blur_kernel_size, 0)

    final_shadow_layer = np.zeros((h_out, w_out, 4), dtype=np.uint8)

    final_shadow_layer[:, :, 0] = shadow_color_bgr[0]
    final_shadow_layer[:, :, 1] = shadow_color_bgr[1]
    final_shadow_layer[:, :, 2] = shadow_color_bgr[2]

    final_shadow_layer[:, :, 3] = (blurred_mask * max_opacity).astype(np.uint8)

    print("✅ Final shadow generated with custom style.")
    return final_shadow_layer