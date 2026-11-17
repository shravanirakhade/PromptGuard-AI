from backend.prompt_engine import (
    validate_prompt,
    improve_prompt,
    generate_response
)


def test_valid_prompt():
    assert validate_prompt("Explain Python")


def test_empty_prompt():
    assert validate_prompt("") is False


def test_whitespace_prompt():
    assert validate_prompt("   ") is False


def test_improve_prompt():
    result = improve_prompt("Explain Python")

    assert "Explain Python" in result
    assert "clear" in result


def test_empty_prompt_raises_error():
    try:
        improve_prompt("")
        assert False
    except ValueError:
        assert True


def test_generate_response():
    result = generate_response("Explain Python")

    assert isinstance(result, str)
    assert "Local Demo Response" in result


def test_empty_response_raises_error():
    try:
        generate_response("")
        assert False
    except ValueError:
        assert True