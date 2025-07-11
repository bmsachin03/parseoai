"""
Functions for normalizing physical layer attributes.
"""

from src.config import ATTRIBUTE_RANGES

def normalize_attribute(value, attr_name):
    """
    Normalize a numeric attribute value to a scale centered at zero based on its predefined range.
    
    Parameters:
        value (float): The attribute value to normalize.
        attr_name (str): The name of the attribute whose range is used for normalization.
    
    Returns:
        float: The normalized value, scaled to the range [-1, 1] with zero at the midpoint of the attribute's range.
    """
    a, b = ATTRIBUTE_RANGES[attr_name]
    return (2 / (b - a)) * (value - (a + b) / 2)

def normalize_vector(values, attr_names):
    """
    Normalize a list of physical layer attribute values based on their corresponding attribute ranges.
    
    Parameters:
        values (list): List of numeric values to be normalized.
        attr_names (list): List of attribute names corresponding to each value.
    
    Returns:
        list: List of normalized values, each scaled according to its attribute's predefined range.
    """
    return [normalize_attribute(v, attr) for v, attr in zip(values, attr_names)]
