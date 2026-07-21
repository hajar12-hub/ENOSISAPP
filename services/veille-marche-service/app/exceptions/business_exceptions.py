from rest_framework.exceptions import APIException
from rest_framework import status


class SousCategorieTypeMismatchError(APIException):
    """Levée quand on essaie d'associer une marque à une sous-catégorie
    via un chemin (direct / segment / groupsInline) qui ne correspond
    pas au type déclaré de cette sous-catégorie."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Le type de la sous-catégorie ne correspond pas au chemin utilisé."
    default_code = "sous_categorie_type_mismatch"


class VisiteDejaSoumiseError(APIException):
    """Levée quand on tente de modifier les relevés d'une visite déjà soumise."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = "Cette visite est déjà soumise, ses relevés ne sont plus modifiables."
    default_code = "visite_deja_soumise"


class ReleveVideError(APIException):
    """Levée quand on tente de soumettre une visite sans aucun relevé rempli."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Impossible de soumettre une visite sans aucun relevé rempli."
    default_code = "releve_vide"
