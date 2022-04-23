"""Test Belinsky Text Analyzer"""
from flask import Flask
from flask.testing import FlaskClient

from . import utils
from belinsky.routes.text_analyzer import TextAnalyzer, text_analyzer_worker

text = (
    "In spectra of the Active Galactic Nuclei (AGNs), the [N II]λλ 6548, 6583 Å lines are commonly "
    "fitted using the fixed intensity ratio of these two lines (R[NII] = I6583/I6548). However, the"
    " used values for fixed intensity ratio are slightly different through literature. There are "
    "several theoretical calculations of the transition probabilities which can be used for the "
    "line ratio estimation, but there are no experimental measurements of this ratio, since the "
    "[N II] lines are extremely weak in laboratory plasma. "
)
text_type = "Science"


# Test Text Analyzer worker
def test_classify_text() -> None:
    """Test classify_text from Text Analyzer."""
    response = text_analyzer_worker.classify_text(text).categories[0].name[1:]

    assert response == text_type


# Test Text Analyzer
def test_text_analyzer_template(app: Flask, client: FlaskClient) -> None:
    """Test Text Analyzer template."""
    with utils.captured_templates(app) as templates:
        response = client.get("/text-analyzer")
        assert response.status_code == 200
        assert len(templates) == 1
        assert templates[0][0].name == "text_analyzer.html"


def test_text_analyzer_post(app: Flask, client: FlaskClient) -> None:
    """Test Text Analyzer."""
    with utils.captured_templates(app) as templates:
        response = client.post(
            "/text-analyzer",
            data={"text": text, "analyzis_type": "Classify text"},
        )
        assert response.status_code == 200
        assert len(templates) == 1
        assert f"<b>{text_type}</b>" in templates[0][1]["analyzis"]
