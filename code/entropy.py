"""
entropy: Shannon Information Entropy helper.
"""

import numpy as np


def compute_shannon_entropy(data_points: np.ndarray, bins: int = 50) -> float:
    """Compute normalized Shannon Information Entropy."""
    hist, _ = np.histogram(data_points, bins=bins, density=True)
    hist = hist[hist > 0]  # Filter zero probabilities to avoid log(0)
    return -np.sum(
        hist * np.log(hist) * (data_points.max() - data_points.min()) / bins
    )