from . import views
from django.urls import path, re_path
from .views import ClientListApiView

urlpatterns = [
    path('api/', ClientListApiView.as_view()),
    path('api/clients/<int:id>/', ClientListApiView.as_view()),
    path('', views.index, name='index'),  # Exemple de route
]
