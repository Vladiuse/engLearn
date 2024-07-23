from django.db import models


class Word(models.Model):
    number_in_dict = models.PositiveIntegerField(blank=True, null=True)
    eng = models.CharField(max_length=100, unique=True)
    ru = models.CharField(max_length=100)

    class Meta:
        ordering = ('number_in_dict',)


class IrregularVerb(models.Model):
    first_form = models.OneToOneField(Word, on_delete=models.PROTECT)
    second_form = models.CharField(max_length=30)
    third_form = models.CharField(max_length=30)
