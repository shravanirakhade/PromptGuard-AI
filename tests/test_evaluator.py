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
    assert result["score"] == 100


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
    assert result["score"] == 100