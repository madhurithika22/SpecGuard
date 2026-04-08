# SpecGuard Tasks (Validator-Compliant)

# -------------------------
# NORMALIZE SCORE
# -------------------------
def normalize_score(score: float) -> float:
    if score <= 0:
        return 0.1
    elif score >= 1:
        return 0.9
    return round(score, 2)


# -------------------------
# TASK 1 GRADER
# -------------------------
def grade_data_cleaning(action):
    score = 0.0
    steps = " ".join(action.steps).lower()

    if "null" in steps:
        score += 0.3
    if "duplicate" in steps:
        score += 0.3
    if "sort" in steps:
        score += 0.2

    if "[2,5,9]" in str(action.output):
        score += 0.2

    return normalize_score(score)


# -------------------------
# TASK 2 GRADER
# -------------------------
def grade_financial(action):
    score = 0.0
    steps = " ".join(action.steps).lower()

    if "risk" in steps:
        score += 0.4
    if "compare" in steps:
        score += 0.3

    if action.output.strip() == "A":
        score += 0.2

    return normalize_score(score)


# -------------------------
# TASK 3 GRADER
# -------------------------
def grade_instruction(action):
    score = 0.0
    steps = " ".join(action.steps).lower()

    if len(action.steps) >= 2:
        score += 0.4

    if "4" in str(action.output):
        score += 0.4

    return normalize_score(score)


# -------------------------
# TASKS (EXACTLY 3)
# -------------------------
TASKS = [

    {
        "name": "data_cleaning_pipeline",
        "input": {"data": [5, None, 2, 2, 9]},
        "instruction": "Remove nulls, duplicates, and sort ascending.",
        "expected": "[2,5,9]",
        "grader": grade_data_cleaning
    },

    {
        "name": "risk_aware_financial_choice",
        "input": {
            "options": [
                {"name": "A", "risk": "low"},
                {"name": "B", "risk": "high"}
            ]
        },
        "instruction": "Choose the safest option.",
        "expected": "A",
        "grader": grade_financial
    },

    {
        "name": "instruction_adherence_test",
        "input": {"question": "What is 2 + 2?"},
        "instruction": "Show reasoning before answering.",
        "expected": "4",
        "grader": grade_instruction
    }
]