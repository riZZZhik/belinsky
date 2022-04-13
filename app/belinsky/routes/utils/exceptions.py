"""Belinsky exceptions."""
from typing import Iterable


class UnknownLanguageError(Exception):
    """Unknown language error."""
    def __init__(self, lang: str, known_langs: Iterable[str]):
        self.lang = lang
        self.message = f"Unknown language: {lang}. Please use one of: {', '.join(known_langs)}."
        super().__init__(self.message)
