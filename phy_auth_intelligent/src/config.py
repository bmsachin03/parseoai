"""
Global configuration constants for PHY layer authentication.
"""

# Gaussian kernel width
KERNEL_WIDTH = 0.5

# KLMS learning rate
LEARNING_RATE = 0.1

# Normalization ranges for PHY attributes
ATTRIBUTE_RANGES = {
    "CFO": (-78.125e3, 78.125e3),   # Hz
    "CIR": (-1.0, 1.0),             # normalized amplitude
    "RSSI": (-120, 0),              # dBm
}
