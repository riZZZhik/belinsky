class WordFinder:
    def __init__(self, var):
        self.words = ['test', 'super_test']

    def get_all_words(self):
        response = {
            'result': self.words,
            'status': 200
        }
        return response
