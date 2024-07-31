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
