"""Format Text Analyzer outputs."""
from flask import flash
from google.cloud import language_v1 as api


def format_analyzis(
    analyzis: api.ClassifyTextResponse,
    analyzis_type: str,
) -> None | str:
    """Format Text Analyzer outputs.

    Args:
        analyzis (api.ClassifyTextResponse): Analyzis outputs.
        analyzis_type (str): Analyzis type.

    Returns:
        str:
            Formatted Text Analyzer outputs.
    """

    if analyzis is not None:
        if analyzis_type == "classify_text" and len(analyzis.categories) != 0:
            return f"Text type: <b>{analyzis.categories[0].name[1:]}</b>"

    flash("Unable to classify this text.")
    return None
