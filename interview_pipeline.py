"""
This module defines the InterviewPipeline for the interview simulation project.

It includes classes and functions for creating and running interview pipelines
with different elimination strategies.
"""

from typing import List, Tuple, Callable, Literal, Dict
from engineer import Engineer
from interview import InterviewStep, Interview
from interview_config import settings

EliminationType = Literal["immediate", "aggregate"]


def create_elimination_function(
    elimination_type: EliminationType,
) -> Callable[[List[Dict[str, float]], float], bool]:
    """
    Create an elimination function based on the specified elimination type.

    Args:
        elimination_type (EliminationType): The type of elimination strategy to use.

    Returns:
        Callable[[List[Dict[str, float]], float], bool]: A function that determines
        whether a candidate should be eliminated based on their scores.

    Raises:
        ValueError: If an invalid elimination type is provided.
    """
    if elimination_type == "immediate":
        return lambda scores, target: scores[-1]["avg"] < target
    elif elimination_type == "aggregate":
        return (
            lambda scores, target: sum(s["avg"] for s in scores) / len(scores) < target
        )
    else:
        raise ValueError("Invalid elimination type. Choose 'immediate' or 'aggregate'.")


class InterviewPipeline:
    """
    Represents an interview pipeline consisting of multiple interview steps.
    """

    def __init__(self, steps: List[InterviewStep]):
        """
        Initialize an InterviewPipeline with a list of InterviewStep objects.

        Args:
            steps (List[InterviewStep]): The steps of the interview pipeline.
        """
        self.steps = steps

    def __call__(
        self,
        target_skill_score: float,
        elimination_type: EliminationType,
        candidate: Engineer,
    ) -> Tuple[float, List[Dict[str, float]]]:
        """
        Conduct the interview pipeline for a candidate.

        Args:
            target_skill_score (float): The target skill score for the candidate.
            elimination_type (EliminationType): The type of elimination strategy to use.
            candidate (Engineer): The candidate being interviewed.

        Returns:
            Tuple[float, List[Dict[str, float]]]: A tuple containing the total interview time
            and a list of score dictionaries for each completed step.
        """
        elimination_function = create_elimination_function(elimination_type)
        total_time = 0
        scores = []

        for step in self.steps:
            total_time += step.duration
            current_score = step.conduct(candidate)
            scores.append(current_score)

            if elimination_function(scores, target_skill_score):
                return total_time, scores

        return total_time, scores


def create_interview_pipeline(*steps: InterviewStep) -> InterviewPipeline:
    """
    Create an InterviewPipeline from a series of InterviewStep objects.

    Args:
        *steps (InterviewStep): Variable number of InterviewStep instances.

    Returns:
        InterviewPipeline: A new InterviewPipeline instance.
    """
    return InterviewPipeline(list(steps))