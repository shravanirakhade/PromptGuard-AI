"""
PromptGuard AI - Response Evaluation Engine
"""


def evaluate_response(response, expected_keywords=None):

    if not response or not response.strip():
        return {
            "status": "FAIL",
            "score": 0,
            "feedback": ["Response is empty."]
        }

    score = 0
    feedback = []

    # Check response length
    if len(response.strip()) >= 50:
        score += 40
        feedback.append("Response length is acceptable.")
    else:
        feedback.append("Response is too short.")

    # Check expected keywords
    if expected_keywords:
        matched = [
            word for word in expected_keywords
            if word.lower() in response.lower()
        ]

        keyword_score = int(
            (len(matched) / len(expected_keywords)) * 40
        )

        score += keyword_score

        feedback.append(
            f"Matched keywords: {matched}"
        )

    else:
        score += 40
        feedback.append("Keyword check skipped.")

    # Check word count
    if len(response.split()) >= 10:
        score += 20
        feedback.append("Response contains sufficient words.")
    else:
        feedback.append("Response contains very few words.")

    # Final result
    status = "PASS" if score >= 70 else "FAIL"

    return {
        "status": status,
        "score": score,
        "feedback": feedback
    }