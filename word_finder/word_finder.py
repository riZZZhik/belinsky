from flask import request
from pymystem3 import Mystem
from transliterate import translit


class Token:
    """Word token structure."""
    def __init__(self, word, lemma, position):
        self.word = word
        self.lemma = lemma
        self.position = position


class WordFinder:
    """ WordFinder API worker."""

    def __init__(self, database):
        """ Initialize WordFinder API worker.

        Arguments:
             database (flask_pymongo.wrappers.Database): MongoDB database connection.
        """

        self.database = database
        self.lemmatizer = Mystem()

    def add_new_word(self):
        """ Add new word or phrase to database.
        ---
        Body (JSON):
            - word: Word or phrase to add.

        Responses:
            200:
                description: Return that request processed properly.
                schema:
                    result: 'ok'.
                    status: 200
            400:
                description: Json body or 'word' key in request body not found.
                schema:
                    error: Error description.
                    status: 400
        """

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
        lemmatized = [self.lemmatize(word) for word in request.json['word'].split()]
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
        """ Get all known words in database.
        ---
        Responses:
            200:
                description: Return words and phrases from database.
                schema:
                    result: List of known words and phrases.
                    status: 200
        """

        response = {
            'result': [' '.join(x) for x in self._load_words()],
            'status': 200
        }
        return response, 200

    def highlight_words(self):
        """ Highlight known words in text.
        ---
        Body (JSON):
            - text: Text to process.

        Responses:
            200:
                description: Return highlighted words and their indexes in text.
                schema:
                    result: Dictionary with highlighted words and their indexes.
                    status: 200
            400:
                description: Json body or 'text' key in request body not found.
                schema:
                    error: Error description.
                    status: 400
            500:
                description: Unexpected error while processing request.
                schema:
                    error: Error description.
                    status: 500
        """

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
            tokenized = self.tokenize(request.json['text'])
            response = {
                'result': self._compare_words(tokenized),
                'status': 200
            }
            return response, 200
        except Exception as e:
            response = {
                'error': "unexpected error encountered during processing request: %s" % e,
                'status': 500
            }
            return response, 500

    def clear_all_words(self):
        """ Clear known words and phrases from database.
        ---
        Responses:
            200:
                description: Return that request processed properly.
                schema:
                    status: 200
        """

        self.database.flaskdb.drop()

        response = {
            'status': 200
        }
        return response, 200

    @staticmethod
    def request_not_found(_):
        """ Respond that request not found.
        ---
        Responses:
            404:
                description: Request not found.
                schema:
                    error: Error description.
                    status: 404
        """

        response = {
            'error': "Request not found. Use one of: "
                     "'highlight-words', 'add-new-word', 'get-all-words', 'clear-all-words'",
            'status': 404
        }
        return response, 404

    @staticmethod
    def request_error(_):
        """ Respond that there is unexpected error on server.
        ---
        Responses:
            500:
                description: Request not found.
                schema:
                    error: Error description.
                    status: 500
        """

        response = {
            'error': "unexpected error encountered during processing request",
            'status': 500
        }
        return response, 500

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

    def _load_words(self):
        """Load words and phrases from database."""
        return [data['word'] for data in self.database.flaskdb.find()]

    def _compare_words(self, tokenized):
        """ Compare text with words and phrases from database.

        Returns:
            Dict:
                Return highlighted words and their indexes in text.
        """

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
        """ Find indexes of sublist first items in list.

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
