from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Album
from .serializer import AlbumSerializer

def index(request):
    return JsonResponse({"message": "Bienvenue sur mon API !"})

class AlbumListApiView(APIView):
    # On permet l'authentification ET l'accès annonyme
    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            albums = Album.objects.filter(pk=id)
            if not Album:
                return Response({"res": "Object with id does not exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data

        # Vérifier s'il y a une liste d'objets dans l'instance POST OU un seul
        if isinstance(data, list):
            serializer = AlbumSerializer(data=data, many=True)
        else:
            serializer = AlbumSerializer(data=data)
        
        # On permet également l'authentification ET l'accès annonyme
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None, *args, **kwargs):
        try:
            album = Album.objects.get(pk=id)
        except Album.DoesNotExist:
            return Response(
                {"res":"Object with id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        album.delete()
        return Response({"res":"Object deleted!"},
                        status=status.HTTP_200_OK
                        )
    
    def put(self, request, id, *args, **kwargs):
        try:
            album = Album.objects.get(pk=id)
        except Album.DoesNotExist:
            return Response(
                {"res": "Object with id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            'titre': request.data.get('titre'),
            'artiste': request.data.get('artiste'),
        }

        if not data['titre'] or not data['artiste']:
            return Response(
                {"res": "Both 'titre' and 'artiste' fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AlbumSerializer(instance=album, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
