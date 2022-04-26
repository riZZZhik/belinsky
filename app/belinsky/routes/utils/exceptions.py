"""Belinsky exceptions."""
import typing as t

from .nlp_utils import format_language_name


class UnknownLanguageError(Exception):
    """Unknown language error."""

    def __init__(self, language: str, known_languages: t.Iterable[str]):
        """Initialize an UnknownLanguageError.

        Args:
            language (str): Language.
            known_languages (list): Known languages.
        """

        self.language = format_language_name(language)[0]
        self.known_languages = format_language_name(known_languages)
        self.message = (
            f"Unknown language: {self.language}. "
            f"Please use one of: {', '.join(self.known_languages)}."
        )
        super().__init__(self.message)
