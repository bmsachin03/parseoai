"""
Kernel-based physical attribute fusion using Gaussian kernel.
"""

import numpy as np
from config import KERNEL_WIDTH

def gaussian_kernel(x1, x2, sigma=KERNEL_WIDTH):
    """
    Compute the Gaussian kernel similarity between two input vectors.
    
    Parameters:
        x1 (array-like): First input vector.
        x2 (array-like): Second input vector.
        sigma (float, optional): Kernel width parameter. Defaults to KERNEL_WIDTH.
    
    Returns:
        float: Gaussian kernel value representing the similarity between x1 and x2.
    """
    diff = np.array(x1) - np.array(x2)
    return np.exp(-np.dot(diff, diff) / (2 * sigma**2))

def compute_kernel_output(alpha, memory, x):
    """
    Compute the weighted sum of Gaussian kernel similarities between a query vector and a set of memory vectors.
    
    Parameters:
        alpha (array-like): Weights corresponding to each memory vector.
        memory (array-like): Collection of vectors to compare against the query vector.
        x (array-like): Query vector.
    
    Returns:
        float: The weighted sum of Gaussian kernel evaluations between the query vector and each memory vector.
    """
    return sum(a * gaussian_kernel(m, x) for a, m in zip(alpha, memory))
