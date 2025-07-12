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

def compute_glare_intensity(pil_img: Image.Image, threshold: int = 240, window: int = 64, local_offset: int = 20) -> int:
    """
    Compute true glare intensity as the percentage of pixels that are
    local outliers (much brighter than their neighborhood and above threshold).

    Args:
        pil_img: PIL.Image.Image input image.
        threshold: base brightness (0–255) above which pixels may count as glare.
        window: sliding window size for local region (pixels).
        local_offset: how much brighter than local mean is considered "glare".

    Returns:
        Integer 0–100 representing glare intensity percentage.
    """
    gray = np.array(pil_img.convert("L"))
    h, w = gray.shape
    glare_mask = np.zeros_like(gray, dtype=np.uint8)
    for y in range(0, h-window+1, window//2):
        for x in range(0, w-window+1, window//2):
            roi = gray[y:y+window, x:x+window]
            local_mean = roi.mean()
            mask = (roi > local_mean + local_offset) & (roi > threshold)
            glare_mask[y:y+window, x:x+window][mask] = 255
    # Remove tiny specks (noise)
    glare_mask = cv2.morphologyEx(glare_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    glare_percent = int(100 * np.sum(glare_mask > 0) / (h * w))
    return glare_percent