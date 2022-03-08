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
        words = self._load_words()
        tokenized = self.tokenizer.tokenize(request.json['text'])

        result = dict([(token['lemma'], token['position']) for token in tokenized if token['lemma'] in words])
        response = {
            'result': result,
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
        lemma = self.tokenizer.lemmatize(request.json['word'])
        if lemma in self._load_words():
            response = {
                'error': "word already in database",
                'status': 406
            }
            return response, 406
        else:
            self.database.flaskdb.insert_one({'word': lemma})

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

    @staticmethod
    def request_not_found(_):
        response = {
            'error': "Request not found. Use one of: 'highlight-words', 'add-new-word', 'get-all-words'",
            'status': 404
        }
        return response, 404

    def _load_words(self):
        return [data['word'] for data in self.database.flaskdb.find()]
