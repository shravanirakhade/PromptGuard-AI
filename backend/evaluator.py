"""
PromptGuard AI - Advanced Response Evaluation Engine
"""


def evaluate_response(response, expected_keywords=None):

    # Check empty response
    if not response or not response.strip():
        return {
            "status": "FAIL",
            "score": 0,
            "feedback": ["Response is empty."],
            "metrics": {
                "word_count": 0,
                "character_count": 0,
                "matched_keywords": [],
                "missing_keywords": [],
                "final_score": 0
            }
        }

    score = 0
    feedback = []
    metrics = {}

    # 1. Response length analysis
    word_count = len(response.split())
    character_count = len(response)

    metrics["word_count"] = word_count
    metrics["character_count"] = character_count

    if word_count >= 10:
        score += 30
        feedback.append("Response length is acceptable.")
    else:
        feedback.append("Response is too short.")

    # 2. Keyword matching
    if expected_keywords:

        matched = [
            word for word in expected_keywords
            if word.lower() in response.lower()
        ]

        missing = [
            word for word in expected_keywords
            if word.lower() not in response.lower()
        ]

        keyword_score = int(
            (len(matched) / len(expected_keywords)) * 40
        )

        score += keyword_score

        metrics["matched_keywords"] = matched
        metrics["missing_keywords"] = missing

        feedback.append(f"Matched keywords: {matched}")

        if missing:
            feedback.append(f"Missing keywords: {missing}")

    else:
        score += 40
        metrics["matched_keywords"] = []
        metrics["missing_keywords"] = []

        feedback.append("Keyword check skipped.")

    # 3. Content quantity
    if word_count >= 20:
        score += 20
        feedback.append("Response has sufficient content.")
    else:
        feedback.append("Response needs more detailed content.")

    # 4. Basic readability
    if response.strip()[0].isupper():
        score += 10
        feedback.append("Response starts with a capital letter.")
    else:
        feedback.append("Response should start with a capital letter.")

    # 5. Final evaluation
    status = "PASS" if score >= 70 else "FAIL"

    metrics["final_score"] = score

    return {
        "status": status,
        "score": score,
        "feedback": feedback,
        "metrics": metrics
    }