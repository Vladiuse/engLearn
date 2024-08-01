from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('test', views.TestSet, basename='words-list')

app_name = 'trainer'

urlpatterns = [
    path('', views.card_trainer, name='card_trainer'),
    path('get-card/', views.get_card,name='get_card'),
    path('', include(router.urls)),
]