"""Belinsky configuration file."""
import json
import os
import secrets

# App config
SECRET_KEY = os.environ.get("BELINSKY_SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = secrets.token_hex(16)

MODULES = os.environ.get("BELINSKY_MODULES", "phrase_finder,text_analyzer").split(",")

# Modules config
# Text Analyzer
GOOGLE_CLOUD_CREDENTIALS = os.environ.get("BELINSKY_GOOGLE_CLOUD_CREDENTIALS")
if GOOGLE_CLOUD_CREDENTIALS:
    GOOGLE_CLOUD_CREDENTIALS = json.loads(GOOGLE_CLOUD_CREDENTIALS)
elif "text_analyzer" in MODULES:
    raise ValueError(
        'BELINSKY_GOOGLE_CLOUD_CREDENTIALS required for "text_analyzer" module, '
        "but not found in the environment."
    )

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
