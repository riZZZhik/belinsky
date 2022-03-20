import sys
import unittest
import flask_unittest

from belinsky import create_app
from belinsky.modules.phrase_finder.phrase_comparer import PhraseComparer, Token


class PhraseFinderTest(flask_unittest.ClientTestCase):
    app = create_app()
    comparer = PhraseComparer()

    def tearDown(self, client):
        client.post('clear-known-phrases')

    def test_lemmatizer(self, _):
        response = self.comparer.lemmatize('Апельсины')
        correct_response = 'апельсин'
        self.assertEqual(response, correct_response)

    def test_lemmatizer_hyphen(self, _):
        response = self.comparer.lemmatize('по-любому')
        correct_response = 'любой'
        self.assertEqual(response, correct_response)

    def test_tokenizer(self, _):
        response = [token.to_list() for token in self.comparer.tokenize('Мама по-любому обожает апельсины')]
        correct_response = [
            Token("мама", "мама", (0, 3)).to_list(),
            Token('по-любому', 'любой', (5, 13)).to_list(),
            Token('обожает', 'обожать', (15, 21)).to_list(),
            Token('апельсины', 'апельсин', (23, 31)).to_list()
        ]
        self.assertEqual(response, correct_response)

    def test_compare_phrases(self, _):
        phrases = ([[self.comparer.lemmatize('я '), self.comparer.lemmatize('папа')]])
        response = self.comparer.compare_phrases('Привет, я Папа', phrases)

        correct_response = {
            'я папа': [[8, 13]]
        }
        self.assertEqual(response, correct_response)

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
                'phrase': 'хочу bananu'
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
                'phrase': 'бананы'
            }
        )

        response = client.post(
            '/find-phrases',
            json={'text': 'мама любит бананы'}
        )
        correct_response = {
            'result': {'банан': [[11, 16]]},
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
            json={'text': 'маме и папе по bananu'}
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

    def test_find_phrase_hyphen(self, client):
        client.post(
            '/add-phrase',
            json={
                'phrase': 'любой'
            }
        )

        response = client.post(
            '/find-phrases',
            json={'text': 'мама по-любому любит'}
        )
        correct_response = {
            'result': {'любой': [[5, 13]]},
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
