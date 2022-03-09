from pymystem3 import Mystem


class Token:
    def __init__(self, word, lemma, position):
        self.word = word
        self.lemma = lemma
        self.position = position


class Tokenizer:
    def __init__(self):
        self.lemmatizer = Mystem()

    def lemmatize(self, word):
        return self.lemmatizer.lemmatize(word)[-2]

    def tokenize(self, text):
        delta = 0
        tokenized = []
        for word in text.split():
            # Process word
            lemma = self.lemmatize(word)
            position = (delta, delta + len(word) - 1)
            delta += len(word) + 1

            # Create token from data
            tokenized.append(Token(word, lemma, position))

        return tokenized
