import transliterate

from .exceptions import UnknownLanguageError


def translit(text, language):
    known_languages = ['ru']
    if language == 'ru':
        return transliterate.translit(text, language)
    else:
        raise UnknownLanguageError(language, known_languages)
