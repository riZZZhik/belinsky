import os

from flask import Flask
from flask_pymongo import PyMongo

from word_finder import WordFinder


def create_app():
    """Create and configure an instance of the Flask application."""
    # Initialize Flask
    app = Flask("WordFinder")

    # Connect MongoDB
    app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + \
                              '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
    mongo = PyMongo(app, authSource="admin")

    # Initialize WordFinder
    word_finder = WordFinder(mongo.db)

    # Add handlers
    app.add_url_rule('/highlight-words', view_func=word_finder.highlight_words, methods=['POST'])
    app.add_url_rule('/add-new-word', view_func=word_finder.add_new_word, methods=['POST'])
    app.add_url_rule('/get-all-words', view_func=word_finder.get_all_words, methods=['GET'])
    app.add_url_rule('/clear-all-words', view_func=word_finder.clear_all_words, methods=['GET'])
    app.register_error_handler(404, word_finder.request_not_found)
    app.register_error_handler(500, word_finder.request_error)

    return app


# Run app
if __name__ == '__main__':
    APP_HOST = os.environ.get("APP_HOST", 'localhost')
    APP_PORT = os.environ.get("APP_PORT", 5000)
    APP_DEBUG = os.environ.get("APP_DEBUG", True)
    app = create_app()
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
