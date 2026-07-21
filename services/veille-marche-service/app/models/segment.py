import uuid
from django.db import models

from app.models.sous_categorie import SousCategorie


class Segment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=150)
    sous_categorie = models.ForeignKey(
        SousCategorie, on_delete=models.CASCADE, related_name="segments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "segments"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom} ({self.sous_categorie.nom})"
