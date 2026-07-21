import uuid
from django.db import models

from app.models.marque import Marque
from app.models.sous_categorie import SousCategorie


class SMarque(models.Model):
    """Table de liaison utilisée quand SousCategorie.type == 'direct'."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name="s_marques")
    sous_categorie = models.ForeignKey(
        SousCategorie, on_delete=models.CASCADE, related_name="s_marques"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "s_marques"
        unique_together = ("marque", "sous_categorie")

    def __str__(self):
        return f"{self.marque.nom} -> {self.sous_categorie.nom}"
