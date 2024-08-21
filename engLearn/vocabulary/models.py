from django.db import models
from django.contrib.auth.models import User
from words.models import Word



class UserWord(models.Model):
    LEARNED = 'learned'
    LEARNING = 'learning'
    STATUSES = (
        (LEARNED,'Выучено'),
        (LEARNING,'Изучаю'),

    )
    word = models.ForeignKey(
        to=Word,
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=12,
        choices=STATUSES,
        default=LEARNING,
    )
    wrong_answer_count = models.PositiveIntegerField(
        blank=True,
        default=0,
    )
    correct_answer_count = models.PositiveIntegerField(
        blank=True,
        default=0,
    )

    class Meta:
        unique_together = ('owner', 'word')

    @staticmethod
    def is_user_has_words_to_train(user):
        if user.is_authenticated:
            return UserWord.objects.filter(owner=user, status=UserWord.LEARNING).exists()
        return False


class Vocabulary:

    def __init__(self, user: User):
        self.user = user


    def _get_queryset(self):
        return UserWord.objects.filter(owner=self.user)

    def stat(self):
        total_words = self.total_words
        words_learned = self.words_learned
        words_learning = total_words -  words_learned
        percent =  round(words_learned / total_words * 100)
        data = {
            'total_words': total_words,
            'words_learned':words_learned,
            'words_learning': words_learning,
            'percent': percent,
        }
        return data

    @property
    def total_words(self) -> int:
        return self._get_queryset().count()

    @property
    def words_learned(self) -> int:
        return self._get_queryset().filter(status=UserWord.LEARNED).count()