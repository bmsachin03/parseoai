"""
Functions for normalizing physical layer attributes.
"""

from src.config import ATTRIBUTE_RANGES

def normalize_attribute(value, attr_name):
    a, b = ATTRIBUTE_RANGES[attr_name]
    return (2 / (b - a)) * (value - (a + b) / 2)

def normalize_vector(values, attr_names):
    return [normalize_attribute(v, attr) for v, attr in zip(values, attr_names)]
