import random as r
from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import TranslationDirectionSerializer, CardSerializer
from rest_framework.response import Response
from words.models import Word
from .trainer import Trainer


def trainer_cards(request):
    content = {

    }
    return render(request, 'trainer/trainer_cards.html', content)


@api_view()
def get_card(request, format=None):
    serializer = TranslationDirectionSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    lang_direction = serializer.save()
    word = Word.objects.order_by('?').first()
    answers = list(Word.objects.exclude(pk=word.pk).order_by('?')[:Trainer.ANSWERS_COUNT - 1])
    answers.append(word)
    r.shuffle(answers)
    card_serializer = CardSerializer(target=word, answers=answers, lang_direction=lang_direction)
    return Response(card_serializer.data)

