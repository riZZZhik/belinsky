from flask import request


class WordFinder:
    def __init__(self, database):
        self.database = database

    def highlight_words(self):
        response = {
            'error': "not implemented yet",
            'status': 501
        }
        return response, 501

    def add_new_word(self):
        # Check api request
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
        self._save_word(request.json['word'])

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
            'error': "Request path not found. Use one of: 'highlight-words', 'add-new-word', 'get-all-words'",
            'status': 404
        }
        return response, 404

    def _save_word(self, word):
        self.database.flaskdb.insert_one({'word': word})

    def _load_words(self):
        str([data['word'] for data in self.database.flaskdb.find()])
