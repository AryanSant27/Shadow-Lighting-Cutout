# In image_utils.py

import cv2

def load_background(path):
    """Loads the background image."""
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not load background image at: {path}")
    print("✅ Background loaded.")
    return img

def load_cutout(path):
    """Loads the cutout image with transparency."""
    # IMREAD_UNCHANGED ensures the alpha channel is loaded
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Could not load cutout image at: {path}")
    if img.shape[2] != 4:
        raise ValueError("Cutout image must be a 4-channel BGRA image with a transparent background.")
    print("✅ Cutout loaded.")
    return img