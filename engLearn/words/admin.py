from django.contrib import admin
from .models import Word, IrregularVerb


class WordAdmin(admin.ModelAdmin):
    list_display = ['number_in_dict', 'eng', 'ru']
    search_fields = ['eng', 'ru']
    list_display_links = ['eng', 'ru']


class IrregularVerbAdmin(admin.ModelAdmin):
    list_display = ['first_form__eng', 'second_form', 'third_form']

    @admin.display()
    def first_form__eng(self, obj):
        return obj.first_form.eng


admin.site.register(Word, WordAdmin)
admin.site.register(IrregularVerb, IrregularVerbAdmin)
