# Engineering Interview Simulator

## Overview

The Engineering Interview Simulator is a tool that models the software engineering hiring process. It aims to capture the complexities and unpredictable nature of real-world interviews.

## Core Components

### 1. Engineers (Candidates and Interviewers)

- Each engineer has a true skill score (1-100).
- Engineers estimate their own skills and others' skills with some error.
- Estimations are affected by personal biases and assessment duration.

### 2. Interview Process

- Interviews consist of multiple steps.
- Each step has a duration and one or more interviewers.
- Interviewers estimate the candidate's skill at each step.

### 3. Evaluation Strategies

- Immediate: Candidate fails if they perform poorly in any step.
- Aggregate: Candidate is evaluated based on average performance across all steps.

### 4. Compensation

- Skill scores are mapped to compensation offers.
- The system uses a piecewise linear function with diminishing returns for high scores.
- Final offers can be adjusted based on various factors.

## How It Works

1. The system creates a set of interviewers.
2. An interview pipeline is constructed with multiple steps.
3. The system generates candidates and runs them through the pipeline.
4. Candidates are evaluated based on their performance and expected compensation.
5. The process continues until a suitable candidate is found or the candidate pool is exhausted.

## Key Features

- Simulates variability in skill assessment due to biases and errors.
- Models the impact of interview duration on assessment accuracy.
- Allows exploration of different evaluation strategies.
- Considers both skill and compensation in candidate selection.

## Potential Insights

The simulator can help identify:

- The impact of interviewer biases on hiring decisions.
- The effectiveness of different interview structures and durations.
- The balance between skill requirements and compensation constraints.
- Potential improvements for real-world hiring practices.

## Configuration

The simulation can be customized by adjusting parameters such as:

- Compensation ranges
- Interview duration limits
- Maximum number of candidates to consider
- Interviewer attributes (bias, error rates)

By experimenting with these parameters, users can explore various hiring scenarios and their outcomes.