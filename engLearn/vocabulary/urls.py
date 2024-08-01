from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from . import views

app_name = 'vocabulary'
router = DefaultRouter()
router.register('', views.UserWordView, basename='userword')

urlpatterns = [
    path('', views.UserVocabularyView.as_view(),name='user_vocabulary'),
    path('api/', include(router.urls),),
]