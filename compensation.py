"""
This module handles compensation calculations for the interview simulation project.

It provides functions to map skill scores to compensation and to make adjusted offers.
"""

from interview_config import settings
import math


def map_skill_to_compensation(skill_score: int) -> float:
    """
    Maps a skill score to a corresponding compensation value.

    The mapping is done using a piecewise linear function with different slopes
    for different ranges of skill scores. For scores above 90, a quadratic function
    is used to model diminishing returns.

    Args:
        skill_score (int): The skill score to map, expected to be between 1 and 100.

    Returns:
        float: The mapped compensation value.
    """
    skill_score = max(1, min(100, skill_score))

    if skill_score <= 25:
        return linear_interpolation(
            skill_score, 1, 25, settings.MIN_COMPENSATION, settings.P25_COMPENSATION
        )
    elif skill_score <= 50:
        return linear_interpolation(
            skill_score, 25, 50, settings.P25_COMPENSATION, settings.MEDIAN_COMPENSATION
        )
    elif skill_score <= 75:
        return linear_interpolation(
            skill_score, 50, 75, settings.MEDIAN_COMPENSATION, settings.P75_COMPENSATION
        )
    elif skill_score <= 90:
        return linear_interpolation(
            skill_score, 75, 90, settings.P75_COMPENSATION, settings.P90_COMPENSATION
        )
    else:
        percentage = (skill_score - 90) / 10
        return settings.P90_COMPENSATION + (
            settings.MAX_COMPENSATION - settings.P90_COMPENSATION
        ) * math.pow(percentage, 2)


def linear_interpolation(x: float, x1: float, x2: float, y1: float, y2: float) -> float:
    """
    Perform linear interpolation between two points.

    Args:
        x (float): The input value to interpolate.
        x1 (float): The lower bound of the input range.
        x2 (float): The upper bound of the input range.
        y1 (float): The lower bound of the output range.
        y2 (float): The upper bound of the output range.

    Returns:
        float: The interpolated value.
    """
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)


def make_offer(final_score: int, adjustment: float) -> float:
    """
    Calculate a compensation offer based on a final score and an adjustment factor.

    Args:
        final_score (int): The final skill score, expected to be between 1 and 100.
        adjustment (float): An adjustment factor, between -0.5 and 5.

    Returns:
        float: The calculated offer amount, always non-negative.
    """
    final_score = max(1, min(100, final_score))
    adjustment = max(-0.5, min(5, adjustment))
    true_compensation = map_skill_to_compensation(final_score)
    offer = true_compensation * (1 + adjustment)
    return max(0, offer)
