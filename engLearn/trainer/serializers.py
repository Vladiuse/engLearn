from rest_framework import serializers
from rest_framework.validators import ValidationError
from words.models import Word, TranslationDirection, Sentence
from .cardtrainer import Card, CardTrainer

class TranslationDirectionSerializer(serializers.Serializer):
    direction = serializers.ChoiceField(choices=TranslationDirection.AVAILABLE)


class CreateCardSerializer(serializers.Serializer):
    direction = serializers.ChoiceField(choices=TranslationDirection.AVAILABLE)
    regime = serializers.ChoiceField(choices=CardTrainer.REGIMES)

    def create(self, validated_data):
        lang_direction = TranslationDirection(direction=validated_data['direction'])
        card_trainer = CardTrainer(
            user=self.context['request'].user,
            lang_direction=lang_direction,
            regime=validated_data['regime'],
        )
        return card_trainer

    def validate(self, data):
        if data['regime'] == CardTrainer.USER_VOC_REGIME and not self.context['request'].user.is_authenticated:
            raise ValidationError(f'Autorize to use {CardTrainer.USER_VOC_REGIME} regime')
        return data


class WordCardSerializer(serializers.ModelSerializer):
    ru = serializers.CharField(write_only=True)
    en = serializers.CharField(write_only=True)

    word = serializers.SerializerMethodField()
    translate = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.lang = kwargs.pop('lang')
        super().__init__(*args, **kwargs)

    def get_word(self, obj):
        return getattr(obj, self.lang.source_lang)

    def get_translate(self, obj):
        return getattr(obj, self.lang.target_lang)

    class Meta:
        model = Word
        fields = '__all__'


class SentenceCardSerializer(WordCardSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        sentence = data.pop('word')
        data['sentence'] = sentence
        return data

    class Meta:
        model = Sentence
        exclude = ('words',)


class CardSerializer:

    def __init__(self, card: Card):
        self.card = card

    @property
    def data(self):
        data = {
            'target': WordCardSerializer(self.card.target, lang=self.card.lang_direction).data,
            'answers': WordCardSerializer(self.card.answers, lang=self.card.lang_direction, many=True).data,
            'sentence': self.sentence_data,
            'lang_direction': TranslationDirectionSerializer(self.card.lang_direction).data
        }
        return data

    @property
    def sentence_data(self):
        if self.card.sentence:
            return SentenceCardSerializer(self.card.sentence, lang=self.card.lang_direction).data
        return None