from django.urls import path
from . import views

app_name = 'trainer'

urlpatterns = [
    path('', views.trainer_cards, name='trainer_cards'),
]