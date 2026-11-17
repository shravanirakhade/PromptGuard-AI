from backend.evaluator import evaluate_response


def test_successful_evaluation():
    response = (
        "Python is a programming language used "
        "for software development and automation."
    )

    result = evaluate_response(
        response,
        ["Python", "programming"]
    )

    assert result["status"] == "PASS"
    assert result["score"] == 80
    assert result["metrics"]["word_count"] >= 10


def test_empty_response():
    result = evaluate_response("")

    assert result["status"] == "FAIL"
    assert result["score"] == 0


def test_missing_keywords():
    response = (
        "Python is useful for programming "
        "and building software applications."
    )

    result = evaluate_response(
        response,
        ["Java", "C++"]
    )

    assert result["status"] == "FAIL"
    assert result["metrics"]["missing_keywords"] == ["Java", "C++"]


def test_short_response():
    result = evaluate_response("Hello")

    assert result["status"] == "FAIL"


def test_keyword_check_skipped():
    response = (
        "Python is a programming language used "
        "for building software applications."
    )

    result = evaluate_response(response)

    assert result["status"] == "PASS"
    assert result["score"] == 80
    assert result["metrics"]["missing_keywords"] == []


def test_character_count():
    response = "Python is a programming language."

    result = evaluate_response(response)

    assert result["metrics"]["character_count"] == len(response)


def test_matched_keywords():
    response = (
        "Python is a programming language used "
        "for software development and automation."
    )

    result = evaluate_response(
        response,
        ["Python", "programming", "Java"]
    )

    assert "Python" in result["metrics"]["matched_keywords"]
    assert "Java" in result["metrics"]["missing_keywords"]


def test_response_starts_with_capital_letter():
    response = (
        "Python is a programming language used "
        "for software development and automation."
    )

    result = evaluate_response(response)

    assert result["score"] >= 70