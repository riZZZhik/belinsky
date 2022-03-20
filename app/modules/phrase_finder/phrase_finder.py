from flask import request
from prometheus_client import Counter, Summary
from pymongo import MongoClient

from .phrase_comparer import PhraseComparer

ADD_PHRASE_LATENCY = Summary('pf_add_phrase_latency', 'Latency of "add-phrase" request')
GET_KNOWN_PHRASES_LATENCY = Summary('pf_get_known_phrases_latency', 'Latency of "get-known-phrases" request')
CLEAR_KNOWN_PHRASES_LATENCY = Summary('pf_clear_known_phrases_latency', 'Latency of "clear-known-phrases" request')
FIND_PHRASES_LATENCY = Summary('pf_find_phrases_latency', 'Latency of "find-phrases" request')

ERROR_500_COUNTER = Counter('pf_500_error_counter', 'Counter of 500 errors')


class PhraseFinder:
    """ PhraseFinder API worker."""

    def __init__(self, mongo_uri):
        """ Initialize WordFinder API worker.

        Arguments:
             mongo_uri (str): MongoDB URI.
        """

        self.database = MongoClient(mongo_uri).db.word_finder_db
        self.comparer = PhraseComparer()

    @ADD_PHRASE_LATENCY.time()
    def add_phrase(self):
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
            406:
                description: Word already in database.
                schema:
                    error: Error description.
                    status: 406
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
        lemmatized = [self.comparer.lemmatize(word) for word in request.json['word'].split()]
        if lemmatized in self._load_words():
            response = {
                'error': "word already in database",
                'status': 406
            }
            return response, 406
        else:
            self.database.insert_one({'word': lemmatized})

            response = {
                'result': 'ok',
                'status': 200
            }
            return response, 200

    @GET_KNOWN_PHRASES_LATENCY.time()
    def get_known_phrases(self):
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

    @CLEAR_KNOWN_PHRASES_LATENCY.time()
    def clear_known_phrases(self):
        """ Clear known words and phrases from database.
        ---
        Responses:
            200:
                description: Return that request processed properly.
                schema:
                    status: 200
        """

        self.database.drop()

        response = {
            'status': 200
        }
        return response, 200

    @FIND_PHRASES_LATENCY.time()
    def find_phrases(self):
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
        response = {
            'result': self.comparer.compare_words(request.json['text'], self._load_words()),
            'status': 200
        }
        return response, 200

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

        ERROR_500_COUNTER.inc()
        response = {
            'error': "unexpected error encountered during PhraseFinder processing",
            'status': 500
        }
        return response, 500

    def _load_words(self):
        """ Load words and phrases from database.

        Returns:
            List: Word and phrases in database.
        """

        return [data['word'] for data in self.database.find()]
