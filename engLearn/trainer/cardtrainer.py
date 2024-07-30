from words.models import Word, TranslationDirection
from typing import List, Optional
import random as r


class Card:

    def __init__(self, target: Word, answers: List[Word], lang_direction: TranslationDirection):
        self.target = target
        self.answers = answers
        self.lang_direction = lang_direction


class CardTrainer:
    TOTAL_ANSWERS_COUNT = 5
    ANSWERS_COUNT = TOTAL_ANSWERS_COUNT - 1
    WORD_RANGE = (1000, 2000)

    qs = Word.objects.filter(number_in_dict__range=WORD_RANGE)

    @classmethod
    def get_card(cls, lang_direction: TranslationDirection) -> Card:
        word = cls._get_word()
        answers = cls._get_answers(word=word)
        card = Card(
            target=word,
            answers=answers,
            lang_direction=lang_direction
        )
        return card

    @classmethod
    def _get_word(cls) -> Word:
        return cls.qs.order_by('?').first()

    @classmethod
    def _get_answers(cls, word: Optional[Word]) -> List[Word]:
        qs = cls.qs
        if word:
            qs.exclude(pk=word.pk)
        qs = qs.order_by('?')[:CardTrainer.ANSWERS_COUNT]
        answers = list(qs)
        answers.append(word)
        r.shuffle(answers)
        return answers
