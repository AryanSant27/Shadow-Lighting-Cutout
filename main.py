# In main.py

import cv2
import numpy as np
import os

from image_utils import load_background, load_cutout
from ui.angle_estimator import get_sun_angle_from_boxes
from ui.interactive_placer import place_and_resize_cutout
from ui.direction_setter import get_light_source_position
# Note the updated import to the final generator
from generation.perspective_shadow_generator import generate_perspective_shadow


def main():
    background_path = "assets/background.jpg"
    cutout_path = "assets/person_cutout.png"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    bg_image = load_background(background_path)
    cutout_image = load_cutout(cutout_path)

    sun_angle, _ = get_sun_angle_from_boxes(bg_image)
    x1, y1, final_cutout = place_and_resize_cutout(bg_image, cutout_image)
    if final_cutout is None:
        print("❌ Placement cancelled. Exiting.");
        return
    sun_pos = get_light_source_position(bg_image)

    # --- 1. Calculate the Shadow Polygon ---
    h_co, w_co, _ = final_cutout.shape
    feet_pos = (x1 + w_co // 2, y1 + h_co)

    shadow_direction = np.array(feet_pos) - np.array(sun_pos)
    if np.linalg.norm(shadow_direction) == 0: shadow_direction = np.array([0, 1])
    shadow_direction_unit = shadow_direction / np.linalg.norm(shadow_direction)

    base_width = w_co * 0.8  # Use a wider base for better perspective
    perp_direction = np.array([-shadow_direction_unit[1], shadow_direction_unit[0]])
    base_point_left = tuple((np.array(feet_pos) - perp_direction * base_width / 2).astype(int))
    base_point_right = tuple((np.array(feet_pos) + perp_direction * base_width / 2).astype(int))

    shadow_length = h_co / np.tan(np.deg2rad(max(sun_angle, 1.0)))

    shadow_endpoint_left = tuple((np.array(base_point_left) + shadow_direction_unit * shadow_length).astype(int))
    shadow_endpoint_right = tuple((np.array(base_point_right) + shadow_direction_unit * shadow_length).astype(int))

    shadow_polygon = np.array([base_point_left, base_point_right, shadow_endpoint_right, shadow_endpoint_left])

    # --- 2. Generate the Shadow using the polygon ---
    shadow_layer = generate_perspective_shadow(final_cutout, shadow_polygon, bg_image.shape[:2])

    # --- 3. Composite Final Image ---
    output_image = bg_image.copy()
    shadow_alpha = shadow_layer[:, :, 3] / 255.0
    for c in range(3):
        output_image[:, :, c] = (1 - shadow_alpha) * output_image[:, :, c] + shadow_alpha * shadow_layer[:, :, c]

    cutout_alpha = final_cutout[:, :, 3:] / 255.0
    roi = output_image[y1:y1 + h_co, x1:x1 + w_co]
    blended_roi = (final_cutout[:, :, :3] * cutout_alpha) + (roi * (1 - cutout_alpha))
    output_image[y1:y1 + h_co, x1:x1 + w_co] = blended_roi

    # --- 4. Save and Display ---
    output_path = os.path.join(output_dir, "final_composite.png")
    cv2.imwrite(output_path, output_image)
    print(f"\n🎉🎉🎉 Success! Final image saved to: {output_path}")
    cv2.imshow("Final Composite", output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()