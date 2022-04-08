class UnknownLanguageError(Exception):
    def __init__(self, language, known_languages):
        self.language = language
        self.message = 'Unknown language: %s. Please use one of: %s.' % (language, ", ".join(known_languages))
        super().__init__(self.message)
