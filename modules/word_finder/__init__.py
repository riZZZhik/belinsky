import os

from flask import Blueprint

from .tokenizer import Tokenizer
from .word_finder import WordFinder


def create_blueprint():
    # Create Flask blueprint
    word_finder_bp = Blueprint('word_finder', __name__)

    # Connect MongoDB
    mongo_uri = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + \
                '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/'
    worker = WordFinder(mongo_uri)

    # Add request handlers
    word_finder_bp.add_url_rule('/highlight-words', view_func=worker.highlight_words, methods=['POST'])
    word_finder_bp.add_url_rule('/add-new-word', view_func=worker.add_new_word, methods=['POST'])
    word_finder_bp.add_url_rule('/get-all-words', view_func=worker.get_all_words, methods=['GET'])
    word_finder_bp.add_url_rule('/clear-all-words', view_func=worker.clear_all_words, methods=['POST'])

    # Add error handlers
    word_finder_bp.register_error_handler(404, worker.request_not_found)
    word_finder_bp.register_error_handler(500, worker.request_error)

    return word_finder_bp


__all__ = ['create_blueprint', 'WordFinder', 'Tokenizer']
