import os

from word_finder import create_app

if __name__ == '__main__':
    APP_HOST = os.environ.get("FLASK_RUN_HOST", 'localhost')
    APP_PORT = int(os.environ.get("FLASK_RUN_PORT", '5000'))
    APP_DEBUG = os.environ.get("FLASK_APP_DEBUG", 'true').lower() in ('true', '1')

    app = create_app()
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
