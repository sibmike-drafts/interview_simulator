"""
This module defines the Interview model for the interview simulation project.

It includes classes for InterviewStep and Interview, as well as utility functions
for creating interview steps and complete interviews.
"""

from typing import List, Dict, Any
from statistics import mean, median, stdev
from pydantic import BaseModel, Field
from engineer import Engineer
from interview_config import settings


class InterviewStep(BaseModel):
    """
    Represents a single step in an interview process.

    Each step has a duration and a list of interviewers who conduct this part of the interview.
    """

    duration: float = Field(
        ..., ge=settings.MIN_INTERVIEW_LENGTH, le=settings.MAX_INTERVIEW_LENGTH
    )
    interviewers: List[Any] = Field(..., description="List of Engineer objects")

    def conduct(self, candidate: Engineer) -> Dict[str, float]:
        """
        Conduct this step of the interview for a given candidate.

        Args:
            candidate (Engineer): The candidate being interviewed.

        Returns:
            Dict[str, float]: A dictionary containing the following statistics of the scores:
                - min: Minimum score
                - max: Maximum score
                - avg: Average score
                - median: Median score
                - std: Standard deviation of scores
        """
        scores = [
            interviewer.estimate_other_skill(candidate, self.duration)
            for interviewer in self.interviewers
        ]

        return {
            "min": min(scores),
            "max": max(scores),
            "avg": mean(scores),
            "median": median(scores),
            "std": stdev(scores) if len(scores) > 1 else 0,
        }


class Interview(BaseModel):
    """
    Represents a complete interview process composed of multiple steps.
    """

    steps: List[InterviewStep]

    def validate(self):
        """
        Validate the interview structure.

        Raises:
            ValueError: If the interview has no steps or if any step has no interviewers.
        """
        if not self.steps:
            raise ValueError("Interview must have at least one step")
        for step in self.steps:
            if not step.interviewers:
                raise ValueError(
                    "Each interview step must have at least one interviewer"
                )

    def conduct(self, candidate: Engineer) -> List[Dict[str, float]]:
        """
        Conduct the full interview process for a given candidate.

        Args:
            candidate (Engineer): The candidate being interviewed.

        Returns:
            List[Dict[str, float]]: A list of dictionaries, each containing the statistics
            for one step of the interview.
        """
        return [step.conduct(candidate) for step in self.steps]


def create_interview_step(duration: float, *interviewers: Engineer) -> InterviewStep:
    """
    Create an InterviewStep with the given duration and interviewers.

    Args:
        duration (float): The duration of the interview step.
        *interviewers (Engineer): Variable number of interviewers for this step.

    Returns:
        InterviewStep: A new InterviewStep instance.
    """
    return InterviewStep(duration=duration, interviewers=list(interviewers))


def create_interview(*steps: InterviewStep) -> Interview:
    """
    Create an Interview with the given steps.

    Args:
        *steps (InterviewStep): Variable number of InterviewStep instances.

    Returns:
        Interview: A new, validated Interview instance.

    Raises:
        ValueError: If the interview structure is invalid.
    """
    interview = Interview(steps=list(steps))
    interview.validate()
    return interview