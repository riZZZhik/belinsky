from pymystem3 import Mystem
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
        self.lemmatizer = Mystem()

    def lemmatize(self, word):
        """ Lemmatize word.

        Arguments:
             word (str): Word to be lemmatized.

        Returns:
            str:
                Lemmatized word.
        """

        word = translit(word, 'ru')
        return self.lemmatizer.lemmatize(word)[-2]

    def tokenize(self, text):
        """ Tokenize text.

        Arguments:
            text (str): Text to be tokenized.

        Returns:
            List:
                Words' tokens as 'phrase_comparer.Token' structure.
        """

        delta = 0
        tokenized = []
        for word in translit(text.lower(), 'ru').split():
            # Process word
            lemma = self.lemmatize(word)
            position = (delta, delta + len(word) - 1)
            delta += len(word) + 1

            # Create token from data
            tokenized.append(Token(word, lemma, position))

        return tokenized

    def compare_words(self, text, words):
        """ Compare text with words and phrases.

        Arguments:
            text (str): Text to compare.
            words (list): List of words and phrases to compare with.

        Returns:
            Dict:
                Return highlighted words and their indexes in text.
        """

        tokenized = self.tokenize(text)
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
