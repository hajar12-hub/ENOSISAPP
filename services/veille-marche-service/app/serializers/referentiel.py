from rest_framework import serializers

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


class SecteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secteur
        fields = ["id", "nom", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class CanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canal
        fields = ["id", "nom", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = ["id", "nom", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        fields = ["id", "nom", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ["id", "nom", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class SousCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousCategorie
        fields = ["id", "nom", "categorie", "type", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = ["id", "nom", "sous_categorie", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class MarqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marque
        fields = [
            "id", "nom", "concurrent", "segment", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class SMarqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMarque
        fields = ["id", "marque", "sous_categorie", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ConcurentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concurent
        fields = ["id", "nom", "marque", "sous_categorie", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ["id", "nom", "unite", "marque", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
