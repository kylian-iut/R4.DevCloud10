from rest_framework import serializers
from .models import Album

class AlbumSerializer(serializers.ModelSerializer):
	class Meta:
		model = Album
		fields = ["titre", "artiste", "date_de_production","nombre_de_pistes","duree_en_minutes"]
