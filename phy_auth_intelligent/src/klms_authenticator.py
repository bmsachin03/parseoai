"""
Implements the Kernel Least Mean Squares adaptive authentication process.
"""

from src.kernel_machine import compute_kernel_output
from src.config import LEARNING_RATE

class KLMSAuthenticator:
    def __init__(self):
        self.alpha = []
        self.memory = []

    def predict(self, x):
        return compute_kernel_output(self.alpha, self.memory, x)

    def update(self, x, y):
        y_hat = self.predict(x)
        error = y - y_hat
        self.alpha.append(LEARNING_RATE * error)
        self.memory.append(x)
        return error
