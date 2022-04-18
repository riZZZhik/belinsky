"""Transliterate english symbols to Russian."""
import transliterate

from .exceptions import UnknownLanguageError


def translit(text: str, language: str) -> str:
    """Transliterate english symbols to Russian.

    Args:
        text (str): Text to be transliterated.
        language (str): Language to text be transliterated in.

    Returns:
        str: Transliterated text.
    """

    # Check input types.
    if not isinstance(text, str):
        raise TypeError(f"Unknown text type: {type(text)}. Required: str")
    if not isinstance(language, str):
        raise TypeError(f"Unknown text language: {type(language)}. Required: str")

    # Transliterate
    known_languages = ["ru"]
    if language == "ru":
        return transliterate.translit(text, language)

    raise UnknownLanguageError(language, known_languages)
