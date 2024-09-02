from django.db import models
from django.contrib.auth.models import User


class UserWord(models.Model):
    LEARNED = 'learned'
    LEARNING = 'learning'
    POSTPONED = 'postponed'
    STATUSES = (
        (LEARNED, 'Выучено'),
        (LEARNING, 'Изучаю'),
        (POSTPONED, 'Отложено'),
    )
    en = models.CharField(
        max_length=100
    )
    ru = models.CharField(
        max_length=100
    )
    created = models.DateField(
        auto_now=True
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

    class Meta:
        unique_together = ('owner', 'en', 'ru')

    @staticmethod
    def is_user_has_words_to_train(user):
        if user.is_authenticated:
            return UserWord.objects.filter(owner=user, status=UserWord.LEARNING).exists()
        return False

class Sentence(models.Model):
    words = models.ManyToManyField(to=UserWord, related_name='sentences', related_query_name='sentence')
    en = models.CharField(max_length=255)
    ru = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.en)


class Vocabulary:

    def __init__(self, user: User):
        self.user = user


    def _get_queryset(self):
        return UserWord.objects.filter(owner=self.user)

    def stat(self):
        total_words = self.total_words
        words_learned = self.words_learned
        words_learning = total_words -  words_learned
        if total_words !=0:
            percent =  round(words_learned / total_words * 100)
        else:
            percent = 0
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