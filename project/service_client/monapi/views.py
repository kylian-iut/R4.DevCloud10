from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializer import ClientSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

def index(request):
    return JsonResponse({"message": "Bienvenue sur mon API !"})

class ClientListApiView(APIView):
    permissions_classes = [IsAuthenticated]
    # On permet l'authentification ET l'accès annonyme
    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            clients = Client.objects.filter(pk=id)
            if not Client:
                return Response({"res": "Object with id does not exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif request.user.is_authenticated:
            clients = Client.objects.all()
        else:
            clients = Client.objects.none()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data

        # Vérifier s'il y a une liste d'objets dans l'instance POST OU un seul
        if isinstance(data, list):
            serializer = ClientSerializer(data=data, many=True)
        else:
            serializer = ClientSerializer(data=data)
        
        # On permet également l'authentification ET l'accès annonyme
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None, *args, **kwargs):
        try:
            client = Client.objects.get(pk=id)
        except Client.DoesNotExist:
            return Response(
                {"res":"Object with id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )
        if not request.user.is_authenticated:
            return Response({"res": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        client.delete()
        return Response({"res":"Object deleted!"},
                        status=status.HTTP_200_OK
                        )
    
    def put(self, request, id, *args, **kwargs):
        try:
            client = Client.objects.get(pk=id)
        except Client.DoesNotExist:
            return Response(
                {"res": "Object with id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data
        mot_de_passe = data.pop('mot_de_passe', None)
        serializer = ClientSerializer(instance=client, data=data, partial=True)
        if not request.user.is_authenticated:
            return Response({"res": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
