"""Couche d'accès aux données pour la collecte terrain (Magasin, Visite, Relevé)."""

from app.models import Magasin, Visite, Releve


class MagasinRepository:
    @staticmethod
    def list_all():
        return Magasin.objects.select_related("secteur", "canal", "ville", "adresse").all()

    @staticmethod
    def get_by_id(magasin_id):
        return Magasin.objects.select_related(
            "secteur", "canal", "ville", "adresse"
        ).get(id=magasin_id)


class VisiteRepository:
    @staticmethod
    def list_all(magasin_id=None, statut=None):
        qs = Visite.objects.select_related("magasin", "categorie", "sous_categorie", "segment").all()
        if magasin_id:
            qs = qs.filter(magasin_id=magasin_id)
        if statut:
            qs = qs.filter(statut=statut)
        return qs

    @staticmethod
    def get_by_id(visite_id):
        return Visite.objects.select_related("magasin", "categorie", "sous_categorie", "segment").get(id=visite_id)


class ReleveRepository:
    @staticmethod
    def list_all(visite_id=None):
        qs = Releve.objects.select_related("visite", "sku", "sku__marque").all()
        if visite_id:
            qs = qs.filter(visite_id=visite_id)
        return qs

    @staticmethod
    def get_by_id(releve_id):
        return Releve.objects.select_related("visite", "sku", "sku__marque").get(id=releve_id)

    @staticmethod
    def replace_for_visite(visite, releves_data):
        """Crée plusieurs relevés en une seule requête (étape 'Saisie par
        blocs de marque' du wizard : un seul appel pour tous les SKU
        d'une visite)."""
        existing = {str(item.sku_id): item for item in Releve.objects.filter(visite=visite)}
        result = []
        for data in releves_data:
            sku_id = data.pop("sku_id")
            releve, _ = Releve.objects.update_or_create(
                visite=visite,
                sku_id=sku_id,
                defaults=data,
            )
            result.append(releve)
        return result
