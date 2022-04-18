"""NLP utils"""
import typing as t

import iso639


def format_language_name(langs: str | t.Iterable) -> list:
    """Format a language name from iso639 to full.

    Args:
        langs (str or t.Iterable): Languages codes as ISO639.

    Returns:
        t.Iterable: Full languages names.
    """

    # Check input data
    if isinstance(langs, str):
        langs = [langs]

    # Format languages
    formatted_langs = []
    for lang in langs:
        try:
            formatted_langs.append(iso639.to_name(lang).split(';')[0])
        except iso639.NonExistentLanguageError:
            formatted_langs.append("Unknown")

    return sorted(formatted_langs)
