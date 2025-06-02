from django.db import models

class Album(models.Model):
    titre = models.CharField(max_length=200)  # titre du commentaire
    artiste = models.TextField() # nom de l'artiste
    date_de_production = models.DateTimeField()  # date de publication auto à la mise à jour
    nombre_de_pistes = models.IntegerField()
    duree_en_minutes = models.IntegerField()

    def __str__(self):
        return f"{self.titre} ({self.artiste})"

    def __repr__(self):
        return f"<Album: {self.titre} publié le {self.date_de_production}>"

# Create your models here.
