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


def generate_candidates() -> Generator[Engineer, None, None]:
    """
    Generate an infinite stream of candidate Engineers.

    Yields:
        Engineer: A newly created Engineer instance representing a candidate.
    """
    while True:
        yield Engineer(EngineerParams())


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
    candidates = generate_candidates()
    for _ in range(settings.MAX_CANDIDATES_TO_CONSIDER):
        candidate = next(candidates)
        total_time, scores = pipeline(target_score, elimination_type, candidate)
        print(total_time, scores)
        final_score = scores[-1]["avg"] if scores else 0
        perceived_compensation = make_offer(int(candidate.skill_score_perceived), 0)
        print(
            f"""Final score: "{final_score} ", Perceived score: "{candidate.skill_score_perceived} ", Perceived_comp:"{perceived_compensation}, "Target Comp: "{target_compensation}"""
        )
        print()
        print()
        if (
            final_score >= target_score
            and perceived_compensation <= target_compensation
        ):
            return candidate, total_time, final_score
    return None, 0, 0
