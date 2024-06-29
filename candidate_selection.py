"""
This module handles candidate generation and selection for the interview simulation project.

It provides functions to generate candidates and find suitable candidates based on
given criteria using an interview pipeline.
"""

from typing import Optional, Tuple, Generator
from engineer import Engineer, EngineerParams
from interview_pipeline import InterviewPipeline, EliminationType
from compensation import make_offer
from interview_config import settings


def generate_candidates(
    target_score: float, tolerance: float = 0.15
) -> Generator[Engineer, None, None]:
    """
    Generate a stream of candidate Engineers whose perceived skill score
    is within the tolerance range of their estimation of the target score.

    Args:
        target_score (float): The target skill score for the position.
        tolerance (float): The tolerance range for accepting a position, default is 0.15 (15%).

    Yields:
        Engineer: A newly created Engineer instance representing a candidate.
    """
    while True:
        candidate = Engineer(EngineerParams())
        estimated_target_score = candidate.estimate_skill_level(
            target_score,
            candidate.params.eval_error_std,
            candidate.params.eval_bias,
            settings.DEFAULT_SELF_ASSESSMENT_TIME,
        )
        lower_bound = estimated_target_score * (1 - tolerance)
        upper_bound = estimated_target_score * (1 + tolerance)

        if lower_bound <= candidate.skill_score_perceived <= upper_bound:
            yield candidate


def find_suitable_candidate(
    pipeline: InterviewPipeline,
    target_score: float,
    target_compensation: float,
    elimination_type: EliminationType,
) -> Tuple[Optional[Engineer], float, float]:
    """
    Find a suitable candidate using the given interview pipeline and criteria.

    This function generates candidates and runs them through the interview pipeline
    until a suitable candidate is found or the maximum number of candidates has been considered.

    Args:
        pipeline (InterviewPipeline): The interview pipeline to use for candidate evaluation.
        target_score (float): The minimum acceptable score for a candidate.
        target_compensation (float): The maximum acceptable compensation for a candidate.
        elimination_type (EliminationType): The type of elimination strategy to use in the pipeline.

    Returns:
        Tuple[Optional[Engineer], float, float]: A tuple containing:
            - The suitable candidate (or None if no suitable candidate was found)
            - The total interview time for the suitable candidate (or 0 if no suitable candidate)
            - The final score of the suitable candidate (or 0 if no suitable candidate)
    """
    # candidates = generate_candidates(target_score)
    # for _ in range(settings.MAX_CANDIDATES_TO_CONSIDER):
    #     candidate = next(candidates)
    #     total_time, scores = pipeline(target_score, elimination_type, candidate)
    #     print(total_time, scores)
    #     final_score = scores[-1]["avg"] if scores else 0
    #     perceived_compensation = make_offer(int(candidate.skill_score_perceived), 0)
    #     print(
    #         f"""Final score: "{final_score} ", Perceived score: "{candidate.skill_score_perceived} ", Perceived_comp:"{perceived_compensation}, "Target Comp: "{target_compensation}"""
    #     )
    #     print()
    #     print()
    #     if (
    #         final_score >= target_score
    #         and perceived_compensation <= target_compensation
    #     ):
    #         return candidate, total_time, final_score
    # return None, 0, 0
    candidates = generate_candidates(target_score)
    total_candidates_screened = 0
    for _ in range(settings.MAX_CANDIDATES_TO_CONSIDER):
        candidate = next(candidates)
        total_candidates_screened += 1
        total_time, scores = pipeline(target_score, elimination_type, candidate)
        final_score = scores[-1]["avg"] if scores else 0
        perceived_compensation = make_offer(int(final_score), 0)
        if (
            final_score >= target_score
            and perceived_compensation <= target_compensation
        ):
            return candidate, total_time, final_score, total_candidates_screened
    return None, 0, 0, total_candidates_screened