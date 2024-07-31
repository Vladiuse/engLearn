from django.shortcuts import render
from .models import Word
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from django.views.generic import ListView
from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet
from .serializers import WordSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import OuterRef, Exists
from vocabulary.models import UserWord


class WordListView(ListView):
    paginate_by = 70

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            vok_words = (
                UserWord.objects.filter(
                    word_id=OuterRef('id')
                ).filter(owner=self.request.user)
                .values('pk')
            )
            qs = Word.objects.annotate(is_in_vocabulary=Exists(vok_words))
        else:
            qs = Word.objects.all()
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        paginator = context['paginator']
        current_page = context['page_obj'].number
        context['paginator_pages'] = paginator.get_elided_page_range(current_page, on_each_side=2, on_ends=1, )
        return context
