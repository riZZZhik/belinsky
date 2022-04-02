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

    def lemmatize(self, word, language):
        """ Lemmatize word.

        Arguments:
             word (str): Word to be lemmatized.
             language (str): Language.

        Returns:
            str:
                Lemmatized word.
        """

        if language == 'ru':
            word = translit(word, 'ru')
            if '-' in word:
                return self.lemmatizers[language](self.lemmatizers[language](word)[-1].lemma_)[-1].lemma_
            else:
                return self.lemmatizers[language](word)[-1].lemma_
        elif language == 'en':
            return self.lemmatizers[language](word)[-1].lemma_
        else:
            raise ValueError('Invalid language: %s' % language)

    def tokenize(self, text, language):
        """ Tokenize text.

        Arguments:
            text (str): Text to be tokenized.
            language (str): Language.

        Returns:
            List:
                Words' tokens as 'phrase_comparer.Token' structure.
        """

        delta = 0
        tokenized = []
        text = translit(text.lower(), 'ru') if language == 'ru' else text
        for word in text.split():
            # Process word
            lemma = self.lemmatize(word, language)
            position = (delta, delta + len(word) - 1)
            delta += len(word) + 1

            # Create token from data
            tokenized.append(Token(word, lemma, position))

        return tokenized

    def compare_phrases(self, text, words, language):
        """ Compare text with known phrases.

        Arguments:
            text (str): Text to compare.
            words (list): List of words and phrases to compare with.
            language (str): Language.

        Returns:
            Dict:
                Return highlighted words and their indexes in text.
        """

        tokenized = self.tokenize(text, language)
        lemmatized = [x.lemma for x in tokenized]

        result = {}
        for word in words:
            for index in self._find_sublist_indexes(word, lemmatized):
                key = ' '.join(word)
                position = [tokenized[index].position[0], tokenized[index + len(word) - 1].position[1]]
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
