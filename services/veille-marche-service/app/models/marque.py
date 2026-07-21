import uuid
from django.db import models

from app.models.segment import Segment


class Marque(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=150)
    concurrent = models.BooleanField(default=False)
    # Rempli uniquement quand la sous-catégorie parente est de type "segment"
    segment = models.ForeignKey(
        Segment,
        on_delete=models.CASCADE,
        related_name="marques",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "marques"
        ordering = ["nom"]

    def __str__(self):
        return self.nom
