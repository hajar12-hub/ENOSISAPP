from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperviseurOrReadOnly(BasePermission):
    """Autorise la lecture à tout utilisateur authentifié, mais réserve
    l'écriture (création de relevés) au rôle superviseur.

    Le payload JWT (émis par auth-service) est attendu avec un champ
    'user_roles' contenant la liste des rôles de l'utilisateur, comme
    documenté pour les autres microservices de ENOSISAPP.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        user_roles = getattr(request.user, "user_roles", []) or []
        return "superviseur" in [r.lower() for r in user_roles]
