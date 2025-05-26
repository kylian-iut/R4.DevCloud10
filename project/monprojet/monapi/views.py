from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Commentaire
from .serializer import CommentaireSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

def index(request):
    return JsonResponse({"message": "Bienvenue sur mon API !"})

class CommentaireListApiView(APIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            commentaires = Commentaire.objects.filter(user=request.user)
        else:
            commentaires = Commentaire.objects.none()
        serializer = CommentaireSerializer(commentaires, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'titre': request.data.get('titre'),
            'commentaire': request.data.get('commentaire'),
        }
        serializer = CommentaireSerializer(data=data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.save(user=request.user)
            else:
                serializer.save(user=None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
