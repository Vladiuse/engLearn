from django.shortcuts import render
from .serializer import UserWordSerializer
from .models import UserWord
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from rest_framework.decorators import action
from django.http import HttpResponse


class UserWordView(ModelViewSet):
    queryset = UserWord.objects.all()
    serializer_class = UserWordSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'word'

    def get_object(self):
        pk = self.kwargs['word']
        return self.get_queryset().get(word_id=pk,owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserVocabularyView(LoginRequiredMixin,ListView):
    paginate_by = 70
    paginator_class = Paginator
    template_name = 'vocabulary/user_vocabulary.html'

    def get_queryset(self):
        return UserWord.objects.filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( object_list=object_list, **kwargs)
        paginator = context['paginator']
        current_page = context['page_obj'].number
        context['paginator_pages'] = paginator.get_elided_page_range(current_page, on_each_side=2, on_ends=1, )
        return context