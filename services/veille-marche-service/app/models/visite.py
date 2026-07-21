import uuid
from django.db import models

from app.models.magasin import Magasin
from app.models.categorie import Categorie
from app.models.sous_categorie import SousCategorie
from app.models.segment import Segment


class Visite(models.Model):
    class Statut(models.TextChoices):
        BROUILLON = "brouillon", "Brouillon"
        SOUMISE = "soumise", "Soumise"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, related_name="visites")
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="visites", null=True, blank=True)
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.PROTECT, related_name="visites", null=True, blank=True)
    segment = models.ForeignKey(Segment, on_delete=models.PROTECT, related_name="visites", null=True, blank=True)
    etape = models.CharField(max_length=32, default="visite")
    # Nullable uniquement pour préserver les visites historiques créées avant
    # l'introduction de la propriété utilisateur. Les nouvelles visites sont
    # toujours renseignées par la vue.
    created_by = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="veille_marche_visites", null=True, blank=True)
    date_visite = models.DateTimeField()
    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.BROUILLON
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "visites"
        ordering = ["-date_visite"]

    def __str__(self):
        return f"Visite {self.magasin.nom} - {self.date_visite:%Y-%m-%d}"
