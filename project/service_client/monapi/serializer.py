import random
import string
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["identifiant", "mot_de_passe", "genre", "nom", "prenom", "email", "telephone", "date_creation"]

    def generate_identifiant(self, length=6):
        """Fonction pour générer un identifiant aléatoire de 6 caractères"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def create(self, validated_data):
        identifiant = self.generate_identifiant()  # Appel de la méthode pour générer un identifiant
        validated_data['identifiant'] = identifiant
        mot_de_passe = validated_data.pop('mot_de_passe', None)
        
        # Optionnel : Définir automatiquement la date de création
        validated_data['date_creation'] = timezone.now()
        
        client = Client(**validated_data)
        
        if mot_de_passe:
            client.mot_de_passe = make_password(mot_de_passe)
            
        client.save()
        return client

    def update(self, instance, validated_data):
        mot_de_passe = validated_data.pop('mot_de_passe', None)
        # Mettre à jour les autres champs de l'instance
        instance = super().update(instance, validated_data)
        
        if mot_de_passe:
            instance.mot_de_passe = make_password(mot_de_passe)
        
        instance.save()
        return instance
