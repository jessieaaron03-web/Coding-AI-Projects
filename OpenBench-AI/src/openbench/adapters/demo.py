class DemoAdapter:
    """Deterministic, provider-free adapter for exercising the evaluation pipeline."""
    name = "demo"
    _answers = {
        "what is the capital of france?": "Paris",
        "which planet is known as the red planet?": "Mars",
        "what is the chemical formula for water?": "H2O",
        "what is the largest ocean on earth?": "Pacific Ocean",
        "what kind of programming language is python?": "A programming language",
    }
    def generate(self, question: str) -> str:
        return self._answers.get(question.strip().lower(), "I do not know.")
