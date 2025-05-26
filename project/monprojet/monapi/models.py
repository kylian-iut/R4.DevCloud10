from django.db import models

class Commentaire(models.Model):
    titre = models.CharField(max_length=200)  # titre du commentaire
    commentaire = models.TextField()           # texte du commentaire
    date_publication = models.DateField(auto_now=True)  # date de publication auto à la mise à jour

    def __str__(self):
        return f"{self.titre} ({self.date_publication})"

    def __repr__(self):
        return f"<Commentaire: {self.titre} publié le {self.date_publication}>"

# Create your models here.
