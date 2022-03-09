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
        try:
            tokenized = self.tokenizer.tokenize(request.json['text'])
            response = {
                'result': self._compare_words(tokenized),
                'status': 200
            }
            return response, 200
        except Exception as e:
            response = {
                'error': "Unexpected error on server : %s" % e,
                'status': 500
            }
            return response, 500

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
        lemmatized = [self.tokenizer.lemmatize(word) for word in request.json['word'].split()]
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
            'result': [' '.join(x) for x in self._load_words()],
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
            'error': "Request not found. Use one of: "
                     "'highlight-words', 'add-new-word', 'get-all-words', 'clear-all-words'",
            'status': 404
        }
        return response, 404

    @staticmethod
    def request_error(_):
        response = {
            'error': "Unknown error encountered during processing request",
            'status': 500
        }
        return response, 500

    def _load_words(self):
        return [data['word'] for data in self.database.flaskdb.find()]

    def _compare_words(self, tokenized):
        words = self._load_words()
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
