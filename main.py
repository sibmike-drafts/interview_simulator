from engineer import Engineer, EngineerParams
from interview_pipeline import create_interview_pipeline
from compensation import make_offer, map_skill_to_compensation
from candidate_selection import find_suitable_candidate
from interview import InterviewStep, create_interview_step


def main():
    # Create interviewers
    interviewer1 = Engineer(
        EngineerParams(skill_score_true=80, eval_error_std=10, eval_bias=-5)
    )
    interviewer2 = Engineer(
        EngineerParams(skill_score_true=75, eval_error_std=12, eval_bias=2)
    )
    interviewer3 = Engineer(
        EngineerParams(skill_score_true=85, eval_error_std=8, eval_bias=0)
    )
    interviewer4 = Engineer(
        EngineerParams(skill_score_true=70, eval_error_std=15, eval_bias=3)
    )

    # Set up the interview pipeline
    pipeline = create_interview_pipeline(
        create_interview_step(0.25, interviewer1),
        create_interview_step(0.5, interviewer2, interviewer3),
        create_interview_step(
            1.5, interviewer1, interviewer2, interviewer3, interviewer4
        ),
    )

    # Set target score and compensation
    target_score = 70
    target_compensation = make_offer(
        target_score, -0.1
    )  # 10% below the compensation for the target score
    elimination_type = "aggregate"

    # Find a suitable candidate
    suitable_candidate, interview_time, final_score = find_suitable_candidate(
        pipeline, target_score, target_compensation, elimination_type
    )

    if suitable_candidate:
        print("Suitable candidate found!")
        print(f"Candidate's true skill: {suitable_candidate.params.skill_score_true}")
        print(f"Interview time: {interview_time:.2f} hours")
        print(f"Final score: {final_score:.2f}")
        print(
            f"True compensation: ${map_skill_to_compensation(suitable_candidate.params.skill_score_true):.2f}"
        )
        print(f"Perceived compensation: ${make_offer(int(final_score), 0):.2f}")

        # Make an offer with an adjustment
        adjustment = 0.05  # 5% above the perceived compensation
        offer = make_offer(int(final_score), adjustment)
        print(f"Offer made: ${offer:.2f}")
    else:
        print("No suitable candidate found.")


if __name__ == "__main__":
    main()
