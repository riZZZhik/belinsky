"""Belinsky PhraseFinder request worker."""
from flask import request
from flask_login import login_required
from prometheus_client import Summary

from .phrase_finder import PhraseFinder, UnknownLanguageError

# Initialize prometheus metrics
FIND_PHRASES_LATENCY = Summary('pf_find_phrases_latency', 'Latency of "find-phrases" request')


# pylint: disable=too-few-public-methods
class PhraseFinderAPI:
    """ PhraseFinder API worker."""

    def __init__(self):
        """Initialize Belinsky's Phrase Finder API worker."""
        self.comparer = PhraseFinder()

    @FIND_PHRASES_LATENCY.time()
    @login_required
    def find_phrases(self):
        """ Find known phrases in text.
        ---
        Body (JSON):
            - text (str): Text to be processed.
            - phrases (List[str]): Phrases to be found.
            - language (str): Language.

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
                'error': f"Required keys not found in request body :{', '.join(required_keys)}.",
                'status': 400
            }
            return response, 400

        # Process text
        try:
            lang = request.json['language'] if 'language' in request.json else None
            result = self.comparer.find_phrases(request.json['text'], request.json['phrases'], lang)
        except UnknownLanguageError as exception:
            response = {
                'error': str(exception),
                'status': 400
            }
            return response

        response = {
            'result': result,
            'status': 200
        }
        return response, 200
