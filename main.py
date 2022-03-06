from flask import Flask

from word_finder import WordFinder

# Initialize WordFinder
word_finder = WordFinder("123")

# Initialize Flask
app = Flask("WordFinder")

# Add handlers
app.add_url_rule('/get-all-words', view_func=word_finder.get_all_words, methods=['GET'])
app.add_url_rule('/add-new-word', view_func=word_finder.add_new_word, methods=['POST'])

# Run app
if __name__ == '__main__':
    app.run(debug=True)
