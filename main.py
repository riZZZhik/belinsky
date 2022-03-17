import os

from app import create_app

if __name__ == "__main__":
    app_host = os.environ.get("FLASK_RUN_HOST", 'localhost')
    app_port = int(os.environ.get("FLASK_RUN_PORT", '5000'))
    app_debug = os.environ.get("FLASK_APP_DEBUG", 'true').lower() in ('true', '1')

    app = create_app()
    app.run(host=app_host, port=app_port, debug=app_debug)
