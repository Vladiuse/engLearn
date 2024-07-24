from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import TrainerLangSerializer, CardSerializer
from rest_framework.response import Response
from words.models import Word


def trainer_cards(request):
    content = {

    }
    return render(request, 'trainer/trainer_cards.html', content)


@api_view()
def get_card(request, format=None):
    serializer = TrainerLangSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    word = Word.objects.order_by('?')[0]
    data = {
        'lang': serializer.validated_data['lang'],
        **word.__dict__,
    }
    card_serializer = CardSerializer(data)
    return Response(card_serializer.data)

