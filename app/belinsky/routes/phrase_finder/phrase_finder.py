"""Belinsky PhraseFinder nlp worker."""
from dataclasses import dataclass
from typing import Any, Sequence

import spacy
from spacy_langdetect import LanguageDetector

from ..utils import UnknownLanguageError, translit


@dataclass(slots=True, frozen=True)
class Token:
    """Word token structure."""

    word: str
    lemma: str
    position: Sequence[int]

    def to_list(self):
        """Convert token structure to list of values."""
        return self.word, self.lemma, self.position


class PhraseFinder:
    """Compare phrases"""

    def __init__(self):
        """Initialize class variables."""

        # Initialize spaCy
        spacy_languages = {"en": "en_core_web_sm", "ru": "ru_core_news_sm"}
        self.lemmatizers = {
            lang: spacy.load(model_name, disable=["parser", "ner"])
            for lang, model_name in spacy_languages.items()
        }

        # Initialize spaCy language detector
        spacy.Language.factory(
            "language_detector", func=lambda nlp, name: LanguageDetector()
        )
        self.lemmatizers["en"].add_pipe("sentencizer")
        self.lemmatizers["en"].add_pipe("language_detector", last=True)

    # pylint: disable=fixme
    def detect_language(self, text: str) -> str:
        """Detect text language

        Args:
            text (str): Text to be processed.

        Returns:
            str:
                Language code as https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes.
        """

        # TODO: Split text into sentences.
        tokens = self.lemmatizers["en"](text)
        language = tokens._.language["language"]
        return language

    def lemmatize(self, text: str, language: str) -> list[str]:
        """Lemmatize text.

        Arguments:
             text (str): Text to be lemmatized.
             language (str): Language.

        Returns:
            list:
                Lemmatized text.
        """

        tokens = self._process_text(text, language)
        lemmatized = [token.lemma_ for token in tokens]

        return lemmatized

    def tokenize(self, text: str, language: str) -> list[Token]:
        """Tokenize text.

        Arguments:
            text (str): Text to be tokenized.
            language (str): Language.

        Returns:
            List:
                Words' tokens as 'phrase_comparer.Token' structure.
        """

        tokens = self._process_text(text, language)
        tokenized = [
            Token(
                token.text, token.lemma_, (token.idx, token.idx + len(token.text) - 1)
            )
            for token in tokens
        ]

        return tokenized

    def find_phrases(
        self, text: str, phrases: Sequence[str], lang: str
    ) -> dict[str, list[int]]:
        """Find phrases in text.

        Arguments:
            text (str): Text to be processed.
            phrases (list): Phrases to be found.
            lang (str): Language.

        Returns:
            Dict:
                Return phrases and their indexes in text.
        """

        # Detect language
        if lang is None:
            lang = self.detect_language(text)

        if lang not in self.lemmatizers:
            raise UnknownLanguageError(lang, self.lemmatizers.keys())

        # Find phrases
        tokenized = self.tokenize(text, lang)
        lemmatized_text = [x.lemma for x in tokenized]

        result = {key: [] for key in phrases}
        for phrase in phrases:
            lemmatized_phrase = self.lemmatize(phrase, lang)
            index_delta = len(lemmatized_phrase) - 1
            for index in self._find_sublist_indexes(lemmatized_phrase, lemmatized_text):
                position = [
                    tokenized[index].position[0],
                    tokenized[index + index_delta].position[1],
                ]
                result[phrase].append(position)

        return result

    def _process_text(self, text: str, language: str) -> list:
        # Preprocess russian text
        if language == "ru":
            # Transliterate ru language
            text = translit(text, "ru")

            # Split hyphened words
            processed_text = []
            for word in text.split():
                if "-" in word and not all(symbol == "-" for symbol in word):
                    split = word.split("-")
                    word = " " * len("".join(split[:-1])) + " " + split[-1]

                processed_text.append(word)

            text = " ".join(processed_text)

        # Get tokens from spaCy
        tokens = self.lemmatizers[language](text)

        # Clean tokens
        to_check = (
            "is_punct",
            "is_left_punct",
            "is_right_punct",
            "is_space",
            "is_quote",
            "is_bracket",
        )
        tokens = [
            token
            for token in tokens
            if all(not getattr(token, attr) for attr in to_check)
        ]

        return tokens

    @staticmethod
    def _find_sublist_indexes(sub: Sequence[Any], bigger: Sequence[Any]) -> list[int]:
        """Find indexes of sublist first items in list.

        Arguments:
            sub (list): Sublist to find in main list.
            bigger (list): Main list.

        Returns:
            List:
                Indexes of sublist first items in list.
        """

        first, rest = sub[0], sub[1:]
        pos = 0
        result = []
        try:
            while True:
                pos = bigger.index(first, pos) + 1
                if not rest or bigger[pos : pos + len(rest)] == rest:
                    result.append(pos - 1)
        except ValueError:
            return result
