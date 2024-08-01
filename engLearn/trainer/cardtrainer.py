from words.models import Word, TranslationDirection
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
    TOTAL_ANSWERS_COUNT = 5
    ANSWERS_COUNT = TOTAL_ANSWERS_COUNT - 1
    WORD_RANGE = (1000, 2000)

    def __init__(self, user:User):
        self.user = user
    
    def get_queryset(self):
        if self.user.is_authenticated:
            userwords_ids = UserWord.objects.filter(owner=self.user, status=UserWord.LEARNING).values('word')
            return Word.objects.filter(pk__in=userwords_ids)
        else:
            return Word.objects.filter(number_in_dict__range=CardTrainer.WORD_RANGE)

    def get_card(self, lang_direction: TranslationDirection) -> Card:
        word = self._get_word()
        answers = self._get_answers(word=word)
        card = Card(
            target=word,
            answers=answers,
            lang_direction=lang_direction
        )
        return card

    
    def _get_word(self) -> Word:
        qs = self.get_queryset()
        return qs.order_by('?').first()

    
    def _get_answers(self, word: Optional[Word]) -> List[Word]:
        qs = self.get_queryset()
        if word:
            qs.exclude(pk=word.pk)
        qs = qs.order_by('?')[:CardTrainer.ANSWERS_COUNT]
        answers = list(qs)
        answers.append(word)
        r.shuffle(answers)
        return answers
