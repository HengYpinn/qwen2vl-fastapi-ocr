# Utility functions to compute image quality metrics: blur and glare intensity.

import cv2
import numpy as np
from PIL import Image

def compute_blur_intensity(pil_img: Image.Image, max_var: float = 1000.0) -> int:
    """
    Compute blur intensity of an image as the variance of the Laplacian, scaled to 0–100.

    Args:
        pil_img: PIL.Image.Image input image.
        max_var: float, value of variance corresponding to 100% blur (tune as needed).

    Returns:
        Integer 0–100 representing blur intensity percentage.
    """
    # Convert to grayscale
    gray = np.array(pil_img.convert("L"))
    # Compute variance of Laplacian (focus measure)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    # Scale to 0–100
    score = int(min(max((fm / max_var) * 100, 0), 100))
    return score

def compute_glare_intensity(pil_img: Image.Image, threshold: int = 240) -> int:
    """
    Compute glare intensity as the percentage of pixels above a brightness threshold.

    Args:
        pil_img: PIL.Image.Image input image.
        threshold: grayscale level above which pixels count as glare (0–255).

    Returns:
        Integer 0–100 representing glare intensity percentage.
    """
    gray = np.array(pil_img.convert("L"))
    # Ratio of over-threshold pixels
    glare_ratio = float(np.mean(gray >= threshold))
    return int(glare_ratio * 100)

