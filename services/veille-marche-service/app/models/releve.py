import uuid
from django.db import models

from app.models.visite import Visite
from app.models.sku import SKU


class Releve(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visite = models.ForeignKey(Visite, on_delete=models.CASCADE, related_name="releves")
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT, related_name="releves")
    prix_conso_ttc = models.FloatField()
    prix_detail_ttc = models.FloatField()
    remise_detail_pct = models.FloatField(null=True, blank=True)
    prix_gros_ttc = models.FloatField(null=True, blank=True)
    remise_gros_pct = models.FloatField(null=True, blank=True)
    promotion = models.CharField(max_length=255, blank=True, default="")
    commentaire = models.TextField(blank=True, default="")
    photo_url = models.URLField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "releves"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["visite", "sku"], name="unique_releve_par_visite_sku"),
        ]

    def __str__(self):
        return f"Relevé {self.sku} - {self.visite}"
