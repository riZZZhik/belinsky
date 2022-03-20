import os

from belinsky import create_app

app = create_app()

if __name__ == "__main__":
    app_host = os.environ.get("FLASK_RUN_HOST", 'localhost')
    app_port = int(os.environ.get("FLASK_RUN_PORT", '4958'))

    app = create_app()
    app.run(host=app_host, port=app_port)