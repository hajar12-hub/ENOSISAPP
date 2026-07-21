from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from app.exceptions import VisiteDejaSoumiseError
from app.models import Magasin, Visite
from app.serializers.collecte import (
    MagasinSerializer,
    VisiteSerializer,
    ReleveSerializer,
    ReleveBulkCreateSerializer,
)
from app.services.collecte_service import CollecteService


class MagasinViewSet(viewsets.ModelViewSet):
    queryset = Magasin.objects.select_related("secteur", "canal", "ville", "adresse").all()
    serializer_class = MagasinSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Magasin.objects.select_related("secteur", "canal", "ville", "adresse").all()


class VisiteViewSet(viewsets.ModelViewSet):
    serializer_class = VisiteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(date_visite=timezone.now(), created_by=self.request.user)

    def get_queryset(self):
        queryset = CollecteService.list_visites(
            magasin_id=self.request.query_params.get("magasin"),
            statut=self.request.query_params.get("statut"),
        )
        return queryset.filter(created_by=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.statut == Visite.Statut.SOUMISE:
            raise VisiteDejaSoumiseError()
        serializer.save()

    def perform_destroy(self, instance):
        if instance.statut == Visite.Statut.SOUMISE:
            raise VisiteDejaSoumiseError()
        instance.delete()


class ReleveViewSet(viewsets.ModelViewSet):
    """GET liste les relevés (filtrables par ?visite={id}).

    POST accepte soit un relevé unique (comportement ModelViewSet
    standard), soit un lot via {"releves": [...]}, pour matcher l'étape
    "Saisie par blocs de marque" du wizard : tous les prix d'une visite
    envoyés en un seul appel.
    """

    serializer_class = ReleveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CollecteService.list_releves(
            visite_id=self.request.query_params.get("visite")
        ).filter(visite__created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        if "releves" in request.data:
            return self._bulk_create(request)
        raise ValidationError({
            "detail": "Utilisez le format {\"releves\": [...]} avec le paramètre ?visite={id}."
        })

    def _assert_modifiable(self, releve):
        if releve.visite.created_by_id != self.request.user.id:
            raise PermissionDenied("Cette visite ne vous appartient pas.")
        if releve.visite.statut == Visite.Statut.SOUMISE:
            raise VisiteDejaSoumiseError()

    def perform_update(self, serializer):
        self._assert_modifiable(serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        self._assert_modifiable(instance)
        instance.delete()

    def _bulk_create(self, request):
        visite_id = request.query_params.get("visite")
        if not visite_id:
            return Response(
                {"detail": "Le paramètre ?visite={id} est requis pour la création en lot."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bulk_serializer = ReleveBulkCreateSerializer(data=request.data)
        bulk_serializer.is_valid(raise_exception=True)

        releves_data = []
        for item in bulk_serializer.validated_data["releves"]:
            data = dict(item)
            data["sku_id"] = data.pop("sku")
            releves_data.append(data)

        try:
            if self.request.query_params.get("draft") == "1":
                releves_crees = CollecteService.sauvegarder_brouillon(
                    visite_id=visite_id, releves_data=releves_data, user=request.user
                )
            else:
                releves_crees = CollecteService.soumettre_releves_en_lot(
                    visite_id=visite_id, releves_data=releves_data, user=request.user
                )
        except PermissionError as error:
            raise PermissionDenied(str(error)) from error
        output = ReleveSerializer(releves_crees, many=True)
        return Response(output.data, status=status.HTTP_201_CREATED)
