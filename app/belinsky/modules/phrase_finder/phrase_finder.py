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
        """ Initialize Belinsky's Phrase Finder API worker.

        Arguments:
             mongo_uri (str): MongoDB URI.
        """

        self.database = MongoClient(mongo_uri).db.belinsky_db
        self.comparer = PhraseComparer()

    @ADD_PHRASE_LATENCY.time()
    def add_phrase(self):
        """ Add new phrase to database.
        ---
        Body (JSON):
            - phrase: Phrase to add.

        Responses:
            200:
                description: Return that request processed properly.
                schema:
                    result: 'ok'.
                    status: 200
            400:
                description: Json body or 'phrase' key in request body not found.
                schema:
                    error: Error description.
                    status: 400
            406:
                description: Phrase already in database.
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

        if 'phrase' not in request.json:
            response = {
                'error': "key 'phrase' not found in request body",
                'status': 400
            }
            return response, 400

        # Check if phrase already exists
        lemmatized = [self.comparer.lemmatize(phrase) for phrase in request.json['phrase'].split()]
        if lemmatized in self._load_phrases():
            response = {
                'error': "phrase already in database",
                'status': 406
            }
            return response, 406

        # Add phrase to dataset
        self.database.insert_one({'phrase': lemmatized})

        response = {
            'result': 'ok',
            'status': 200
        }
        return response, 200

    @GET_KNOWN_PHRASES_LATENCY.time()
    def get_known_phrases(self):
        """ Get all known phrases from database.
        ---
        Responses:
            200:
                description: Return phrases from database.
                schema:
                    result: List of known phrases.
                    status: 200
        """

        response = {
            'result': [' '.join(x) for x in self._load_phrases()],
            'status': 200
        }
        return response, 200

    @CLEAR_KNOWN_PHRASES_LATENCY.time()
    def clear_known_phrases(self):
        """ Clear known phrases from database.
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
        """ Find known phrases in text.
        ---
        Body (JSON):
            - text: Text to process.

        Responses:
            200:
                description: Return found phrases and their indexes in text.
                schema:
                    result: Dictionary with found phrases and their indexes.
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
            'result': self.comparer.compare_phrases(request.json['text'], self._load_phrases()),
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

    def _load_phrases(self):
        """ Load phrases from database.

        Returns:
            List: Phrases in database.
        """

        return [data['phrase'] for data in self.database.find()]