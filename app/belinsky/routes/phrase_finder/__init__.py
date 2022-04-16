"""Belinsky PhraseFinder blueprint."""
from flask import Blueprint, request, render_template, flash
from flask_login import login_required
from prometheus_client import Summary

from .formatter import bold_phrases
from .phrase_finder import PhraseFinder, UnknownLanguageError

# Initialize prometheus metrics.
FIND_PHRASES_LATENCY = Summary(
    "pf_find_phrases_latency", 'Latency of "find-phrases" request'
)

# Initialize PhraseFinder worker.
phrase_finder_worker = PhraseFinder()


@FIND_PHRASES_LATENCY.time()
@login_required
def phrase_finder():
    """Generate Phrase Finder home page.
    Returns:
        str: HTMl source of Phrase Finder page.
    """

    # Check request method
    if request.method == "GET":
        return render_template("phrase_finder.html", result=None)

    # Process text
    text = request.form.get("text")
    phrases = [p for p in request.form.get("phrases").split("\r\n") if p != ""]
    result = None

    if not text:
        flash("No text given. Try again please.")
    elif not phrases:
        flash("No phrases given. Try again please.")
    else:
        try:
            result = phrase_finder_worker.find_phrases(
                text, phrases, request.form.get("language")
            )
            result = bold_phrases(text, result)
        except UnknownLanguageError as exception:
            flash(str(exception))

    return render_template(
        "phrase_finder.html",
        result=result,
        text=text,
        phrases="\n".join(phrases),
    )


def create_blueprint_phrase_finder() -> Blueprint:
    """Create PhraseFinder blueprint."""
    # Create Flask blueprint
    phrase_finder_bp = Blueprint(
        "phrase_finder", __name__, template_folder="../../templates"
    )

    # Add request handlers
    phrase_finder_bp.add_url_rule(
        "/phrase-finder", view_func=phrase_finder, methods=["GET", "POST"]
    )
    return phrase_finder_bp


__all__ = ["create_blueprint_phrase_finder", "PhraseFinder"]
