from words.models import Word, TranslationDirection, EnglishLevel
from typing import List, Optional
import random as r
from django.contrib.auth.models import User
from vocabulary.models import UserWord


class Card:

    def __init__(self, target: Word, answers: List[Word], lang_direction: TranslationDirection):
        self.target = target
        self.answers = answers
        self.lang_direction = lang_direction


class CardTrainer:
    USER_VOC_REGIME = 'user_vocabulary'
    REGIMES = [
        USER_VOC_REGIME,
        'A0',
        'A1',
        'A2',
        'B1',
        'B2',
        'C1',
        'C2',
    ]
    TOTAL_ANSWERS_COUNT = 5
    ANSWERS_COUNT = TOTAL_ANSWERS_COUNT - 1

    def __init__(self, user: User, regime:str, lang_direction: TranslationDirection):
        self.user = user
        self.regime = regime
        self.lang_direction = lang_direction

        print(regime, user)

    def get_queryset(self):
        if self.user.is_authenticated and self.regime == CardTrainer.USER_VOC_REGIME:
            userwords_ids = UserWord.objects.filter(owner=self.user, status=UserWord.LEARNING).values('word')
            return Word.objects.filter(pk__in=userwords_ids)
        else:
            level = EnglishLevel.get_by_id(self.regime)
            return Word.objects.filter(number_in_dict__range=level.words_range)

    def get_card(self) -> Card:
        word = self._get_word()
        answers = self._get_answers(word=word)
        card = Card(
            target=word,
            answers=answers,
            lang_direction=self.lang_direction
        )
        return card

    def _get_word(self) -> Word:
        qs = self.get_queryset()
        word = qs.order_by('?').first()
        # if not word:
        #     raise
        return word

    def _get_answers(self, word: Word) -> List[Word]:
        qs = self.get_queryset()
        qs.exclude(pk=word.pk)
        qs = qs.order_by('?')[:CardTrainer.ANSWERS_COUNT]
        answers = list(qs)
        answers.append(word)
        r.shuffle(answers)
        return answers
