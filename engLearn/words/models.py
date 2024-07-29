from django.db import models

class TranslationDirection:

    AVAILABLE = ('en-ru', 'ru-en')

    def __init__(self, direction:str):
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



class Word(models.Model):

    number_in_dict = models.PositiveIntegerField(blank=True, null=True)
    en = models.CharField(max_length=100, unique=True)
    ru = models.CharField(max_length=100)

    class Meta:
        ordering = ('number_in_dict',)


class IrregularVerb(models.Model):
    first_form = models.OneToOneField(Word, on_delete=models.PROTECT)
    second_form = models.CharField(max_length=30)
    third_form = models.CharField(max_length=30)


class Sentence(models.Model):
    word = models.ForeignKey(to=Word, on_delete=models.CASCADE)
    end = models.CharField(max_length=255)
    ru = models.CharField(max_length=255, blank=True)
