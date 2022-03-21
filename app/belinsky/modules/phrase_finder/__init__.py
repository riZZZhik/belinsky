from flask import Blueprint

from .phrase_comparer import PhraseComparer
from .phrase_finder import PhraseFinder


def create_blueprint_phrase_finder():
    # Create Flask blueprint
    phrase_finder_bp = Blueprint('phrase_finder', __name__)

    # Connect MongoDB
    worker = PhraseFinder()

    # Add request handlers
    phrase_finder_bp.add_url_rule('/find-phrases', view_func=worker.find_phrases, methods=['POST'])
    phrase_finder_bp.add_url_rule('/add-phrase', view_func=worker.add_phrase, methods=['POST'])
    phrase_finder_bp.add_url_rule('/get-known-phrases', view_func=worker.get_known_phrases, methods=['GET'])
    phrase_finder_bp.add_url_rule('/clear-known-phrases', view_func=worker.clear_known_phrases, methods=['POST'])

    return phrase_finder_bp


__all__ = ['create_blueprint_phrase_finder', 'PhraseFinder', 'PhraseComparer']
