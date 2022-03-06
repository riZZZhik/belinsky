from flask import Flask

from word_finder import WordFinder

# Initialize WordFinder
word_finder = WordFinder()

# Initialize Flask
app = Flask("WordFinder")

# Add handlers
app.add_url_rule('/highlight-words', view_func=word_finder.highlight_words, methods=['POST'])
app.add_url_rule('/add-new-word', view_func=word_finder.add_new_word, methods=['POST'])
app.add_url_rule('/get-all-words', view_func=word_finder.get_all_words, methods=['GET'])
app.register_error_handler(404, word_finder.request_not_found)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
