class CardTrainerError(Exception):
    TEXT = ''

    def __init__(self):
        self.text = self.TEXT
        self.type = self.__class__.__name__


class NoWordsToLearError(CardTrainerError):
    TEXT = 'Нет слов для изучания'
