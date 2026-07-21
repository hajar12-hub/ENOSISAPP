"""Logique métier de la collecte terrain (Magasin, Visite, Relevé).

Le point métier central ici est la soumission en lot des relevés d'une
visite (étape "Saisie par blocs de marque" du wizard : un superviseur
envoie tous les prix d'une visite en un seul appel), avec les règles
de validation associées (visite non déjà soumise, au moins un relevé
rempli).
"""

from django.db import transaction

from app.exceptions import VisiteDejaSoumiseError, ReleveVideError
from app.models import Visite, SKU
from app.repositories.collecte import MagasinRepository, VisiteRepository, ReleveRepository


class CollecteService:
    magasins = MagasinRepository
    visites_repo = VisiteRepository
    releves_repo = ReleveRepository

    @staticmethod
    def list_magasins():
        return MagasinRepository.list_all()

    @staticmethod
    def list_visites(magasin_id=None, statut=None):
        return VisiteRepository.list_all(magasin_id=magasin_id, statut=statut)

    @staticmethod
    def list_releves(visite_id=None):
        return ReleveRepository.list_all(visite_id=visite_id)

    @staticmethod
    @transaction.atomic
    def sauvegarder_brouillon(visite_id, releves_data, user):
        visite = VisiteRepository.get_by_id(visite_id)
        if visite.created_by_id != user.id:
            raise PermissionError("Cette visite ne vous appartient pas.")
        if visite.statut == Visite.Statut.SOUMISE:
            raise VisiteDejaSoumiseError()
        return CollecteService._enregistrer_releves(visite, releves_data)

    @staticmethod
    @transaction.atomic
    def soumettre_releves_en_lot(visite_id, releves_data, user):
        """Crée plusieurs relevés pour une visite en une seule transaction,
        et passe la visite au statut 'soumise'.

        releves_data: liste de dicts avec au minimum ku_id, prix_conso_ttc,
        prix_detail_ttc (et optionnellement remise_detail_pct,
        prix_gros_ttc, remise_gros_pct).
        """
        visite = VisiteRepository.get_by_id(visite_id)

        if visite.created_by_id != user.id:
            raise PermissionError("Cette visite ne vous appartient pas.")

        if visite.statut == Visite.Statut.SOUMISE:
            raise VisiteDejaSoumiseError()

        lignes_remplies = [
            r for r in releves_data
            if r.get("prix_conso_ttc") and r.get("prix_detail_ttc")
        ]
        if not lignes_remplies:
            raise ReleveVideError()

        releves_crees = CollecteService._enregistrer_releves(visite, releves_data)

        visite.statut = Visite.Statut.SOUMISE
        visite.save(update_fields=["statut", "updated_at"])

        return releves_crees

    @staticmethod
    def _enregistrer_releves(visite, releves_data):
        sku_ids = [str(item["sku_id"]) for item in releves_data]
        if SKU.objects.filter(id__in=sku_ids).count() != len(set(sku_ids)):
            raise ValueError("Un SKU transmis n'existe pas.")
        return ReleveRepository.replace_for_visite(visite, releves_data)
