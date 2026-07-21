import uuid
from django.db import models

from app.models.secteur import Secteur
from app.models.canal import Canal
from app.models.ville import Ville
from app.models.adresse import Adresse


class Magasin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Le workflow démarre volontairement avec le seul couple secteur / ville.
    # Les autres informations d'un point de vente sont enrichies ultérieurement.
    nom = models.CharField(max_length=255, blank=True)
    secteur = models.ForeignKey(Secteur, on_delete=models.PROTECT, related_name="magasins")
    canal = models.ForeignKey(Canal, on_delete=models.PROTECT, related_name="magasins", null=True, blank=True)
    ville = models.ForeignKey(Ville, on_delete=models.PROTECT, related_name="magasins")
    adresse = models.ForeignKey(Adresse, on_delete=models.PROTECT, related_name="magasins", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "magasins"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom} ({self.ville})"
