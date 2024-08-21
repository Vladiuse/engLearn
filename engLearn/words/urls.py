from django.urls import path
from . import views

app_name = 'words'
urlpatterns = [
    path('', views.WordListView.as_view(), name='words_base'),
    # path('', include(router.urls),),
]