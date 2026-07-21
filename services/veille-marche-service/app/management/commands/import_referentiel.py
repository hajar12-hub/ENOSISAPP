"""Importe le référentiel produit depuis le classeur livré dans ``data/``.

Le format est celui du Price Ladder : les marques sont sur la deuxième ligne
et leurs SKU sur la troisième. La commande est idempotente et peut donc être
rejouée après chaque déploiement sans dupliquer les références.
"""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from openpyxl import load_workbook

from app.models import Categorie, Marque, Segment, SKU, SMarque, SousCategorie


DATA_FILE = Path(__file__).resolve().parents[5] / "data" / "Price ladder PAPER Tracker (1) (1).xlsx"


class Command(BaseCommand):
    help = "Importe les catégories, sous-catégories, segments, marques et SKU depuis data/."

    def handle(self, *args, **options):
        if not DATA_FILE.exists():
            raise CommandError(f"Classeur introuvable : {DATA_FILE}")

        workbook = load_workbook(DATA_FILE, read_only=True, data_only=True)
        detergent, _ = Categorie.objects.get_or_create(nom="Detergent")
        paper, _ = Categorie.objects.get_or_create(nom="Papier")

        self._import_high_suds(workbook["Sheet1"], detergent)
        for sheet_name, sous_categorie_name in {
            "TOILET PAPER ": "Toilet Paper",
            "FACIAL TISSUES": "Facial Tissues",
            "PAPER TOWEL": "Paper Towel",
        }.items():
            self._import_paper_sheet(workbook[sheet_name], paper, sous_categorie_name)

        self.stdout.write(self.style.SUCCESS("Référentiel importé depuis data/ avec succès."))

    @staticmethod
    def _text(value):
        return str(value).strip() if value is not None and str(value).strip() else None

    def _import_high_suds(self, sheet, categorie):
        sous_categorie, _ = SousCategorie.objects.get_or_create(
            nom="High Suds",
            categorie=categorie,
            defaults={"type": SousCategorie.Type.DIRECT},
        )
        current_brand = None
        for column in range(1, sheet.max_column + 1):
            brand_name = self._text(sheet.cell(2, column).value)
            if brand_name:
                current_brand = brand_name
            sku_name = self._text(sheet.cell(3, column).value)
            if not current_brand or not sku_name:
                continue
            marque, _ = Marque.objects.get_or_create(
                nom=current_brand,
                defaults={"concurrent": current_brand.upper() != "MIO"},
            )
            SMarque.objects.get_or_create(marque=marque, sous_categorie=sous_categorie)
            SKU.objects.get_or_create(nom=sku_name, marque=marque)

    def _import_paper_sheet(self, sheet, categorie, sous_categorie_name):
        sous_categorie, _ = SousCategorie.objects.get_or_create(
            nom=sous_categorie_name,
            categorie=categorie,
            defaults={"type": SousCategorie.Type.SEGMENT},
        )
        current_segment = None
        current_brand = None
        for column in range(1, sheet.max_column + 1):
            segment_name = self._text(sheet.cell(1, column).value)
            if segment_name:
                current_segment = segment_name
            brand_name = self._text(sheet.cell(2, column).value)
            if brand_name and brand_name.lower() != "paper":
                current_brand = brand_name
            sku_name = self._text(sheet.cell(3, column).value)
            if not current_segment or not current_brand or not sku_name:
                continue
            segment, _ = Segment.objects.get_or_create(
                nom=current_segment, sous_categorie=sous_categorie
            )
            marque, _ = Marque.objects.get_or_create(
                nom=current_brand,
                segment=segment,
                defaults={"concurrent": current_brand.upper() != "PAPILLON"},
            )
            SKU.objects.get_or_create(nom=sku_name, marque=marque)
