from . import views
from django.urls import path, re_path
from .views import CommentaireListApiView

urlpatterns = [
    path('api/', CommentaireListApiView.as_view()),
    path('api/commentaires/<int:id>/', CommentaireListApiView.as_view()),
    path('', views.index, name='index'),  # Exemple de route
]
