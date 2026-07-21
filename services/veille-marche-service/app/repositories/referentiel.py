"""Couche d'accès aux données pour le référentiel produit.

Chaque repository encapsule les requêtes ORM pour une entité donnée,
afin que les services n'accèdent jamais directement au queryset Django.
"""

from django.db import models

from app.models import (
    Secteur,
    Canal,
    Ville,
    Adresse,
    Categorie,
    SousCategorie,
    Segment,
    Marque,
    SMarque,
    Concurent,
    SKU,
)


class SecteurRepository:
    @staticmethod
    def list_all():
        return Secteur.objects.all()

    @staticmethod
    def get_by_id(secteur_id):
        return Secteur.objects.get(id=secteur_id)


class CanalRepository:
    @staticmethod
    def list_all():
        return Canal.objects.all()

    @staticmethod
    def get_by_id(canal_id):
        return Canal.objects.get(id=canal_id)


class VilleRepository:
    @staticmethod
    def list_all():
        return Ville.objects.all()

    @staticmethod
    def get_by_id(ville_id):
        return Ville.objects.get(id=ville_id)


class AdresseRepository:
    @staticmethod
    def list_all():
        return Adresse.objects.all()

    @staticmethod
    def get_by_id(adresse_id):
        return Adresse.objects.get(id=adresse_id)


class CategorieRepository:
    @staticmethod
    def list_all():
        return Categorie.objects.all()

    @staticmethod
    def get_by_id(categorie_id):
        return Categorie.objects.get(id=categorie_id)


class SousCategorieRepository:
    @staticmethod
    def list_all(categorie_id=None):
        qs = SousCategorie.objects.select_related("categorie").all()
        if categorie_id:
            qs = qs.filter(categorie_id=categorie_id)
        return qs

    @staticmethod
    def get_by_id(sous_categorie_id):
        return SousCategorie.objects.select_related("categorie").get(id=sous_categorie_id)


class SegmentRepository:
    @staticmethod
    def list_all(sous_categorie_id=None):
        qs = Segment.objects.select_related("sous_categorie").all()
        if sous_categorie_id:
            qs = qs.filter(sous_categorie_id=sous_categorie_id)
        return qs

    @staticmethod
    def get_by_id(segment_id):
        return Segment.objects.select_related("sous_categorie").get(id=segment_id)


class SMarqueRepository:
    @staticmethod
    def list_all(sous_categorie_id=None):
        qs = SMarque.objects.select_related("marque", "sous_categorie").all()
        if sous_categorie_id:
            qs = qs.filter(sous_categorie_id=sous_categorie_id)
        return qs

    @staticmethod
    def get_by_id(s_marque_id):
        return SMarque.objects.select_related("marque", "sous_categorie").get(id=s_marque_id)


class ConcurentRepository:
    @staticmethod
    def list_all(sous_categorie_id=None):
        qs = Concurent.objects.select_related("marque", "sous_categorie").all()
        if sous_categorie_id:
            qs = qs.filter(sous_categorie_id=sous_categorie_id)
        return qs

    @staticmethod
    def get_by_id(concurent_id):
        return Concurent.objects.select_related("marque", "sous_categorie").get(id=concurent_id)


class MarqueRepository:
    @staticmethod
    def list_all(segment_id=None, s_marque_id=None, concurent_id=None, sous_categorie_id=None):
        qs = Marque.objects.select_related("segment").all()
        if segment_id:
            qs = qs.filter(segment_id=segment_id)
        if s_marque_id:
            qs = qs.filter(s_marques__id=s_marque_id)
        if concurent_id:
            qs = qs.filter(concurents__id=concurent_id)
        if sous_categorie_id:
            qs = qs.filter(
                models.Q(segment__sous_categorie_id=sous_categorie_id)
                | models.Q(s_marques__sous_categorie_id=sous_categorie_id)
                | models.Q(concurents__sous_categorie_id=sous_categorie_id)
            )
        return qs.distinct()

    @staticmethod
    def get_by_id(marque_id):
        return Marque.objects.select_related("segment").get(id=marque_id)


class SKURepository:
    @staticmethod
    def list_all(marque_id=None):
        qs = SKU.objects.select_related("marque").all()
        if marque_id:
            qs = qs.filter(marque_id=marque_id)
        return qs

    @staticmethod
    def get_by_id(sku_id):
        return SKU.objects.select_related("marque").get(id=sku_id)
