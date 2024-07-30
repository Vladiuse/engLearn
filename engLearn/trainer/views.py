import random as r
from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import TranslationDirectionSerializer, CardSerializer
from rest_framework.response import Response
from words.models import Word
from .cardtrainer import CardTrainer


def trainer_cards(request):
    content = {

    }
    return render(request, 'trainer/trainer_cards.html', content)


@api_view()
def get_card(request, format=None):
    serializer = TranslationDirectionSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    lang_direction = serializer.save()
    card = CardTrainer.get_card(lang_direction)
    card_serializer = CardSerializer(card)
    return Response(card_serializer.data)

