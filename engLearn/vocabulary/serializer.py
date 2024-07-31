from rest_framework import serializers
from .models import UserWord
from rest_framework.validators import UniqueTogetherValidator
from django.views.generic import ListView

class UserWordSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        data['owner'] = self.context['request'].user.pk
        ret = super().to_internal_value(data)
        return ret

    class Meta:
        model = UserWord
        fields ='__all__'
        read_only_fields = ('wrong_answer_count', 'correct_answer_count', )
        validators = [
            UniqueTogetherValidator(
                queryset=UserWord.objects.all(),
                fields=['owner', 'word']
            )
        ]


class UserVocabularyView(ListView):

    template_name = 'vocabulary/user_vocabulary.html'
