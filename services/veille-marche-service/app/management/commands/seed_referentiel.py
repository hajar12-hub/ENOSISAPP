"""Peuple un référentiel minimal cohérent avec le prototype
(Détergent > High Suds direct, Low Suds Liquide groupsInline ;
Papier > Toilet Paper segment), pour pouvoir tester l'API tout de suite.

Usage: python manage.py seed_referentiel
"""

from django.core.management.base import BaseCommand

from app.models import (
    Secteur, Canal, Ville, Adresse, Categorie, SousCategorie,
    Segment, Marque, SMarque, Concurent, SKU,
)


class Command(BaseCommand):
    help = "Peuple un référentiel minimal de test (Détergent + Papier)."

    def handle(self, *args, **options):
        secteur, _ = Secteur.objects.get_or_create(nom="Casablanca Centre")
        Canal.objects.get_or_create(nom="GMS")
        Ville.objects.get_or_create(nom="Casablanca")
        Adresse.objects.get_or_create(nom="Bd Chefchaouni, Ain Sebaa")

        detergent, _ = Categorie.objects.get_or_create(nom="Detergent")
        papier, _ = Categorie.objects.get_or_create(nom="Papier")

        # High Suds : direct
        high_suds, _ = SousCategorie.objects.get_or_create(
            nom="High Suds", categorie=detergent,
            defaults={"type": SousCategorie.Type.DIRECT},
        )
        for nom, concurrent, formats in [
            ("MIO", False, ["225gr", "500gr", "1Kg", "1,5Kg"]),
            ("Magix", True, ["300gr", "500gr", "1Kg"]),
            ("Tide", True, ["225gr", "400gr", "900gr", "1,5Kg"]),
        ]:
            marque, _ = Marque.objects.get_or_create(nom=nom, concurrent=concurrent)
            SMarque.objects.get_or_create(marque=marque, sous_categorie=high_suds)
            for f in formats:
                SKU.objects.get_or_create(nom=f, marque=marque)

        # Low Suds Liquide : groupsInline
        low_suds, _ = SousCategorie.objects.get_or_create(
            nom="Low Suds Liquide", categorie=detergent,
            defaults={"type": SousCategorie.Type.GROUPS_INLINE},
        )
        mio, _ = Marque.objects.get_or_create(nom="MIO", concurrent=False)
        ariel, _ = Marque.objects.get_or_create(nom="ARIEL", concurrent=True)
        Concurent.objects.get_or_create(
            nom="vs MIO", marque=mio, sous_categorie=low_suds
        )
        Concurent.objects.get_or_create(
            nom="vs MIO", marque=ariel, sous_categorie=low_suds
        )
        for f in ["1L", "1,8L", "3L"]:
            SKU.objects.get_or_create(nom=f, marque=mio)
            SKU.objects.get_or_create(nom=f, marque=ariel)

        # Toilet Paper : segment
        toilet_paper, _ = SousCategorie.objects.get_or_create(
            nom="Toilet Paper", categorie=papier,
            defaults={"type": SousCategorie.Type.SEGMENT},
        )
        deux_plis, _ = Segment.objects.get_or_create(
            nom="2 PLIS", sous_categorie=toilet_paper
        )
        papillon, _ = Marque.objects.get_or_create(
            nom="Papillon", concurrent=False, segment=deux_plis
        )
        for f in ["4", "12"]:
            SKU.objects.get_or_create(nom=f, marque=papillon)

        self.stdout.write(self.style.SUCCESS("Référentiel de test créé avec succès."))
