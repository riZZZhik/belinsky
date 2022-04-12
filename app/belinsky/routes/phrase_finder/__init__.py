"""Belinsky PhraseFinder blueprint."""
from flask import Blueprint

from .phrase_comparer import PhraseFinder
from .phrase_finder import PhraseFinderAPI


def create_blueprint_phrase_finder():
    """Create PhraseFinder blueprint."""
    # Create Flask blueprint
    phrase_finder_bp = Blueprint('phrase_finder', __name__)

    # Create PhraseFinder Worker
    worker = PhraseFinderAPI()

    # Add request handlers
    phrase_finder_bp.add_url_rule('/find-phrases', view_func=worker.find_phrases, methods=['GET'])
    return phrase_finder_bp


__all__ = ['create_blueprint_phrase_finder', 'PhraseFinderAPI', 'PhraseFinder']
