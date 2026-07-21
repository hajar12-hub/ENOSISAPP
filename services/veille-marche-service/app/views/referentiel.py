from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

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
from app.serializers.referentiel import (
    SecteurSerializer,
    CanalSerializer,
    VilleSerializer,
    AdresseSerializer,
    CategorieSerializer,
    SousCategorieSerializer,
    SegmentSerializer,
    MarqueSerializer,
    SMarqueSerializer,
    ConcurentSerializer,
    SKUSerializer,
)
from app.services.referentiel_service import ReferentielService


class SecteurViewSet(viewsets.ModelViewSet):
    queryset = Secteur.objects.all()
    serializer_class = SecteurSerializer
    permission_classes = [IsAuthenticated]


class CanalViewSet(viewsets.ModelViewSet):
    queryset = Canal.objects.all()
    serializer_class = CanalSerializer
    permission_classes = [IsAuthenticated]


class VilleViewSet(viewsets.ModelViewSet):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer
    permission_classes = [IsAuthenticated]


class AdresseViewSet(viewsets.ModelViewSet):
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer
    permission_classes = [IsAuthenticated]


class CategorieViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Lecture seule pour l'instant, comme prévu au cahier des charges."""

    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticated]


class SousCategorieViewSet(viewsets.ModelViewSet):
    serializer_class = SousCategorieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReferentielService.list_sous_categories(
            categorie_id=self.request.query_params.get("categorie")
        )


class SegmentViewSet(viewsets.ModelViewSet):
    serializer_class = SegmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReferentielService.list_segments(
            sous_categorie_id=self.request.query_params.get("sous_categorie")
        )


class SMarqueViewSet(viewsets.ModelViewSet):
    serializer_class = SMarqueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReferentielService.list_s_marques(
            sous_categorie_id=self.request.query_params.get("sous_categorie")
        )


class ConcurentViewSet(viewsets.ModelViewSet):
    serializer_class = ConcurentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReferentielService.list_concurents(
            sous_categorie_id=self.request.query_params.get("sous_categorie")
        )


class MarqueViewSet(viewsets.ModelViewSet):
    serializer_class = MarqueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        params = self.request.query_params
        return ReferentielService.list_marques(
            segment_id=params.get("segment"),
            s_marque_id=params.get("s_marque"),
            concurent_id=params.get("concurent"),
            sous_categorie_id=params.get("sous_categorie"),
        )


class SKUViewSet(viewsets.ModelViewSet):
    serializer_class = SKUSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReferentielService.skus.list_all(
            marque_id=self.request.query_params.get("marque")
        )
