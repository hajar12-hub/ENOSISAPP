from django.http import JsonResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from app.views.referentiel import (
    SecteurViewSet,
    CanalViewSet,
    VilleViewSet,
    AdresseViewSet,
    CategorieViewSet,
    SousCategorieViewSet,
    SegmentViewSet,
    SMarqueViewSet,
    ConcurentViewSet,
    MarqueViewSet,
    SKUViewSet,
)
from app.views.collecte import MagasinViewSet, VisiteViewSet, ReleveViewSet
from app import auth_views

router = DefaultRouter()
router.register(r"secteurs", SecteurViewSet, basename="secteur")
router.register(r"canaux", CanalViewSet, basename="canal")
router.register(r"villes", VilleViewSet, basename="ville")
router.register(r"adresses", AdresseViewSet, basename="adresse")
router.register(r"categories", CategorieViewSet, basename="categorie")
router.register(r"sous-categories", SousCategorieViewSet, basename="sous-categorie")
router.register(r"segments", SegmentViewSet, basename="segment")
router.register(r"s-marques", SMarqueViewSet, basename="s-marque")
router.register(r"concurents", ConcurentViewSet, basename="concurent")
router.register(r"marques", MarqueViewSet, basename="marque")
router.register(r"skus", SKUViewSet, basename="sku")
router.register(r"magasins", MagasinViewSet, basename="magasin")
router.register(r"visites", VisiteViewSet, basename="visite")
router.register(r"releves", ReleveViewSet, basename="releve")


@api_view(["GET"])
@permission_classes([AllowAny])
def health(_request):
    return JsonResponse({"status": "ok", "service": "veille-marche-service"})


urlpatterns = [
    path("auth/register/", auth_views.register),
    path("auth/login/", auth_views.login),
    path("auth/refresh/", auth_views.refresh),
    path("auth/logout/", auth_views.logout),
    path("auth/me/", auth_views.me),
    path("auth/forgot-password/", auth_views.forgot_password),
    path("health", health),
    path("veille-marche/", include(router.urls)),
]
