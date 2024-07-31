from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'vocabulary'
router = DefaultRouter()
router.register('', views.UserWordView, basename='user_word')

urlpatterns = [
    path('', views.UserVocabularyView.as_view(),name='user_vocabulary'),
    path('', include(router.urls),),
]