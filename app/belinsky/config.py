"""Belinsky configuration file."""
import os
import secrets

# App config
SECRET_KEY = os.environ.get("BELINSKY_SECRET_KEY", secrets.token_hex(16))

MODULES = os.environ.get("BELINSKY_MODULES", "phrase_finder").split(",")


# Database config
if "BELINSKY_POSTGRES_URI" in os.environ:
    BELINSKY_POSTGRES_URI = os.environ["BELINSKY_POSTGRES_URI"]
else:
    user = os.environ.get("BELINSKY_POSTGRES_USER", "admin")
    password = os.environ.get("BELINSKY_POSTGRES_PASSWORD", "admin")
    host = os.environ.get("BELINSKY_POSTGRES_HOST", "localhost")
    port = os.environ.get("BELINSKY_POSTGRES_PORT", 5432)
    database = os.environ.get("BELINSKY_POSTGRES_DB", "belinsky_db")

    BELINSKY_POSTGRES_URI = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
