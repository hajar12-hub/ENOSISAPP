from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def user_data(user):
    return {"id": user.id, "email": user.email, "first_name": user.first_name, "last_name": user.last_name}


def tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh), "user": user_data(user)}


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Un compte existe déjà avec cette adresse e-mail.")
        return value.lower()

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Les mots de passe ne correspondent pas."})
        candidate = User(username=attrs["email"], email=attrs["email"], first_name=attrs["first_name"], last_name=attrs["last_name"])
        try:
            validate_password(attrs["password"], candidate)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": list(error.messages)})
        return attrs


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    user = User.objects.create_user(username=data["email"], email=data["email"], first_name=data["first_name"], last_name=data["last_name"], password=data["password"])
    return Response(tokens_for(user), status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = str(request.data.get("email", "")).strip().lower()
    password = request.data.get("password", "")
    if not email or not password:
        return Response({"detail": "L’e-mail et le mot de passe sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(email__iexact=email).first()
    if not user or not user.is_active or not user.check_password(password):
        return Response({"detail": "Votre e-mail ou votre mot de passe est incorrect."}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(tokens_for(user))


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh(request):
    value = request.data.get("refresh")
    if not value:
        return Response({"detail": "Le jeton de rafraîchissement est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        old = RefreshToken(value)
        user = User.objects.get(id=old["user_id"], is_active=True)
        old.blacklist()
    except (TokenError, User.DoesNotExist):
        return Response({"detail": "Votre session a expiré. Veuillez vous reconnecter."}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(tokens_for(user))


@api_view(["POST"])
@permission_classes([AllowAny])
def logout(request):
    value = request.data.get("refresh")
    if not value:
        return Response({"detail": "Le jeton de rafraîchissement est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        RefreshToken(value).blacklist()
    except Exception:
        pass
    return Response({"detail": "Déconnexion réussie."})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({"user": user_data(request.user)})


@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    if not request.data.get("email"):
        return Response({"detail": "L’adresse e-mail est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Si un compte existe avec cet e-mail, les instructions ont été envoyées."})
