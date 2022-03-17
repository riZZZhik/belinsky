from flask import Flask


def create_app():
    app = Flask("WordFinder")
    return app

