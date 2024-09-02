from django.db import models
from enum import Enum
from django.contrib.auth.models import User


class TranslationDirection:
    AVAILABLE = ('en-ru', 'ru-en')

    def __init__(self, direction: str):
        self.direction = direction
        if self.direction not in TranslationDirection.AVAILABLE:
            raise ValueError('Incorrect lang')

    def __str__(self):
        return self.direction

    @property
    def source_lang(self) -> str:
        return self.direction.split('-')[0]

    @property
    def target_lang(self) -> str:
        return self.direction.split('-')[-1]

    def reverse(self) -> 'TranslationDirection':
        lang = self.target_lang + '-' + self.source_lang
        return TranslationDirection(lang)


class EnglishLevel(Enum):
    A0 = ('A0', 'Beginner', (0, 500), '#6fd2f4')
    A1 = ('A1', 'Elementary', (500, 1000), '#4fc1e9')
    A2 = ('A2', 'Pre Intermediate', (1000, 2000), '#3bafda')
    B1 = ('B1', 'Intermediate', (2000, 3500), '#48cfad')
    B2 = ('B2', 'Upper Intermediate', (3500, 5000), '#37bc9b')
    C1 = ('C1', 'Advanced', (5000, 8000), '#ac92ec')
    C2 = ('C2', 'Proficient', (8000, 12000), '#967adc')

    def __init__(self, id, name, words_range, color):
        self._id = id
        self._name = name
        self._color = color
        self._words_range = words_range

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def words_range(self):
        return self._words_range

    @classmethod
    def choices(cls):
        return [level for level in cls]

    @classmethod
    def get_by_id(cls, id):
        dic = {level.id: level for level in cls}
        return dic[id]

    def __eq__(self, other):
        return self.id == str(other).upper()


class Word(models.Model):
    number_in_dict = models.PositiveIntegerField(blank=True, null=True)
    en = models.CharField(max_length=100)
    ru = models.CharField(max_length=100)
    created = models.DateField(auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True,)

    class Meta:
        ordering = ('number_in_dict',)
        unique_together = ('en', 'ru')

    def __str__(self):
        return f'{self.en} - {self.ru}'


class IrregularVerb(models.Model):
    first_form = models.OneToOneField(Word, on_delete=models.PROTECT)
    second_form = models.CharField(max_length=30)
    third_form = models.CharField(max_length=30)

