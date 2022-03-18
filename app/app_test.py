import sys
import unittest
import flask_unittest

from app import create_app
from modules.phrase_finder.phrase_comparer import PhraseComparer, Token


class WordFinderTest(flask_unittest.ClientTestCase):
    app = create_app()
    tokenizer = PhraseComparer()

    def tearDown(self, client):
        client.post('clear-all-words')

    def test_lemmatizer(self, _):
        response = self.tokenizer.lemmatize('Апельсины')
        correct_response = 'апельсин'
        self.assertEqual(response, correct_response)

    def test_lemmatizer_hyphen(self, _):
        response = self.tokenizer.lemmatize('по-любому')
        correct_response = 'любой'
        self.assertEqual(response, correct_response)

    def test_tokenizer(self, _):
        response = [token.to_list() for token in self.tokenizer.tokenize('Мама по-любому обожает апельсины')]
        correct_response = [
            Token("мама", "мама", (0, 3)).to_list(),
            Token('по-любому', 'любой', (5, 13)).to_list(),
            Token('обожает', 'обожать', (15, 21)).to_list(),
            Token('апельсины', 'апельсин', (23, 31)).to_list()
        ]
        self.assertEqual(response, correct_response)

    def test_compare_words(self, _):
        words = ([[self.tokenizer.lemmatize('привет')], [self.tokenizer.lemmatize('папа')]])
        response = self.tokenizer.compare_words('Привет, я Папа', words)

        correct_response = {
            'привет': [[0, 6]],
            'папа': [[10, 13]]
        }
        self.assertEqual(response, correct_response)

    def test_compare_phrases(self, _):
        words = ([[self.tokenizer.lemmatize('я '), self.tokenizer.lemmatize('папа')]])
        response = self.tokenizer.compare_words('Привет, я Папа', words)

        correct_response = {
            'я папа': [[8, 13]]
        }
        self.assertEqual(response, correct_response)

    def test_get_all_words_clear(self, client):
        response = client.get('/get-all-words')
        correct_response = {
            'result': [],
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_add_new_word(self, client):
        response = client.post(
            '/add-new-word',
            json={'word': 'проверка'}
        )
        correct_response = {
            'result': 'ok',
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_add_new_word_translit(self, client):
        client.post(
            '/add-new-word',
            json={
                'word': 'bananu'
            }
        )

        response = client.get('/get-all-words')
        correct_response = {
            'result': ['банан'],
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_add_new_word_phrase(self, client):
        client.post(
            '/add-new-word',
            json={
                'word': 'супер тест'
            }
        )

        response = client.get('/get-all-words')
        correct_response = {
            'result': ['супер тест'],
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_get_all_words(self, client):
        client.post(
            '/add-new-word',
            json={'word': 'проверка'}
        )

        response = client.get('/get-all-words')
        correct_response = {
            'result': ['проверка'],
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_highlight_one_word(self, client):
        client.post(
            '/add-new-word',
            json={
                'word': 'бананы'
            }
        )

        response = client.post(
            '/highlight-words',
            json={'text': 'мама любит бананы'}
        )
        correct_response = {
            'result': {'банан': [[11, 16]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_highlight_one_word_translit(self, client):
        client.post(
            '/add-new-word',
            json={
                'word': 'бананы'
            }
        )

        response = client.post(
            '/highlight-words',
            json={'text': 'маме и папе по bananu'}
        )
        correct_response = {
            'result': {'банан': [[15, 20]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_highlight_multiple_words(self, client):
        client.post(
            '/add-new-word',
            json={
                'word': 'бананы'
            }
        )

        response = client.post(
            '/highlight-words',
            json={'text': 'банану мама любит бананы'}
        )
        correct_response = {
            'result': {'банан': [[0, 5], [18, 23]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_highlight_phrase(self, client):
        client.post(
            '/add-new-word',
            json={
                'word': 'ненавижу апельсины'
            }
        )

        response = client.post(
            '/highlight-words',
            json={'text': 'папа ненавидит апельсины'}
        )
        correct_response = {
            'result': {'ненавидеть апельсин': [[5, 23]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_highlight_word_hyphen(self, client):
        client.post(
            '/add-new-word',
            json={
                'word': 'любой'
            }
        )

        response = client.post(
            '/highlight-words',
            json={'text': 'мама по-любому любит'}
        )
        correct_response = {
            'result': {'любой': [[5, 13]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)

    def test_highlight_hyphen_phrase(self, client):
        client.post(
            '/add-new-word',
            json={
                'word': 'обожает любой'
            }
        )

        response = client.post(
            '/highlight-words',
            json={'text': 'мама обожает по-любому тебя'}
        )
        correct_response = {
            'result': {'обожать любой': [[5, 21]]},
            'status': 200
        }
        self.assertEqual(response.json, correct_response)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.makeSuite(WordFinderTest))
    sys.exit(not result.wasSuccessful())
