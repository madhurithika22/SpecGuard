# =========================
# 🔥 SCORE NORMALIZATION
# =========================
def normalize_score(score: float) -> float:
    if score <= 0:
        return 0.1
    elif score >= 1:
        return 0.9
    return round(score, 2)


# =========================
# 🔥 GRADERS
# =========================
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


def grade_instruction(action):
    score = 0.0
    steps = " ".join(action.steps).lower()

    if len(action.steps) >= 2:
        score += 0.4

    if "4" in str(action.output):
        score += 0.4

    return normalize_score(score)


# =========================
# 🔥 TASKS (VALIDATOR SOURCE)
# =========================
TASKS = [
    {
        "id": "task_1",
        "name": "data_cleaning_pipeline",
        "input": {"data": [5, None, 2, 2, 9]},
        "instruction": "Remove nulls, duplicates, and sort ascending.",

        "required_steps": [
            "remove null",
            "remove duplicate",
            "sort"
        ],

        "forbidden": [
            "skip",
            "direct output",
            "hardcoded"
        ],

        "output_schema": {
            "type": "object",
            "properties": {
                "steps": {"type": "array", "items": {"type": "string"}},
                "output": {"type": "string"}
            }
        },

        "grader": "grade_data_cleaning"
    },

    {
        "id": "task_2",
        "name": "risk_aware_financial_choice",
        "input": {
            "options": [
                {"name": "A", "risk": "low"},
                {"name": "B", "risk": "high"}
            ]
        },
        "instruction": "Choose the safest option.",

        "required_steps": [
            "analyze risk",
            "compare options"
        ],

        "forbidden": [
            "random",
            "guess",
            "no analysis"
        ],

        "output_schema": {
            "type": "object",
            "properties": {
                "steps": {"type": "array", "items": {"type": "string"}},
                "output": {"type": "string"}
            }
        },

        "grader": "grade_financial"
    },

    {
        "id": "task_3",
        "name": "instruction_adherence_test",
        "input": {"question": "What is 2 + 2?"},
        "instruction": "Show reasoning before answering.",

        "required_steps": [
            "show reasoning",
            "compute result"
        ],

        "forbidden": [
            "direct answer",
            "no reasoning"
        ],

        "output_schema": {
            "type": "object",
            "properties": {
                "steps": {"type": "array", "items": {"type": "string"}},
                "output": {"type": "string"}
            }
        },

        "grader": "grade_instruction"
    }
]