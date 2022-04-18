"""Belinsky exceptions."""
import typing as t

from .nlp_utils import format_language_name


class UnknownLanguageError(Exception):
    """Unknown language error."""

    def __init__(self, lang: str, known_langs: t.Iterable[str]):
        """Initialize an UnknownLanguageError.

        Args:
            lang (str): Language.
            known_langs (list): Known languages.
        """

        lang = format_language_name(lang)[0]
        known_langs = format_language_name(known_langs)
        self.message = (
            f"Unknown language: {lang}. Please use one of: {', '.join(known_langs)}."
        )
        super().__init__(self.message)
