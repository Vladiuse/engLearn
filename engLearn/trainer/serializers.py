from rest_framework import serializers
from rest_framework.validators import ValidationError
from words.models import Word, TranslationDirection


class TranslationDirectionSerializer(serializers.Serializer):
    lang = serializers.ChoiceField(choices=['en-ru', 'ru-en'])



class WordCardSerializer(serializers.ModelSerializer):
    ru = serializers.CharField(write_only=True)
    en = serializers.CharField(write_only=True)

    word = serializers.SerializerMethodField()
    translate = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.lang = kwargs.pop('lang', 213)
        super().__init__(*args, **kwargs)

    def get_word(self, obj):
        return getattr(obj, self.lang.source_lang)

    def get_translate(self, obj):
        return getattr(obj, self.lang.target_lang)

    class Meta:
        model = Word
        fields = '__all__'

class CardSerializer:

    def __init__(self, word: Word, answers, lang: TranslationDirection):
        self.word = word
        self.answers = answers
        self.lang = lang

    @property
    def data(self):
        data = {
            'word': WordCardSerializer(self.word, lang=self.lang).data,
            'answers': WordCardSerializer(self.answers, lang=self.lang.reverse(), many=True).data,

            'lang': str(self.lang),
        }
        return data
