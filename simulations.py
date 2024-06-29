import random
from typing import List, Tuple
from engineer import Engineer, EngineerParams
from interview_pipeline import create_interview_pipeline, InterviewPipeline
from interview import create_interview_step
from candidate_selection import find_suitable_candidate
from interview_config import settings
from compensation import make_offer


def create_random_engineer() -> Engineer:
    return Engineer(EngineerParams())


def create_pipeline(
    structure: List[Tuple[int, float]], elimination_type: str
) -> InterviewPipeline:
    steps = []
    for num_engineers, duration in structure:
        interviewers = [create_random_engineer() for _ in range(num_engineers)]
        steps.append(create_interview_step(duration, *interviewers))
    return create_interview_pipeline(*steps)


def run_simulation(
    pipeline: InterviewPipeline,
    elimination_type: str,
    target_score: float,
    target_compensation: float,
) -> Tuple[float, float, int, int]:
    suitable_candidate, total_time, final_score, total_candidates_screened = (
        find_suitable_candidate(
            pipeline, target_score, target_compensation, elimination_type
        )
    )
    return (
        total_time,
        final_score,
        suitable_candidate.params.skill_score_true if suitable_candidate else 0,
        total_candidates_screened,
    )


def main(target_score=85, adjustement=0.0):
    pipelines = [
        ("pipeline1", [(1, 0.5), (1, 1.5)], "immediate"),
        ("pipeline2", [(1, 0.5), (1, 0.5), (1, 0.5), (1, 0.5), (3, 1.5)], "immediate"),
        ("pipeline3", [(1, 0.5), (1, 0.5), (1, 0.5), (1, 0.5), (3, 1.5)], "aggregate"),
        ("pipeline4", [(1, 0.25), (1, 0.5), (3, 1.5)], "immediate"),
    ]

    target_compensation = make_offer(target_score, adjustement)  # Adjust this value as needed

    results = {name: [] for name, _, _ in pipelines}

    for name, structure, elimination_type in pipelines:
        print(
            f"Running pipeline: {name}, structure: {structure}, elimination type: {elimination_type}"
        )
        for _ in range(100):  # Run 100 times
            pipeline = create_pipeline(structure, elimination_type)
            total_time, final_score, true_skill, candidates_screened = run_simulation(
                pipeline, elimination_type, target_score, target_compensation
            )
            results[name].append(
                (total_time, final_score, true_skill, candidates_screened)
            )

    # Print summary statistics
    for name, data in results.items():
        total_times, final_scores, true_skills, candidates_screened = zip(*data)
        successful_hires = sum(1 for score in final_scores if score >= target_score)
        fraction_above_target = successful_hires / len(final_scores)

        print(f"\n{name} Results:")
        print(f"Ttotal time: {sum(total_times):.2f}")
        print(f"Average total time: {sum(total_times) / len(total_times):.2f}")
        print(f"Average final score: {sum(final_scores) / len(final_scores):.2f}")
        print(f"Average true skill: {sum(true_skills) / len(true_skills):.2f}")
        print(f"Number of successful hires: {successful_hires}")
        print(f"Fraction of candidates above target score: {fraction_above_target:.2f}")
        print(
            f"Average candidates screened: {sum(candidates_screened) / len(candidates_screened):.2f}"
        )
        print(f"Total candidates screened: {sum(candidates_screened)}")


if __name__ == "__main__":
    main()