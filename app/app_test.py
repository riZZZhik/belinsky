import sys
import unittest

import flask_unittest

from belinsky import create_app, database, models
from belinsky.routes.phrase_finder.phrase_comparer import PhraseComparer, Token


def add_user(app, username, password, language):
    with app.app_context():
        if database.get_instance(models.User, username=username) is None:
            database.add_instance(models.User, lambda instance: instance.set_password(password),
                                  username=username, language=language)


def delete_user(app, username):
    with app.app_context():
        if database.get_instance(models.User, username=username) is not None:
            database.delete_instance(models.User, username=username)


class PhraseFinderTest(flask_unittest.ClientTestCase):
    # Initialize app
    credentials = {'username': 'unittester', 'password': 'test_password'}
    app = create_app()

    # Create test user
    add_user(app, credentials['username'], credentials['password'], 'ru')

    # Initialize plugins
    comparer = PhraseComparer()

    def setUp(self, client):
        client.post('login', json=self.credentials)

    def tearDown(self, client):
        database.edit_instance(models.User, {'username': 'unittester'}, known_phrases=[])

    def test_lemmatizer(self, _):
        response = self.comparer.lemmatize('Апельсины', 'ru')
        correct_response = 'апельсин'
        self.assertEqual(response, correct_response)

    def test_lemmatizer_hyphen(self, _):
        response = self.comparer.lemmatize('по-любому', 'ru')
        correct_response = 'любой'
        self.assertEqual(response, correct_response)

    def test_lemmatizer_en(self, _):
        response = self.comparer.lemmatize('stunned', 'en')
        correct_response = 'stun'
        self.assertEqual(response, correct_response)

    def test_tokenizer(self, _):
        response = [token.to_list() for token in self.comparer.tokenize('Мама по-любому обожает апельсины', 'ru')]
        correct_response = [
            Token("мама", "мама", (0, 3)).to_list(),
            Token('по-любому', 'любой', (5, 13)).to_list(),
            Token('обожает', 'обожать', (15, 21)).to_list(),
            Token('апельсины', 'апельсин', (23, 31)).to_list()
        ]
        self.assertEqual(response, correct_response)

    def test_compare_phrases(self, _):
        phrases = ([[self.comparer.lemmatize('я ', 'ru'), self.comparer.lemmatize('папа', 'ru')]])
        response = self.comparer.compare_phrases('Привет, я Папа', phrases, 'ru')

        correct_response = {
            'я папа': [[8, 13]]
        }
        self.assertEqual(response, correct_response)

    def test_signup(self, client):
        delete_user(self.app, 'unittester_1')

        response = client.post('/signup', json={'username': 'unittester_1',
                                                'password': 'test_password',
                                                'language': 'ru'})
        correct_response = {
            'result': "Successfully signed up as unittester_1.",
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_delete(self, client):
        add_user(self.app, 'unittester_1', 'test_password', 'ru')

        response = client.post('delete-user', json={'username': 'unittester_1', 'password': 'test_password'})
        correct_response = {
            'result': "Successfully deleted unittester_1 user.",
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_logout(self, client):
        response = client.post('/logout')
        correct_response = {
            'result': 'Successfully logged out.',
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_login(self, client):
        client.post('/logout')
        response = client.post('login', json=self.credentials)
        correct_response = {
            'result': "Successfully logged in as unittester.",
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_get_known_phrases_clear(self, client):
        response = client.get('/get-known-phrases')
        correct_response = {
            'result': [],
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_add_phrase(self, client):
        response = client.post(
            '/add-phrase',
            json={'phrase': 'супер тест'}
        )
        correct_response = {
            'result': 'ok',
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_add_phrase_translit(self, client):
        client.post(
            '/add-phrase',
            json={
                'phrase': 'хочу banana'
            }
        )

        response = client.get('/get-known-phrases')
        correct_response = {
            'result': ['хотеть банан'],
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_get_known_phrases(self, client):
        client.post(
            '/add-phrase',
            json={'phrase': 'проверка'}
        )

        response = client.get('/get-known-phrases')
        correct_response = {
            'result': ['проверка'],
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_find_phrase(self, client):
        client.post(
            '/add-phrase',
            json={
                'phrase': 'ненавижу апельсины'
            }
        )

        response = client.post(
            '/find-phrases',
            json={'text': 'папа ненавидит апельсины'}
        )
        correct_response = {
            'result': {'ненавидеть апельсин': [[5, 23]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_find_phrase_translit(self, client):
        client.post(
            '/add-phrase',
            json={
                'phrase': 'бананы'
            }
        )

        response = client.post(
            '/find-phrases',
            json={'text': 'маме и папе по banana'}
        )
        correct_response = {
            'result': {'банан': [[15, 20]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_find_phrase_multiple(self, client):
        client.post(
            '/add-phrase',
            json={
                'phrase': 'бананы'
            }
        )

        response = client.post(
            '/find-phrases',
            json={'text': 'банану мама любит бананы'}
        )
        correct_response = {
            'result': {'банан': [[0, 5], [18, 23]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_find_phrase_hyphen(self, client):
        client.post(
            '/add-phrase',
            json={
                'phrase': 'обожает любой'
            }
        )

        response = client.post(
            '/find-phrases',
            json={'text': 'мама обожает по-любому тебя'}
        )
        correct_response = {
            'result': {'обожать любой': [[5, 21]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.makeSuite(PhraseFinderTest))
    sys.exit(not result.wasSuccessful())
