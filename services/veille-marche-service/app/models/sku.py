import uuid
from django.db import models

from app.models.marque import Marque


class SKU(models.Model):
    """Représente un SKU (ex. '225gr', '500gr') rattaché à une marque."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    # Présent dans la base PostgreSQL historique ; une chaîne vide garde la
    # compatibilité des anciennes lignes dont le format porte déjà l'unité.
    unite = models.CharField(max_length=32, blank=True, default="")
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name="skus")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "skus"
        verbose_name = "SKU"
        verbose_name_plural = "SKUs"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.marque.nom} {self.nom}"
