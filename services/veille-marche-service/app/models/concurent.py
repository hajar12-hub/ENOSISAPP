import uuid
from django.db import models

from app.models.marque import Marque
from app.models.sous_categorie import SousCategorie


class Concurent(models.Model):
    """Table de liaison utilisée quand SousCategorie.type == 'groupsInline'.

    Représente un groupe comparatif (ex. "vs MIO"), reliant une marque
    à sa sous-catégorie dans ce contexte de comparaison.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=150)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name="concurents")
    sous_categorie = models.ForeignKey(
        SousCategorie, on_delete=models.CASCADE, related_name="concurents"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "concurents"

    def __str__(self):
        return f"{self.nom} - {self.marque.nom}"
