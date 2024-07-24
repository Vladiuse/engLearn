from rest_framework import serializers
from .models import Word, Sentence


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = '__all__'
