from openbench.metrics import exact_match, normalize, token_f1

def test_normalize_case_and_whitespace():
    assert normalize("  HELLO   world ") == "hello world"

def test_exact_match():
    assert exact_match(" Paris ", "paris") == 1.0
    assert exact_match("Paris, France", "Paris") == 0.0

def test_token_f1():
    assert token_f1("red planet", "planet red") == 1.0
    assert token_f1("red planet", "blue moon") == 0.0
    assert token_f1("", "") == 1.0
