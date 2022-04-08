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

    def lemmatize(self, text, language):
        """ Lemmatize text.

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

    def tokenize(self, text, language):
        """ Tokenize text.

        Arguments:
            text (str): Text to be tokenized.
            language (str): Language.

        Returns:
            List:
                Words' tokens as 'phrase_comparer.Token' structure.
        """

        tokens = self._process_text(text, language)
        tokenized = [Token(token.text, token.lemma_, (token.idx, token.idx + len(token.text) - 1)) for token in tokens]

        return tokenized

    def find_phrases(self, text, phrases, language):
        """ Find phrases in text.

        Arguments:
            text (str): Text to find in.
            phrases (list): Phrases to be found.
            language (str): Language.

        Returns:
            Dict:
                Return phrases and their indexes in text.
        """

        tokenized = self.tokenize(text, language)
        lemmatized_text = [x.lemma for x in tokenized]

        result = {key: [] for key in phrases}
        for phrase in phrases:
            lemmatized_phrase = self.lemmatize(phrase, language)
            index_delta = len(lemmatized_phrase) - 1
            for index in self._find_sublist_indexes(lemmatized_phrase, lemmatized_text):
                position = [tokenized[index].position[0], tokenized[index + index_delta].position[1]]
                result[phrase].append(position)

        return result

    def _process_text(self, text, language):
        # Preprocess russian text
        if language == 'ru':
            # Transliterate ru language
            text = translit(text, 'ru')

            # Split hyphened words
            processed_text = []
            for word in text.split():
                if '-' in word and not all(symbol == '-' for symbol in word):
                    split = word.split('-')
                    word = ' ' * len(''.join(split[:-1])) + ' ' + split[-1]

                processed_text.append(word)

            text = ' '.join(processed_text)

        # Get tokens from spaCy
        tokens = self.lemmatizers[language](text)

        # Clean tokens
        tokens = [token for token in tokens
                  if not token.is_punct and not token.is_space and not token.is_quote and not token.is_bracket]

        return tokens

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
