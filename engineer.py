"""
This module defines the Engineer model for the interview simulation project.

It includes the Engineer class that models the behavior of engineers in estimating
their own skills and the skills of others.
"""

from random import gauss
from pydantic import BaseModel, Field
from interview_config import settings
from random_generators import (
    generate_skill_score,
    generate_error_std,
    generate_bias,
)


class EngineerParams(BaseModel):
    """
    Pydantic model for Engineer parameters.

    This model defines the attributes of an engineer, including their true skill score,
    error standards, and biases for self-assessment and evaluation of others.
    """

    skill_score_true: int = Field(default_factory=generate_skill_score, ge=1, le=100)
    own_error_std: float = Field(default_factory=generate_error_std, ge=0)
    own_bias: float = Field(default_factory=generate_bias)
    eval_error_std: float = Field(default_factory=generate_error_std, ge=0)
    eval_bias: float = Field(default_factory=generate_bias)


class Engineer:
    """
    Represents an Engineer in the simulation.

    This class defines methods for skill estimation, both for self-assessment and evaluation of others.
    """

    def __init__(self, params: EngineerParams):
        """
        Initialize an Engineer instance.

        Args:
            params (EngineerParams): The parameters defining the engineer's attributes.
        """
        self.params = params
        self.skill_score_perceived = self.estimate_skill_level(
            self.params.skill_score_true,
            self.params.own_error_std,
            self.params.own_bias,
            settings.DEFAULT_SELF_ASSESSMENT_TIME,
        )

    def estimate_skill_level(
        self,
        skill_score: int,
        error_std: float,
        error_bias: float,
        interview_length: float,
    ) -> int:
        """
        Estimate a skill level given various parameters.

        This method applies error and bias to the true skill score, considering the interview length.

        Args:
            skill_score (int): The true skill score to estimate from.
            error_std (float): The standard deviation of the estimation error.
            error_bias (float): The bias in the estimation.
            interview_length (float): The length of the interview or assessment.

        Returns:
            int: The estimated skill level, bounded between 1 and 100.
        """
        interview_length = max(
            settings.MIN_INTERVIEW_LENGTH,
            min(settings.MAX_INTERVIEW_LENGTH, interview_length),
        )
        error = gauss(0, error_std / interview_length)
        estimated_score = skill_score + error + error_bias / interview_length
        return max(1, min(100, int(estimated_score)))

    def estimate_own_skill(
        self, interview_length: float = settings.DEFAULT_SELF_ASSESSMENT_TIME
    ) -> int:
        """
        Estimate the engineer's own skill level.

        Args:
            interview_length (float, optional): The length of self-reflection.
                Defaults to settings.DEFAULT_SELF_ASSESSMENT_TIME.

        Returns:
            int: The estimated own skill level.
        """
        return self.estimate_skill_level(
            self.params.skill_score_true,
            self.params.own_error_std,
            self.params.own_bias,
            interview_length,
        )

    def estimate_other_skill(
        self,
        other: "Engineer",
        interview_length: float = settings.DEFAULT_INTERVIEW_LENGTH,
    ) -> int:
        """
        Estimate another engineer's skill level.

        Args:
            other (Engineer): The engineer whose skill to estimate.
            interview_length (float, optional): The length of the interview.
                Defaults to settings.DEFAULT_INTERVIEW_LENGTH.

        Returns:
            int: The estimated skill level of the other engineer.
        """
        return self.estimate_skill_level(
            other.params.skill_score_true,
            self.params.eval_error_std,
            self.params.eval_bias,
            interview_length,
        )