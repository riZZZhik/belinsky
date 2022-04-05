from flask import Blueprint

from .phrase_comparer import PhraseComparer
from .phrase_finder import PhraseFinder


def create_blueprint_phrase_finder():
    # Create Flask blueprint
    phrase_finder_bp = Blueprint('phrase_finder', __name__)

    # Create PhraseFinder Worker
    worker = PhraseFinder()

    # Add request handlers
    phrase_finder_bp.add_url_rule('/find-phrases', view_func=worker.find_phrases, methods=['GET'])
    return phrase_finder_bp


__all__ = ['create_blueprint_phrase_finder', 'PhraseFinder', 'PhraseComparer']
