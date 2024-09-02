from django.contrib import admin
from vocabulary.models import UserWord, Sentence


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
    readonly_fields = ['owner']

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)


class SentenceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'en', 'ru']
    autocomplete_fields = ['words']
    inlines = [
        WordContext,
    ]


admin.site.register(UserWord, UserWordAdmin)
admin.site.register(Sentence, SentenceAdmin)
