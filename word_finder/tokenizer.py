from pymystem3 import Mystem
from transliterate import translit


class Token:
    """Word token structure."""
    def __init__(self, word, lemma, position):
        self.word = word
        self.lemma = lemma
        self.position = position


class Tokenizer:
    """Class for tokenizing words and phrases."""
    def __init__(self):
        """Initialize Tokenizer."""
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
                Words' tokens.
        """

        delta = 0
        tokenized = []
        for word in translit(text, 'ru').split():
            # Process word
            lemma = self.lemmatize(word)
            position = (delta, delta + len(word) - 1)
            delta += len(word) + 1

            # Create token from data
            tokenized.append(Token(word, lemma, position))

        return tokenized
