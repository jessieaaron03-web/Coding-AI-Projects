from typing import Protocol

class ModelAdapter(Protocol):
    """Minimal interface implemented by a model or demo adapter."""
    name: str
    def generate(self, question: str) -> str:
        """Return a model response for the supplied question."""
        ...
