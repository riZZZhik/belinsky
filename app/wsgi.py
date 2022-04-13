"""Belinsky configuration for WSGI application."""
from belinsky import create_app

app = create_app()


def main() -> None:
    """Run Belinsky application."""
    app.run(host='localhost', port=4958)


if __name__ == "__main__":
    main()
