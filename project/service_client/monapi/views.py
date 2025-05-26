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
    permissions_classes = [IsAuthenticated]
    # On permet l'authentification ET l'accès annonyme
    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            commentaires = Commentaire.objects.filter(pk=id)
            if not Commentaire:
                return Response({"res": "Object with id does not exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif request.user.is_authenticated:
            commentaires = Commentaire.objects.filter(user=request.user)
        else:
            commentaires = Commentaire.objects.none()
        serializer = CommentaireSerializer(commentaires, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data

        # Vérifier s'il y a une liste d'objets dans l'instance POST OU un seul
        if isinstance(data, list):
            serializer = CommentaireSerializer(data=data, many=True)
        else:
            serializer = CommentaireSerializer(data=data)
        
        # On permet également l'authentification ET l'accès annonyme
        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.save(user=request.user)
            else:
                serializer.save(user=None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None, *args, **kwargs):
        try:
            commentaire = Commentaire.objects.get(pk=id)
        except Commentaire.DoesNotExist:
            return Response(
                {"res":"Object with id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )
        if commentaire.user != request.user and commentaire.user != None:
            return Response({"res": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        commentaire.delete()
        return Response({"res":"Object deleted!"},
                        status=status.HTTP_200_OK
                        )
    
    def put(self, request, id, *args, **kwargs):
        try:
            commentaire = Commentaire.objects.get(pk=id)
        except Commentaire.DoesNotExist:
            return Response(
                {"res": "Object with id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            'titre': request.data.get('titre'),
            'commentaire': request.data.get('commentaire'),
        }
        if commentaire.user != request.user and commentaire.user != None:
            return Response({"res": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        if not data['titre'] or not data['commentaire']:
            return Response(
                {"res": "Both 'titre' and 'commentaire' fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CommentaireSerializer(instance=commentaire, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
