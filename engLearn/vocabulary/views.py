from django.shortcuts import render
from .serializer import UserWordSerializer
from .models import UserWord
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


class UserVocabularyView(ModelViewSet):
    queryset = UserWord.objects.all()
    serializer_class = UserWordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
