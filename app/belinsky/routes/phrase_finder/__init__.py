"""Belinsky PhraseFinder blueprint."""
from flask import Blueprint
from flask import request
from flask_login import login_required
from prometheus_client import Summary

from .phrase_finder import PhraseFinder, UnknownLanguageError
from ..utils import check_request_keys

# Initialize prometheus metrics.
FIND_PHRASES_LATENCY = Summary('pf_find_phrases_latency', 'Latency of "find-phrases" request')

# Initialize PhraseFinder worker.
phrase_finder = PhraseFinder()


@FIND_PHRASES_LATENCY.time()
@login_required
def find_phrases() -> tuple[dict[str, str | int], int]:
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
    required_keys = {'text', 'phrases'}
    check = check_request_keys(required_keys)
    if check:
        return check

    # Process text
    try:
        lang = request.json['language'] if 'language' in request.json else None
        result = phrase_finder.find_phrases(request.json['text'], request.json['phrases'], lang)
    except UnknownLanguageError as exception:
        response = {
            'error': str(exception),
            'status': 400
        }
        return response, 400

    response = {
        'result': result,
        'status': 200
    }
    return response, 200


def create_blueprint_phrase_finder() -> Blueprint:
    """Create PhraseFinder blueprint."""
    # Create Flask blueprint
    phrase_finder_bp = Blueprint('phrase_finder', __name__)

    # Add request handlers
    phrase_finder_bp.add_url_rule('/find-phrases', view_func=find_phrases, methods=['GET'])
    return phrase_finder_bp


__all__ = ['create_blueprint_phrase_finder', 'PhraseFinder']
