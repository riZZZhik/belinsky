# System imports
import os

# Flask imports
from flask import Flask
from flask_pymongo import PyMongo

# Module imports
from .tokenizer import Tokenizer
from .word_finder import WordFinder


def create_app():
    # Initialize Flask
    app = Flask("WordFinder")

    # Connect MongoDB
    app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + \
                              '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
    mongo = PyMongo(app, authSource="admin")

    # Initialize WordFinder
    worker = WordFinder(mongo.db)

    # Add request handlers
    app.add_url_rule('/highlight-words', view_func=worker.highlight_words, methods=['POST'])
    app.add_url_rule('/add-new-word', view_func=worker.add_new_word, methods=['POST'])
    app.add_url_rule('/get-all-words', view_func=worker.get_all_words, methods=['GET'])
    app.add_url_rule('/clear-all-words', view_func=worker.clear_all_words, methods=['POST'])

    # Add error handlers
    app.register_error_handler(404, worker.request_not_found)
    app.register_error_handler(500, worker.request_error)

    return app


# Module names
__all__ = ['create_app', 'Tokenizer', 'WordFinder']
