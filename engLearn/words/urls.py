from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'words'
urlpatterns = [
    path('', views.WordListView.as_view(), name='words_base'),
    # path('', include(router.urls),),
]