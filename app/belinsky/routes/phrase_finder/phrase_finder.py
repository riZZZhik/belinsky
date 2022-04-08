from flask import request
from flask_login import current_user, login_required
from prometheus_client import Summary

from .phrase_comparer import PhraseComparer

# Initialize prometheus metrics
FIND_PHRASES_LATENCY = Summary('pf_find_phrases_latency', 'Latency of "find-phrases" request')


class PhraseFinder:
    """ PhraseFinder API worker."""

    def __init__(self):
        """Initialize Belinsky's Phrase Finder API worker."""
        self.comparer = PhraseComparer()

    @FIND_PHRASES_LATENCY.time()
    @login_required
    def find_phrases(self):
        """ Find known phrases in text.
        ---
        Body (JSON):
            - text (str): Text to process.
            - phrases (list or tuple): Phrases to find.

        Responses:
            200:
                description: Return found phrases and their indexes in text.
                schema:
                    result: Dictionary with found phrases and their indexes.
                    status: 200
            400:
                description: Json body or 'text' key not found in request body.
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
                'error': "Json body not found in request",
                'status': 400
            }
            return response, 400

        required_keys = ['text', 'phrases']
        if not all(key in request.json for key in required_keys):
            response = {
                'error': "Required keys not found in request body :%s." % ', '.join(required_keys),
                'status': 400
            }
            return response, 400

        # Get text language
        if 'language' in request.json:
            language = request.json['language']
        else:
            language = self.comparer.detect_language(request.json['text'])

        known_languages = ['ru', 'en']
        if language not in known_languages:
            response = {
                'error': 'Unknown language: %s. Please use one of: %s.' %
                         (language, ", ".join(known_languages)),
                'status': 400
            }
            return response, 400

        # Process text
        response = {
            'result': self.comparer.find_phrases(request.json['text'],
                                                 request.json['phrases'],
                                                 language),
            'status': 200
        }
        return response, 200
