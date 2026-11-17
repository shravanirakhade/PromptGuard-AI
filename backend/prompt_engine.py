"""
PromptGuard AI - Advanced Prompt Processing Engine
"""


def validate_prompt(prompt):

    if not prompt or not prompt.strip():
        return False

    return True


def analyze_prompt(prompt):

    if not validate_prompt(prompt):
        return {
            "status": "FAIL",
            "score": 0,
            "feedback": ["Prompt cannot be empty."]
        }

    score = 0
    feedback = []

    word_count = len(prompt.split())

    # Check prompt length
    if word_count >= 10:
        score += 30
        feedback.append("Prompt length is good.")
    else:
        feedback.append("Prompt is too short. Add more details.")

    # Check instruction clarity
    clarity_words = [
        "explain", "describe", "write",
        "create", "compare", "analyze",
        "summarize", "develop", "calculate"
    ]

    if any(word in prompt.lower() for word in clarity_words):
        score += 30
        feedback.append("Clear instruction detected.")
    else:
        feedback.append("Add a clear instruction.")

    # Check context
    if word_count >= 20:
        score += 20
        feedback.append("Prompt provides sufficient context.")
    else:
        feedback.append("Consider adding more context.")

    # Check specific requirements
    requirement_words = [
        "example", "format", "steps",
        "points", "details", "beginner"
    ]

    if any(word in prompt.lower() for word in requirement_words):
        score += 20
        feedback.append("Specific requirements detected.")
    else:
        feedback.append("Add examples or specific requirements.")

    status = "PASS" if score >= 60 else "NEEDS IMPROVEMENT"

    return {
        "status": status,
        "score": score,
        "feedback": feedback,
        "word_count": word_count
    }


def improve_prompt(prompt):

    if not validate_prompt(prompt):
        raise ValueError("Prompt cannot be empty.")

    improved_prompt = (
        "Provide a clear, accurate, and detailed answer. "
        "Organize the response properly and include examples "
        "wherever useful.\n\n"
        f"User Request: {prompt.strip()}"
    )

    return improved_prompt


def generate_response(prompt):

    if not validate_prompt(prompt):
        raise ValueError("Prompt cannot be empty.")

    return (
        "Local Demo Response\n\n"
        f"You asked: {prompt.strip()}\n\n"
        "PromptGuard AI has successfully processed your prompt. "
        "This is a demonstration response generated locally "
        "without an external AI API."
    )