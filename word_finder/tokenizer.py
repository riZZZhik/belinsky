from pymystem3 import Mystem


class Tokenizer:
    def __init__(self):
        self.lemmatizer = Mystem()

    def lemmatize(self, word):
        return self.lemmatizer.lemmatize(word)[-2]

    def tokenize(self, text):
        delta = 0
        tokenized = []
        for word in text.split():
            # Check word
            if word is None:
                continue

            # Process word
            lemma = self.lemmatize(word)
            position = (delta, delta + len(word) - 1)
            delta += len(word) + 1

            # Create token from data
            token = {
                'word': word,
                'lemma': lemma,
                'position': position
            }
            tokenized.append(token)

        return tokenized
