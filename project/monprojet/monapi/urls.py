from django.urls import path
from . import views
from django.conf.urls import url
from django.urls import path, include
from .views import CommentaireListApiView

urlpatterns = [
    path('api/', CommentaireListApiView.as_view()),
    path('', views.index, name='index'),  # Exemple de route
]
