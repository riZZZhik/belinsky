import spacy
from transliterate import translit


class Token:
    """Word token structure."""

    def __init__(self, word, lemma, position):
        self.word = word
        self.lemma = lemma
        self.position = position

    def to_list(self):
        return self.word, self.lemma, self.position


class PhraseComparer:
    """Compare phrases"""

    def __init__(self):
        """Initialize class variables."""

        spacy_languages = {
            'ru': 'ru_core_news_sm',
            'en': 'en_core_web_sm'
        }
        self.lemmatizers = dict([(key, spacy.load(value, disable=['parser', 'ner']))
                                 for key, value in spacy_languages.items()])

    @staticmethod
    def _preprocess_text(text, language):
        if language == 'ru':
            # Transliterate ru language
            text = translit(text, 'ru')

            # Split hyphened words
            processed_text = []
            for word in text.split():
                if '-' in word and not all(symbol == '-' for symbol in word):
                    split = word.split('-')
                    word = " " * len("".join(split[:-1])) + ' ' + split[-1]

                processed_text.append(word)

            text = " ".join(processed_text)

        return text

    @staticmethod
    def _filter_spacy_tokens(tokens):
        filtered_tokens = [token for token in tokens
                           if not token.is_punct and not token.is_space and not token.is_quote and not token.is_bracket]
        return filtered_tokens

    def lemmatize(self, text, language):
        """ Lemmatize text.

        Arguments:
             text (str): Text to be lemmatized.
             language (str): Language.

        Returns:
            str:
                Lemmatized text.
        """

        # Lemmatize text using spaCy
        text = self._preprocess_text(text, language)
        tokens = self.lemmatizers[language](text)

        # Clear punctuation and other marks from text.
        tokens = self._filter_spacy_tokens(tokens)
        lemmatized = [token.lemma_ for token in tokens]

        return lemmatized

    def tokenize(self, text, language):
        """ Tokenize text.

        Arguments:
            text (str): Text to be tokenized.
            language (str): Language.

        Returns:
            List:
                Words' tokens as 'phrase_comparer.Token' structure.
        """

        # Translit text if ru language
        text = self._preprocess_text(text, language)

        # Generate spaCy tokens
        tokens = self._filter_spacy_tokens(self.lemmatizers[language](text))

        # Generate tokens from spaCy
        tokenized = [Token(token.text, token.lemma_, (token.idx, token.idx + len(token.text) - 1)) for token in tokens]

        return tokenized

    def compare_phrases(self, text, known_lemmas, language):
        """ Compare text with known phrases.

        Arguments:
            text (str): Text to compare.
            known_lemmas (list): List of known lemmas to compare with.
            language (str): Language.

        Returns:
            Dict:
                Return highlighted words and their indexes in text.
        """

        tokenized = self.tokenize(text, language)
        lemmatized = [x.lemma for x in tokenized]

        result = {}
        for known_lemma in known_lemmas:
            for index in self._find_sublist_indexes(known_lemma, lemmatized):
                key = ' '.join(known_lemma)
                position = [tokenized[index].position[0], tokenized[index + len(known_lemma) - 1].position[1]]
                if key in result.keys():
                    result[key].append(position)
                else:
                    result[key] = [position]

        return result

    @staticmethod
    def _find_sublist_indexes(sub, bigger):
        """ Find indexes of sublist first items in list.

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
                if not rest or bigger[pos:pos + len(rest)] == rest:
                    result.append(pos - 1)
        except ValueError:
            return result
