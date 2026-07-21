import uuid
from django.db import models

from app.models.categorie import Categorie


class SousCategorie(models.Model):
    class Type(models.TextChoices):
        DIRECT = "direct", "Direct"
        SEGMENT = "segment", "Segment"
        GROUPS_INLINE = "groupsInline", "Groupes comparatifs"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=150)
    categorie = models.ForeignKey(
        Categorie, on_delete=models.CASCADE, related_name="sous_categories"
    )
    type = models.CharField(max_length=20, choices=Type.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sous_categories"
        ordering = ["nom"]
        verbose_name_plural = "sous-catégories"

    def __str__(self):
        return f"{self.nom} ({self.categorie.nom})"
