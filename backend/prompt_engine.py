"""
PromptGuard AI - Prompt Processing Engine
"""


def validate_prompt(prompt):
    """Check whether the prompt is valid."""

    if not prompt or not prompt.strip():
        return False

    return True


def improve_prompt(prompt):
    """Improve the structure of a user prompt."""

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
    """Generate a local demo response without an API key."""

    if not validate_prompt(prompt):
        raise ValueError("Prompt cannot be empty.")

    return (
        "Local Demo Response\n\n"
        f"You asked: {prompt.strip()}\n\n"
        "PromptGuard AI has successfully processed your prompt. "
        "This is a demonstration response generated locally "
        "without an external AI API."
    )