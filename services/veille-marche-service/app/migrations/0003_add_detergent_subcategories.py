from django.db import migrations


def add_detergent_subcategories(apps, schema_editor):
    Categorie = apps.get_model("app", "Categorie")
    SousCategorie = apps.get_model("app", "SousCategorie")
    Marque = apps.get_model("app", "Marque")
    SMarque = apps.get_model("app", "SMarque")
    SKU = apps.get_model("app", "SKU")

    detergent = Categorie.objects.filter(nom="Detergent").order_by("created_at").first()
    if not detergent:
        detergent = Categorie.objects.create(nom="Detergent")
    subcategories = {}
    for nom, type_ in (
        ("High Suds", "direct"),
        ("Low Suds Liquide", "groupsInline"),
        ("Liquide Vaisselle", "direct"),
        ("Poudre Matic", "direct"),
    ):
        subcategory = SousCategorie.objects.filter(nom=nom, categorie=detergent).order_by("created_at").first()
        subcategories[nom] = subcategory or SousCategorie.objects.create(
            nom=nom, categorie=detergent, type=type_
        )

    references = {
        "Liquide Vaisselle": {
            "MIO": ["300ml", "750ml", "1250ml"],
            "ONI": ["300ml", "750ml", "1250ml"],
            "MAXIS": ["300ml", "750ml", "1250ml"],
            "ARIEL": ["900ml"],
        },
        "Poudre Matic": {
            "MIO": ["400 GR", "750+150GR"],
            "ARIEL": ["400gr", "750gr"],
            "MAXIS": ["400 gr", "900 gr"],
        },
    }
    for subcategory_name, brands in references.items():
        for brand_name, sku_names in brands.items():
            marque = Marque.objects.filter(nom=brand_name).order_by("created_at").first()
            if not marque:
                marque = Marque.objects.create(
                    nom=brand_name, concurrent=brand_name != "MIO"
                )
            if not SMarque.objects.filter(
                marque=marque, sous_categorie=subcategories[subcategory_name]
            ).exists():
                SMarque.objects.create(
                    marque=marque, sous_categorie=subcategories[subcategory_name]
                )
            for sku_name in sku_names:
                if not SKU.objects.filter(nom=sku_name, marque=marque).exists():
                    SKU.objects.create(nom=sku_name, marque=marque)


class Migration(migrations.Migration):
    dependencies = [("app", "0002_releve_enrichissements")]

    operations = [migrations.RunPython(add_detergent_subcategories, migrations.RunPython.noop)]
