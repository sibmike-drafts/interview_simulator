"""
This module contains utility functions for generating random values
used in the Engineering Interview Simulator.
"""

import random


def generate_skill_score() -> int:
    """
    Generate a random skill score between 1 and 100 using a normal distribution.

    Returns:
        int: A random skill score.
    """
    mean = 50
    std_dev = 25

    score = round(random.gauss(mean, std_dev))
    if 1 <= score <= 100:
        return score
    elif score < 1:
        return 1

    return 100


def generate_error_std() -> float:
    """
    Generate a random error standard deviation.

    Returns:
        float: A random error standard deviation, typically between 0 and 20.
    """
    return max(0, random.gauss(10, 3))


def generate_bias() -> float:
    """
    Generate a random bias value.

    Returns:
        float: A random bias value, typically between -15 and 15.
    """
    return random.gauss(0, 5)


# You can add more generator functions as needed for your simulation

if __name__ == "__main__":
    # Test the functions
    print(f"Sample skill score: {generate_skill_score()}")
    print(f"Sample error std: {generate_error_std():.2f}")
    print(f"Sample bias: {generate_bias():.2f}")