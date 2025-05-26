from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Client(models.Model):
    identifiant = models.CharField(max_length=6, unique=True, editable=False, blank=True)
    genre = models.CharField(max_length=1)  # genre du client
    nom = models.TextField()
    prenom = models.TextField()
    date_creation = models.DateField(auto_now_add=True)  # date de création auto
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)
    telephone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?[\d\s\-]{7,15}$',
                message="Le numéro de téléphone doit être valide (ex: +33612345678 ou 0612345678)"
            )
        ]
    )

    def set_mot_de_passe(self, raw_password):
        self.mot_de_passe = make_password(raw_password)

    def check_mot_de_passe(self, raw_password):
        return check_password(raw_password, self.mot_de_passe)

    def __str__(self):
        return f"{self.identifiant} ({self.date_creation})"

    def __repr__(self):
        return f"<Client: {self.nom} {self.prenom} créé le {self.date_creation}>"

# Create your models here.
