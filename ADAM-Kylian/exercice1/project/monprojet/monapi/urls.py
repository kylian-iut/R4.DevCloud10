from . import views
from django.urls import path, re_path
from .views import AlbumListApiView

urlpatterns = [
    path('api/', AlbumListApiView.as_view()),
    path('api/albums/<int:id>/', AlbumListApiView.as_view()),
    path('', views.index, name='index'),  # Exemple de route
]
