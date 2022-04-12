"""Unittest Belinsky application."""
import sys
import unittest

import flask_unittest

from belinsky import create_app, database, models
from belinsky.routes.phrase_finder.phrase_comparer import PhraseComparer, Token
from belinsky.routes.utils import translit


def add_user(app, username, password):
    """Add user model to database."""
    with app.app_context():
        if database.get_instance(models.User, username=username) is None:
            database.add_instance(models.User,
                                  lambda instance: instance.set_password(password),
                                  username=username)


def delete_user(app, username):
    """Delete user model from database."""
    with app.app_context():
        if database.get_instance(models.User, username=username) is not None:
            database.delete_instance(models.User, username=username)


# pylint: disable=too-many-public-methods
class PhraseFinderTest(flask_unittest.ClientTestCase):
    """Unittest Belinsky application."""
    # Initialize app
    credentials = {'username': 'unittester', 'password': 'test_password'}
    app = create_app()

    # Create test user
    add_user(app, credentials['username'], credentials['password'])

    # Initialize plugins
    comparer = PhraseComparer()

    def setUp(self, client):
        """Login as test user."""
        client.post('login', json=self.credentials)

    def test_lemmatizer(self, _):
        """Test lemmatizer russian word."""
        response = self.comparer.lemmatize('Апельсины', 'ru')
        correct_response = ['апельсин']
        self.assertEqual(response, correct_response)

    def test_lemmatizer_hyphen(self, _):
        """Test lemmatizer with russian hyphened word."""
        response = self.comparer.lemmatize('по-любому', 'ru')
        correct_response = ['любой']
        self.assertEqual(response, correct_response)

    def test_lemmatizer_phrase(self, _):
        """Test lemmatizer with russian phrase."""
        response = self.comparer.lemmatize('а он обожает', 'ru')
        correct_response = ['а', 'он', 'обожать']
        self.assertEqual(response, correct_response)

    def test_lemmatizer_punctuation(self, _):
        """Test lemmatizer with russian phrase with punctuation."""
        response = self.comparer.lemmatize('а, -- [он], обожает?!', 'ru')
        correct_response = ['а', 'он', 'обожать']
        self.assertEqual(response, correct_response)

    def test_lemmatizer_en(self, _):
        """Test lemmatizer with english word."""
        response = self.comparer.lemmatize('stunned', 'en')
        correct_response = ['stun']
        self.assertEqual(response, correct_response)

    def test_translit_ru(self, _):
        """Test lemmatizers with russian word using english translit."""
        response = translit('banan', 'ru')
        correct_response = 'банан'
        self.assertEqual(response, correct_response)

    def test_detect_language_ru(self, _):
        """Test detect language with russian phrase."""
        response = self.comparer.detect_language('Это русский текст')
        correct_response = 'ru'
        self.assertEqual(response, correct_response)

    def test_detect_language_en(self, _):
        """Test detect language with english phrase."""
        response = self.comparer.detect_language('This is english text')
        correct_response = 'en'
        self.assertEqual(response, correct_response)

    def test_tokenizer(self, _):
        """Test tokenizer from PhraseFinder."""
        response = [token.to_list() for token in
                    self.comparer.tokenize('Мама обожает апельсины', 'ru')]
        correct_response = [
            Token("Мама", "мама", (0, 3)).to_list(),
            Token('обожает', 'обожать', (5, 11)).to_list(),
            Token('апельсины', 'апельсин', (13, 21)).to_list()
        ]
        self.assertEqual(response, correct_response)

    def test_compare_phrases(self, _):
        """Test compare phrases from PhraseFinder."""
        response = self.comparer.find_phrases('Привет, я Папа', ['я папа'], 'ru')

        correct_response = {
            'я папа': [[8, 13]]
        }
        self.assertEqual(response, correct_response)

    def test_signup(self, client):
        """Test signup method."""
        delete_user(self.app, 'unittester_1')

        response = client.post('/signup',
                               json={'username': 'unittester_1', 'password': 'test_password'})

        correct_response = {
            'result': "Successfully signed up as unittester_1.",
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_login(self, client):
        """Test login method."""
        client.post('/logout')
        response = client.post('login', json=self.credentials)
        correct_response = {
            'result': "Successfully logged in as unittester.",
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_delete(self, client):
        """Test delete method."""
        add_user(self.app, 'unittester_1', 'test_password')

        response = client.post('delete-user',
                               json={'username': 'unittester_1', 'password': 'test_password'})

        correct_response = {
            'result': "Successfully deleted unittester_1 user.",
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_logout(self, client):
        """Test logout method."""
        response = client.post('/logout')
        correct_response = {
            'result': 'Successfully logged out.',
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_find_phrase(self, client):
        """Test find phrase method with russian text."""
        response = client.get(
            '/find-phrases',
            json={'text': 'папа ненавидит апельсины', 'phrases': ['ненавижу апельсины']}
        )
        correct_response = {
            'result': {'ненавижу апельсины': [[5, 23]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_find_phrase_translit(self, client):
        """Test find phrase method with russian text in english translit."""
        response = client.get(
            '/find-phrases',
            json={'text': 'маме и папе по bananu', 'phrases': ['бананы'], 'language': 'ru'}
        )
        correct_response = {
            'result': {'бананы': [[15, 20]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_find_phrase_multiple_in_text(self, client):
        """Test find phrase method with russian text and multiple phrases in text."""
        response = client.get(
            '/find-phrases',
            json={'text': 'банан мама любит бананы', 'phrases': ['банан']}
        )
        correct_response = {
            'result': {'банан': [[0, 4], [17, 22]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_find_phrase_multiple_phrases(self, client):
        """Test find phrase method with russian text and multiple phrases in text."""
        response = client.get(
            '/find-phrases',
            json={'text': 'мама любит бананы', 'phrases': ['банан', 'любит']}
        )
        correct_response = {
            'result': {'банан': [[11, 16]], 'любит': [[5, 9]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_find_phrase_hyphen(self, client):
        """Test find phrase method with russian text and hyphened word."""
        response = client.get(
            '/find-phrases',
            json={'text': 'мама обожает по-любому тебя', 'phrases': ['обожает любой']}
        )
        correct_response = {
            'result': {'обожает любой': [[5, 21]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_find_phrase_unknown_language(self, client):
        """Test find phrase with unknown language."""
        response = client.get(
            '/find-phrases',
            json={'text': 'Dies ist ein deutsch.', 'phrases': []}
        )
        correct_response = {
            'error': 'Unknown language: de. Please use one of: en, ru.',
            'status': 400
        }
        self.assertEqual(response.json, correct_response)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.makeSuite(PhraseFinderTest))
    sys.exit(not result.wasSuccessful())
