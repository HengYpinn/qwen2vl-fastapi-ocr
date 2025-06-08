# utils/image_quality.py
# Utility functions to compute image quality metrics: blur and glare intensity.

import cv2
import numpy as np
from PIL import Image

def compute_blur_intensity(pil_img: Image.Image, min_var: float = 100.0, max_var: float = 1000.0) -> int:
    """
    Compute blur intensity of an image as a percentage (0–100), where:
      - 0 means very sharp (high focus measure)
      - 100 means very blurry (low focus measure)

    Uses variance of Laplacian (focus measure): the lower the variance, the more blurred the image.

    Args:
        pil_img: PIL.Image.Image input image.
        min_var: float, variance value mapped to 100% sharpness baseline.
        max_var: float, variance value mapped to 0% sharpness baseline.

    Returns:
        Integer 0–100 representing blur intensity percentage.
    """
    # Convert to grayscale
    gray = np.array(pil_img.convert("L"))
    # Compute variance of Laplacian
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    # Normalize focus measure to [0,1]
    norm = (fm - min_var) / (max_var - min_var)
    norm = np.clip(norm, 0.0, 1.0)
    # Invert so lower variance (blurry) → higher score
    blur_score = int((1.0 - norm) * 100)
    return blur_score

def compute_glare_intensity(pil_img: Image.Image, threshold: int = 250) -> int:
    """
    Compute glare intensity of an image as a percentage (0–100), based on the proportion of very bright pixels.

    Args:
        pil_img: PIL.Image.Image input image.
        threshold: grayscale threshold (0–255) above which pixels count as glare.

    Returns:
        Integer 0–100 representing glare intensity percentage.
    """
    # Convert to grayscale
    gray = np.array(pil_img.convert("L"))
    # Exclude borders (e.g., document margins) to avoid counting white background
    h, w = gray.shape
    h_margin = int(0.05 * h)
    w_margin = int(0.05 * w)
    roi = gray[h_margin : h - h_margin, w_margin : w - w_margin]
    # Proportion of pixels above threshold
    glare_ratio = float(np.mean(roi >= threshold))
    return int(glare_ratio * 100)