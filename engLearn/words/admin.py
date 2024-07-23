from django.contrib import admin
from .models import Word


class WordAdmin(admin.ModelAdmin):
    list_display = ['number_in_dict', 'eng', 'ru']
    search_fields = ['eng', 'ru']
    list_display_links = ['eng', 'ru']


admin.site.register(Word, WordAdmin)
