from rest_framework import serializers

from app.models import Magasin, Visite, Releve


class MagasinSerializer(serializers.ModelSerializer):
    adresse_nom = serializers.CharField(source="adresse.nom", read_only=True, default="")
    secteur_nom = serializers.CharField(source="secteur.nom", read_only=True)
    ville_nom = serializers.CharField(source="ville.nom", read_only=True)
    class Meta:
        model = Magasin
        fields = [
            "id", "nom", "secteur", "secteur_nom", "canal", "ville", "ville_nom", "adresse", "adresse_nom",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "nom": {"required": False, "allow_blank": True},
            "canal": {"required": False, "allow_null": True},
            "adresse": {"required": False, "allow_null": True},
        }


class VisiteSerializer(serializers.ModelSerializer):
    magasin_nom = serializers.CharField(source="magasin.nom", read_only=True)
    def validate(self, attrs):
        sous_categorie = attrs.get("sous_categorie", getattr(self.instance, "sous_categorie", None))
        segment = attrs.get("segment", getattr(self.instance, "segment", None))
        categorie = attrs.get("categorie", getattr(self.instance, "categorie", None))

        if sous_categorie and categorie and sous_categorie.categorie_id != categorie.id:
            raise serializers.ValidationError({
                "sous_categorie": "La sous-catégorie doit appartenir à la catégorie sélectionnée."
            })
        if segment and sous_categorie and segment.sous_categorie_id != sous_categorie.id:
            raise serializers.ValidationError({
                "segment": "Le segment doit appartenir à la sous-catégorie sélectionnée."
            })
        return attrs

    class Meta:
        model = Visite
        fields = [
            "id", "magasin", "magasin_nom", "date_visite", "statut", "categorie", "sous_categorie", "segment", "etape", "created_by", "created_at", "updated_at"
        ]
        # The collection screen never exposes this field: the server owns the
        # visit timestamp to prevent forged or stale visit dates.
        read_only_fields = ["id", "date_visite", "statut", "created_by", "created_at", "updated_at"]


class ReleveSerializer(serializers.ModelSerializer):
    sku_nom = serializers.CharField(source="sku.nom", read_only=True)
    marque_nom = serializers.CharField(source="sku.marque.nom", read_only=True)
    categorie_nom = serializers.SerializerMethodField()
    sous_categorie = serializers.SerializerMethodField()
    sous_categorie_nom = serializers.SerializerMethodField()
    segment_nom = serializers.CharField(source="sku.marque.segment.nom", read_only=True, default="")

    def _sous_categorie(self, obj):
        marque = obj.sku.marque
        if marque.segment_id:
            return marque.segment.sous_categorie
        s_marque = marque.s_marques.select_related("sous_categorie").first()
        if s_marque:
            return s_marque.sous_categorie
        concurrent = marque.concurents.select_related("sous_categorie").first()
        return concurrent.sous_categorie if concurrent else None

    def get_sous_categorie(self, obj):
        sous_categorie = self._sous_categorie(obj)
        return str(sous_categorie.id) if sous_categorie else None

    def get_sous_categorie_nom(self, obj):
        sous_categorie = self._sous_categorie(obj)
        return sous_categorie.nom if sous_categorie else ""

    def get_categorie_nom(self, obj):
        sous_categorie = self._sous_categorie(obj)
        return sous_categorie.categorie.nom if sous_categorie else ""

    class Meta:
        model = Releve
        fields = [
            "id", "visite", "sku", "sku_nom", "marque_nom", "categorie_nom", "sous_categorie", "sous_categorie_nom", "segment_nom",
            "prix_conso_ttc", "prix_detail_ttc",
            "remise_detail_pct", "prix_gros_ttc", "remise_gros_pct",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ReleveBulkItemSerializer(serializers.Serializer):
    """Un item de la création en lot : pas de champ 'visite', il est
    injecté depuis l'URL /releves/?visite={id}."""

    sku = serializers.UUIDField()
    prix_conso_ttc = serializers.FloatField()
    prix_detail_ttc = serializers.FloatField()
    remise_detail_pct = serializers.FloatField(required=False, allow_null=True)
    prix_gros_ttc = serializers.FloatField(required=False, allow_null=True)
    remise_gros_pct = serializers.FloatField(required=False, allow_null=True)


class ReleveBulkCreateSerializer(serializers.Serializer):
    """Payload de POST /veille-marche/releves/ pour créer plusieurs
    relevés d'un coup (étape 'Saisie par blocs de marque')."""

    releves = ReleveBulkItemSerializer(many=True)
