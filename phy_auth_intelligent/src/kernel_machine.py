"""
Kernel-based physical attribute fusion using Gaussian kernel.
"""

import numpy as np
from src.config import KERNEL_WIDTH

def gaussian_kernel(x1, x2, sigma=KERNEL_WIDTH):
    diff = np.array(x1) - np.array(x2)
    return np.exp(-np.dot(diff, diff) / (2 * sigma**2))

def compute_kernel_output(alpha, memory, x):
    return sum(a * gaussian_kernel(m, x) for a, m in zip(alpha, memory))
