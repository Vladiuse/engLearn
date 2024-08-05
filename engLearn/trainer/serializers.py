from rest_framework import serializers
from rest_framework.validators import ValidationError
from words.models import Word, TranslationDirection
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


class CardSerializer:

    def __init__(self, card: Card):
        self.card = card

    @property
    def data(self):
        data = {
            'target': WordCardSerializer(self.card.target, lang=self.card.lang_direction).data,
            'answers': WordCardSerializer(self.card.answers, lang=self.card.lang_direction, many=True).data,

            # 'lang': str(self.lang),
            'lang_direction': TranslationDirectionSerializer(self.card.lang_direction).data
        }
        return data
