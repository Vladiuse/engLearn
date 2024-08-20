from django.contrib import admin
from .models import Word, IrregularVerb, Sentence
from vocabulary.models import UserWord
from django.db import IntegrityError
from django.utils.translation import ngettext
from django.contrib import messages


class WordContext(admin.TabularInline):
    model = Sentence.words.through
    extra = 0
    can_delete = False
    show_change_link = True


class WordAdmin(admin.ModelAdmin):
    list_display = ['number_in_dict', 'en', 'ru']
    search_fields = ['en', 'ru']
    list_display_links = ['en', 'ru']
    inlines = [
        WordContext,
    ]
    actions = ["add_to_vocabulary"]


    @admin.action(description='Add to vocabulary')
    def add_to_vocabulary(self, request, queryset):
        create_count = 0
        already_exist = 0
        for word in queryset:
            try:
                UserWord.objects.create(
                    owner=request.user,
                    word=word
                )
                create_count += 1
            except IntegrityError:
                already_exist += 1
        message = f'Add: {create_count}, already exist: {already_exist}.'
        status = messages.SUCCESS if create_count else messages.WARNING
        self.message_user(
            request,
            message,
            status,
        )


class IrregularVerbAdmin(admin.ModelAdmin):
    list_display = ['first_form__en', 'second_form', 'third_form']

    @admin.display()
    def first_form__en(self, obj):
        return obj.first_form.en

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('first_form')
        return qs


class SentenceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'en', 'ru']
    autocomplete_fields = ['words']
    inlines = [
        WordContext,
    ]


admin.site.register(Word, WordAdmin)
admin.site.register(IrregularVerb, IrregularVerbAdmin)
admin.site.register(Sentence, SentenceAdmin)
