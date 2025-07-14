"""
Implements the Kernel Least Mean Squares adaptive authentication process.
"""

from kernel_machine import compute_kernel_output
from config import LEARNING_RATE

class KLMSAuthenticator:
    def __init__(self):
        """
        Initialize the KLMSAuthenticator with empty coefficient and memory lists.
        """
        self.alpha = []
        self.memory = []

    def predict(self, x):
        """
        Predicts the output for the given input using the current kernel model state.
        
        Parameters:
            x: Input sample for which to compute the prediction.
        
        Returns:
            The predicted output value for the input sample.
        """
        return compute_kernel_output(self.alpha, self.memory, x)

    def update(self, x, y):
        """
        Update the KLMS model with a new input-output pair and return the prediction error.
        
        The method predicts the output for input `x`, computes the error with respect to the true output `y`, updates the model's coefficients and memory with the scaled error and input, and returns the error value.
        
        Returns:
            error (float): The difference between the true output and the predicted output for input `x`.
        """
        y_hat = self.predict(x)
        error = y - y_hat
        self.alpha.append(LEARNING_RATE * error)
        self.memory.append(x)
        return error
