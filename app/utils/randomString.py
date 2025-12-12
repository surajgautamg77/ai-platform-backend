import string
import random

def randomString(size=6, chars=None):
    """
    Generate a random ID of given size.
    
    Args:
        size (int): Length of the ID. Default is 6.
        chars (str): Characters to choose from. 
                     Default: A–Z + 0–9.
    
    Returns:
        str: Randomly generated ID.
    """
    if chars is None:
        chars = string.ascii_uppercase + string.digits
    
    return ''.join(random.choice(chars) for _ in range(size))
