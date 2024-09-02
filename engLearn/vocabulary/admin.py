from django.contrib import admin
from vocabulary.models import UserWord, Sentence
from django.db import IntegrityError
from django.contrib import messages


class WordContext(admin.TabularInline):
    model = Sentence.words.through
    extra = 0
    can_delete = False
    show_change_link = True


class UserWordAdmin(admin.ModelAdmin):
    list_display = ['en', 'ru']
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

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
        UserWord.objects.create(word=obj, owner=request.user)


class SentenceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'en', 'ru']
    autocomplete_fields = ['words']
    inlines = [
        WordContext,
    ]


admin.site.register(UserWord, UserWordAdmin)
admin.site.register(Sentence, SentenceAdmin)
