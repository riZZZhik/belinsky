"""Test Belinsky Phrase Finder"""
from flask import Flask
from flask.testing import FlaskClient

from . import utils
from belinsky.routes.phrase_finder import phrase_finder_worker
from belinsky.routes.phrase_finder.phrase_finder import translit, Token


# Test Phrase Finder worker
def test_lemmatizer() -> None:
    """Test lemmatizer from Phrase Finder russian word."""
    response = phrase_finder_worker.lemmatize("Апельсины", "ru")
    correct_response = ["апельсин"]
    assert response == correct_response


def test_lemmatizer_hyphen() -> None:
    """Test lemmatizer from Phrase Finder with russian hyphened word."""
    response = phrase_finder_worker.lemmatize("по-любому", "ru")
    correct_response = ["любой"]
    assert response == correct_response


def test_lemmatizer_phrase() -> None:
    """Test lemmatizer from Phrase Finder with russian phrase."""
    response = phrase_finder_worker.lemmatize("а он обожает", "ru")
    correct_response = ["а", "он", "обожать"]
    assert response == correct_response


def test_lemmatizer_punctuation() -> None:
    """Test lemmatizer with from Phrase Finder russian phrase with punctuation."""
    response = phrase_finder_worker.lemmatize("а, -- [он], захочет?!", "ru")
    correct_response = ["а", "он", "захотеть"]
    assert response == correct_response


def test_lemmatizer_en() -> None:
    """Test lemmatizer from Phrase Finder with english word."""
    response = phrase_finder_worker.lemmatize("stunned", "en")
    correct_response = ["stun"]
    assert response == correct_response


def test_translit_ru() -> None:
    """Test lemmatizers with russian word using english translit."""
    response = translit("banan", "ru")
    correct_response = "банан"
    assert response == correct_response


def test_detect_language_ru() -> None:
    """Test detect language with russian phrase."""
    response = phrase_finder_worker.detect_language("Это русский текст")
    correct_response = "ru"
    assert response == correct_response


def test_detect_language_en() -> None:
    """Test detect language with english phrase."""
    response = phrase_finder_worker.detect_language("This is english text")
    correct_response = "en"
    assert response == correct_response


def test_tokenizer() -> None:
    """Test tokenizer from Phrase Finder."""
    response = [
        token.to_list()
        for token in phrase_finder_worker.tokenize("Мама обожает апельсины", "ru")
    ]
    correct_response = [
        Token("Мама", "мама", (0, 3)).to_list(),
        Token("обожает", "обожать", (5, 11)).to_list(),
        Token("апельсины", "апельсин", (13, 21)).to_list(),
    ]
    assert response == correct_response


def test_find_phrases() -> None:
    """Test find_phrases from Phrase Finder."""
    response = phrase_finder_worker.find_phrases("Привет, я Папа", ["я папа"], "ru")

    correct_response = {"я папа": [[8, 13]]}
    assert response == correct_response


# Test phrase finder
def test_phrase_finder_template(app: Flask, client: FlaskClient) -> None:
    """Test Phrase Finder template."""
    with utils.captured_templates(app) as templates:
        response = client.get("/phrase-finder")
        assert response.status_code == 200
        assert len(templates) == 1
        assert templates[0][0].name == "phrase_finder.html"


def test_phrase_finder_post(app: Flask, client: FlaskClient) -> None:
    """Test Phrase Finder with russian text."""
    with utils.captured_templates(app) as templates:
        response = client.post(
            "/phrase-finder",
            data={"text": "Клара у карла украла кораллы", "phrases": "коралл"},
        )
        assert response.status_code == 200
        assert len(templates) == 1
        assert "<b>кораллы</b>" in templates[0][1]["found_phrases"]


def test_phrase_finder_translit(client: FlaskClient) -> None:
    """Test Phrase Finder with russian text in english translit."""
    response = client.post(
        "/phrase-finder",
        data={
            "text": "маме и папе по bananu",
            "phrases": "бананы",
            "language": "ru",
            "raw": True,
        },
    )

    assert response.status_code == 200
    assert {"бананы": [[15, 20]]} == response.json["found_phrases"]


def test_phrase_finder_multiple_in_text(client: FlaskClient) -> None:
    """Test Phrase Finder with russian text and multiple phrases in text."""
    response = client.post(
        "/phrase-finder",
        data={"text": "Его мама любит любит апельсины", "phrases": "любить"},
    )

    assert response.status_code == 200
    assert "<b>любит</b> <b>любит</b>" in response.get_data(as_text=True)


def test_phrase_finder_multiple_phrases(client: FlaskClient) -> None:
    """Test Phrase Finder with russian text and multiple phrases in text."""
    response = client.post(
        "/phrase-finder",
        data={"text": "мама любит бананы", "phrases": "банан\r\nлюбит", "raw": True},
    )

    assert response.status_code == 200
    assert {"банан": [[11, 16]], "любит": [[5, 9]]} == response.json["found_phrases"]


def test_phrase_finder_hyphen(client: FlaskClient) -> None:
    """Test Phrase Finder with russian text and hyphened word."""
    response = client.post(
        "/phrase-finder",
        data={
            "text": "мама обожает по-любому тебя",
            "phrases": "обожает любой",
            "raw": True,
        },
    )

    assert response.status_code == 200
    assert {"обожает любой": [[5, 21]]} == response.json["found_phrases"]


def test_phrase_finder_de_without_preload(client: FlaskClient) -> None:
    """Test Phrase Finder with unknown language."""
    response = client.post(
        "/phrase-finder",
        data={
            "text": "Dies ist ein deutschland.",
            "phrases": "deutschland",
            "raw": True,
        },
    )

    assert response.status_code == 200
    assert {"deutschland": [[13, 23]]} == response.json["found_phrases"]


def test_phrase_finder_unknown_language(client: FlaskClient) -> None:
    """Test Phrase Finder with unknown language."""
    response = client.post(
        "/phrase-finder",
        data={"text": "Tai lietuviškas tekstas.", "phrases": ["tekstas"]},
    )

    assert response.status_code == 200
    assert "Unknown language" in response.get_data(as_text=True)
