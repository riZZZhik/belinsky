"""Test Belinsky Phrase Finder"""
from flask import Flask
from flask.testing import FlaskClient

from . import utils
from belinsky.routes.phrase_finder.phrase_finder import PhraseFinder, translit, Token

comparer = PhraseFinder()


def test_lemmatizer() -> None:
    """Test lemmatizer russian word."""
    response = comparer.lemmatize("Апельсины", "ru")
    correct_response = ["апельсин"]
    assert response == correct_response


def test_lemmatizer_hyphen() -> None:
    """Test lemmatizer with russian hyphened word."""
    response = comparer.lemmatize("по-любому", "ru")
    correct_response = ["любой"]
    assert response == correct_response


def test_lemmatizer_phrase() -> None:
    """Test lemmatizer with russian phrase."""
    response = comparer.lemmatize("а он обожает", "ru")
    correct_response = ["а", "он", "обожать"]
    assert response == correct_response


def test_lemmatizer_punctuation() -> None:
    """Test lemmatizer with russian phrase with punctuation."""
    response = comparer.lemmatize("а, -- [он], захочет?!", "ru")
    correct_response = ["а", "он", "захотеть"]
    assert response == correct_response


def test_lemmatizer_en() -> None:
    """Test lemmatizer with english word."""
    response = comparer.lemmatize("stunned", "en")
    correct_response = ["stun"]
    assert response == correct_response


def test_translit_ru() -> None:
    """Test lemmatizers with russian word using english translit."""
    response = translit("banan", "ru")
    correct_response = "банан"
    assert response == correct_response


def test_detect_language_ru() -> None:
    """Test detect language with russian phrase."""
    response = comparer.detect_language("Это русский текст")
    correct_response = "ru"
    assert response == correct_response


def test_detect_language_en() -> None:
    """Test detect language with english phrase."""
    response = comparer.detect_language("This is english text")
    correct_response = "en"
    assert response == correct_response


def test_tokenizer() -> None:
    """Test tokenizer from PhraseFinder."""
    response = [
        token.to_list() for token in comparer.tokenize("Мама обожает апельсины", "ru")
    ]
    correct_response = [
        Token("Мама", "мама", (0, 3)).to_list(),
        Token("обожает", "обожать", (5, 11)).to_list(),
        Token("апельсины", "апельсин", (13, 21)).to_list(),
    ]
    assert response == correct_response


def test_compare_phrases() -> None:
    """Test compare phrases from PhraseFinder."""
    response = comparer.find_phrases("Привет, я Папа", ["я папа"], "ru")

    correct_response = {"я папа": [[8, 13]]}
    assert response == correct_response


# Test phrase finder
def test_find_phrase_template(app: Flask, client: FlaskClient) -> None:
    """Test find phrase method."""
    with utils.captured_templates(app) as templates:
        response = client.get("/phrase-finder")
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == "phrase_finder.html"


def test_find_phrase_post(app: Flask, client: FlaskClient) -> None:
    """Test find phrase method with russian text."""
    with utils.captured_templates(app) as templates:
        response = client.post(
            "/phrase-finder",
            data={"text": "Клара у карла украла кораллы", "phrases": "коралл"},
        )
        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == "phrase_finder.html"
        assert "<b>кораллы</b>" in context["found_phrases"]


def test_find_phrase_translit(client: FlaskClient) -> None:
    """Test find phrase method with russian text in english translit."""
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


def test_find_phrase_multiple_in_text(client: FlaskClient) -> None:
    """Test find phrase method with russian text and multiple phrases in text."""
    response = client.post(
        "/phrase-finder",
        data={"text": "Его мама любит любит апельсины", "phrases": "любить"},
    )

    assert response.status_code == 200
    assert "<b>любит</b> <b>любит</b>" in response.get_data(as_text=True)


def test_find_phrase_multiple_phrases(client: FlaskClient) -> None:
    """Test find phrase method with russian text and multiple phrases in text."""
    response = client.post(
        "/phrase-finder",
        data={"text": "мама любит бананы", "phrases": "банан\r\nлюбит", "raw": True},
    )

    assert response.status_code == 200
    assert {"банан": [[11, 16]], "любит": [[5, 9]]} == response.json["found_phrases"]


def test_find_phrase_hyphen(client: FlaskClient) -> None:
    """Test find phrase method with russian text and hyphened word."""
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


def test_find_phrase_de_without_preload(client: FlaskClient) -> None:
    """Test find phrase with unknown language."""
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


def test_find_phrase_unknown_language(client: FlaskClient) -> None:
    """Test find phrase with unknown language."""
    response = client.post(
        "/phrase-finder",
        data={"text": "Tai lietuviškas tekstas.", "phrases": ["tekstas"]},
    )

    assert response.status_code == 200
    assert "Unknown language" in response.get_data(as_text=True)
