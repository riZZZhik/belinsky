"""Belinsky TextAnalyzer blueprint."""
from flask import Blueprint, request, render_template, flash
from flask_login import login_required
from google.api_core import exceptions
from prometheus_client import Summary

from .formatter import format_analyzis
from .text_analyzer import TextAnalyzer
from ... import config

# Initialize prometheus metrics.
TEXT_ANALYZER_LATENCY = Summary(
    "text_analyzer_latency", 'Latency of "phrase-finder" request'
)

# Initialize TextAnalyzer worker.
text_analyzer_worker = TextAnalyzer(config.GOOGLE_CLOUD_CREDENTIALS)
available_analyzis = text_analyzer_worker.available_analyzis()


@TEXT_ANALYZER_LATENCY.time()
@login_required
def text_analyzer() -> str | tuple[dict[str, str | list | int], int]:
    """Generate Text Analyzer home page.

    Returns:
        str: HTML source of Text Analyzer page.
    """

    # Check request method
    if request.method == "GET":
        return render_template(
            "text_analyzer.html",
            analyzis=None,
            available_analyzis=available_analyzis.keys(),
        )

    # Process input data
    text = request.form.get("text")
    analyzis_type = available_analyzis[request.form.get("analyzis_type")]
    analyzis = None

    # Process text
    if not text:
        flash("No text given. Try again please.")
    else:
        try:
            analyzis = getattr(text_analyzer_worker, analyzis_type)(text)
            analyzis = format_analyzis(analyzis, analyzis_type)
        except exceptions.InvalidArgument as e:
            flash(f"Unknown language: {e.message[13:15]}.")

    # Response with raw data if required
    if request.form.get("raw"):
        response = {
            "text": text,
            "analyzis_type": analyzis_type,
            "analyzis_result": analyzis,
            "status": 200,
        }
        return response, 200

    return render_template(
        "text_analyzer.html",
        text=text,
        analyzis=analyzis,
        available_analyzis=available_analyzis.keys(),
    )


def create_blueprint_text_analyzer() -> Blueprint:
    """Create TextAnalyzer blueprint."""
    # Create Flask blueprint
    text_analyzer_bp = Blueprint(
        "text_analyzer", __name__, template_folder="../../templates"
    )

    # Add request handlers
    text_analyzer_bp.add_url_rule(
        "/text-analyzer", view_func=text_analyzer, methods=["GET", "POST"]
    )

    return text_analyzer_bp


__all__ = ["create_blueprint_text_analyzer", "TextAnalyzer"]
