"""Belinsky exceptions."""


class UnknownLanguageError(Exception):
    """Unknown language error."""
    def __init__(self, lang, known_langs):
        self.lang = lang
        self.message = f"Unknown language: {lang}. Please use one of: {', '.join(known_langs)}."
        super().__init__(self.message)
