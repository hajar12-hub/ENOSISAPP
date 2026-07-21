"""Logique métier du référentiel produit (Catégorie -> Sous-catégorie
-> Segment/SMarque/Concurent -> Marque -> SKU).

Reste volontairement simple pour cette V1 (Mois 1 - Collecte) : la
validation de cohérence entre SousCategorie.type et le chemin utilisé
(direct/segment/groupsInline) est le principal point métier à ce stade.
"""

from app.exceptions import SousCategorieTypeMismatchError
from app.models import SousCategorie
from app.repositories.referentiel import (
    SecteurRepository,
    CanalRepository,
    VilleRepository,
    AdresseRepository,
    CategorieRepository,
    SousCategorieRepository,
    SegmentRepository,
    SMarqueRepository,
    ConcurentRepository,
    MarqueRepository,
    SKURepository,
)


class ReferentielService:
    # --- Lecture simple, déléguée directement aux repositories ---
    secteurs = SecteurRepository
    canaux = CanalRepository
    villes = VilleRepository
    adresses = AdresseRepository
    categories = CategorieRepository
    skus = SKURepository

    @staticmethod
    def list_sous_categories(categorie_id=None):
        return SousCategorieRepository.list_all(categorie_id=categorie_id)

    @staticmethod
    def list_segments(sous_categorie_id=None):
        return SegmentRepository.list_all(sous_categorie_id=sous_categorie_id)

    @staticmethod
    def list_s_marques(sous_categorie_id=None):
        return SMarqueRepository.list_all(sous_categorie_id=sous_categorie_id)

    @staticmethod
    def list_concurents(sous_categorie_id=None):
        return ConcurentRepository.list_all(sous_categorie_id=sous_categorie_id)

    @staticmethod
    def list_marques(segment_id=None, s_marque_id=None, concurent_id=None, sous_categorie_id=None):
        return MarqueRepository.list_all(
            segment_id=segment_id, s_marque_id=s_marque_id, concurent_id=concurent_id,
            sous_categorie_id=sous_categorie_id,
        )

    # --- Règles métier ---
    @staticmethod
    def valider_type_sous_categorie(sous_categorie_id, type_attendu):
        """Vérifie que la sous-catégorie est bien du type attendu avant
        de créer un Segment, un SMarque ou un Concurent dessus."""
        sous_categorie = SousCategorieRepository.get_by_id(sous_categorie_id)
        if sous_categorie.type != type_attendu:
            raise SousCategorieTypeMismatchError(
                detail=(
                    f"La sous-catégorie '{sous_categorie.nom}' est de type "
                    f"'{sous_categorie.type}', pas '{type_attendu}'."
                )
            )
        return sous_categorie

    @staticmethod
    def creer_s_marque(marque_id, sous_categorie_id):
        ReferentielService.valider_type_sous_categorie(
            sous_categorie_id, SousCategorie.Type.DIRECT
        )
        from app.models import SMarque

        return SMarque.objects.create(marque_id=marque_id, sous_categorie_id=sous_categorie_id)

    @staticmethod
    def creer_concurent(nom, marque_id, sous_categorie_id):
        ReferentielService.valider_type_sous_categorie(
            sous_categorie_id, SousCategorie.Type.GROUPS_INLINE
        )
        from app.models import Concurent

        return Concurent.objects.create(
            nom=nom, marque_id=marque_id, sous_categorie_id=sous_categorie_id
        )

    @staticmethod
    def creer_segment(nom, sous_categorie_id):
        ReferentielService.valider_type_sous_categorie(
            sous_categorie_id, SousCategorie.Type.SEGMENT
        )
        from app.models import Segment

        return Segment.objects.create(nom=nom, sous_categorie_id=sous_categorie_id)
