from rest_framework import serializers
from rest_framework.validators import ValidationError


class TrainerLangSerializer(serializers.Serializer):
    lang = serializers.ChoiceField(choices=['en-ru', 'ru-en'])


class CardSerializer(serializers.Serializer):
    lang = serializers.CharField(max_length=5)
    word = serializers.SerializerMethodField()
    translate = serializers.SerializerMethodField()
    id = serializers.IntegerField()
    number_in_dict = serializers.IntegerField(required=False)
    ru = serializers.CharField(write_only=True)
    eng = serializers.CharField(write_only=True)

    def get_word(self, obj):
        return obj['ru'] if obj['lang'] == 'ru-en' else obj['eng']

    def get_translate(self, obj):
        return obj['eng'] if obj['lang'] == 'ru-en' else obj['ru']
