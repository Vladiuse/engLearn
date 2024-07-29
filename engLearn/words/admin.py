from django.contrib import admin
from .models import Word, IrregularVerb


class WordAdmin(admin.ModelAdmin):
    list_display = ['number_in_dict', 'en', 'ru']
    search_fields = ['en', 'ru']
    list_display_links = ['en', 'ru']


class IrregularVerbAdmin(admin.ModelAdmin):
    list_display = ['first_form__en', 'second_form', 'third_form']

    @admin.display()
    def first_form__en(self, obj):
        return obj.first_form.en

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('first_form')
        return qs


admin.site.register(Word, WordAdmin)
admin.site.register(IrregularVerb, IrregularVerbAdmin)
