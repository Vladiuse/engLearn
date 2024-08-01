import random as r
from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import TranslationDirectionSerializer, CardSerializer
from rest_framework.response import Response
from words.models import Word
from  words.serializers import WordSerializer
from .cardtrainer import CardTrainer
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.decorators import renderer_classes
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet


def card_trainer(request):
    return render(request, 'trainer/card_trainer.html')


@api_view()
def get_card(request, format=None):
    serializer = TranslationDirectionSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    lang_direction = serializer.save()
    card = CardTrainer(request.user).get_card(lang_direction)
    card_serializer = CardSerializer(card)
    return Response(card_serializer.data)

class TestSet(ModelViewSet):
    queryset = Word.objects.all()[:10]
    serializer_class = WordSerializer
    template_name = 'vocabulary/test.html'

    def get_renderers(self):
        if self.action == 'list':
            return [TemplateHTMLRenderer(), JSONRenderer(), BrowsableAPIRenderer()]
        else:
            return [JSONRenderer(), BrowsableAPIRenderer()]


    def render_html_response(self, request):
        words = self.get_queryset()
        return render(request, self.template_name, {'words': words})

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html' or not request.accepted_renderer:
            return self.render_html_response(request)
        else:
            return super().list(request, *args, **kwargs)

# @api_view(['GET'])
# def test(request):
#     data = {
#         'data': 'DATA',
#         'request': request.query_params
#     }
#     return Response(data, template_name='vocabulary/test.html')
#     # return render(request, 'vocabulary/test.html')