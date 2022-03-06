from flask import request


class WordFinder:
    def __init__(self):
        self.words = ['test', 'super_test']

    def highlight_words(self):
        response = {
            'error': "not implemented yet",
            'status': 501
        }
        return response

    def add_new_word(self):
        # Check api request
        if not request.json:
            response = {
                'error': "json body not found in request",
                'status': 400
            }
            return response

        if 'word' not in request.json:
            response = {
                'error': "key 'word' not found in request body",
                'status': 400
            }
            return response

        # Add new word to database
        self.words.append(request.json['word'])

        response = {
            'result': 'ok',
            'status': 200
        }
        return response

    def get_all_words(self):
        response = {
            'result': self.words,
            'status': 200
        }
        return response

    @staticmethod
    def request_not_found(_):
        response = {
            'error': "Request path not found. Use one of: 'highlight-words', 'add-new-word', 'get-all-words'",
            'status': 404
        }
        return response
