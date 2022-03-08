from flask import request

from .tokenizer import Tokenizer


class WordFinder:
    def __init__(self, database):
        self.database = database
        self.tokenizer = Tokenizer()

    def highlight_words(self):
        # Check request body
        if not request.json:
            response = {
                'error': "json body not found in request",
                'status': 400
            }
            return response, 400

        if 'text' not in request.json:
            response = {
                'error': "key 'text' not found in request body",
                'status': 400
            }
            return response, 400

        # Process text
        tokenized = self.tokenizer.tokenize(request.json['text'])
        response = {
            'result': self._compare_words(tokenized),
            'status': 200
        }
        return response, 200

    def add_new_word(self):
        # Check request body
        if not request.json:
            response = {
                'error': "json body not found in request",
                'status': 400
            }
            return response, 400

        if 'word' not in request.json:
            response = {
                'error': "key 'word' not found in request body",
                'status': 400
            }
            return response, 400

        # Add new word to database
        lemmatized = ' '.join([self.tokenizer.lemmatize(word) for word in request.json['word'].split()])
        if lemmatized in self._load_words():
            response = {
                'error': "word already in database",
                'status': 406
            }
            return response, 406
        else:
            self.database.flaskdb.insert_one({'word': lemmatized})

            response = {
                'result': 'ok',
                'status': 200
            }
            return response, 200

    def get_all_words(self):
        response = {
            'result': self._load_words(),
            'status': 200
        }
        return response, 200

    def clear_all_words(self):
        self.database.flaskdb.drop()

        response = {
            'status': 200
        }
        return response, 200

    @staticmethod
    def request_not_found(_):
        response = {
            'error': "Request not found. Use one of: 'highlight-words', 'add-new-word', 'get-all-words'",
            'status': 404
        }
        return response, 404

    def _load_words(self):
        return [data['word'] for data in self.database.flaskdb.find()]

    def _compare_words(self, tokenized):
        words = self._load_words()
        result = {}
        for token in tokenized:
            if token.lemma in words:
                if token.lemma in result.keys():
                    result[token.lemma].append(token.position)
                else:
                    result[token.lemma] = [token.position]

        return result