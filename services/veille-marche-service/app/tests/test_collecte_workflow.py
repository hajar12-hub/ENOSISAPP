from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APITestCase

from app.models import Categorie, Concurent, Magasin, Marque, Releve, SKU, Secteur, SousCategorie, Ville, Visite


class CollecteWorkflowTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="terrain", password="secret")
        self.client.force_authenticate(self.user)
        secteur = Secteur.objects.create(nom="Centre")
        ville = Ville.objects.create(nom="Casablanca")
        self.magasin = Magasin.objects.create(secteur=secteur, ville=ville)
        detergent, _ = Categorie.objects.get_or_create(nom="Detergent")
        self.sous_categorie, _ = SousCategorie.objects.get_or_create(
            nom="Low Suds Liquide", categorie=detergent, defaults={"type": SousCategorie.Type.GROUPS_INLINE}
        )
        marque = Marque.objects.create(nom="MIO")
        Concurent.objects.create(nom="vs MIO", marque=marque, sous_categorie=self.sous_categorie)
        self.sku = SKU.objects.create(nom="1L", marque=marque)

    def create_visit(self):
        response = self.client.post("/veille-marche/visites/", {"magasin": str(self.magasin.id)}, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        return response.data["id"]

    def test_draft_submission_and_status_lists(self):
        draft_id = self.create_visit()
        response = self.client.post(f"/veille-marche/releves/?visite={draft_id}&draft=1", {"releves": []}, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        second_draft_id = self.create_visit()
        self.client.post(f"/veille-marche/releves/?visite={second_draft_id}&draft=1", {"releves": []}, format="json")
        drafts = self.client.get("/veille-marche/visites/?statut=brouillon")
        self.assertEqual(drafts.status_code, 200)
        self.assertEqual({item["id"] for item in drafts.data}, {draft_id, second_draft_id})

        submitted_id = self.create_visit()
        response = self.client.post(f"/veille-marche/releves/?visite={submitted_id}", {
            "releves": [{"sku": str(self.sku.id), "prix_conso_ttc": 12, "prix_detail_ttc": 10}],
        }, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data[0]["sous_categorie_nom"], "Low Suds Liquide")
        releves = self.client.get(f"/veille-marche/releves/?visite={submitted_id}")
        self.assertEqual(releves.status_code, 200)
        self.assertEqual(releves.data[0]["sous_categorie_nom"], "Low Suds Liquide")
        self.assertTrue(Releve.objects.filter(visite_id=submitted_id).exists())
        self.assertEqual(Visite.objects.get(id=submitted_id).statut, Visite.Statut.SOUMISE)

        historique = self.client.get("/veille-marche/visites/?statut=soumise")
        self.assertEqual(historique.status_code, 200)
        self.assertEqual(historique.data[0]["id"], submitted_id)

    def test_reference_import_includes_detergent_and_paper_formats(self):
        call_command("import_referentiel")
        detergent = Categorie.objects.get(nom="Detergent")
        names = set(SousCategorie.objects.filter(categorie=detergent).values_list("nom", flat=True))
        self.assertTrue({"High Suds", "Low Suds Liquide", "Liquide Vaisselle", "Poudre Matic"}.issubset(names))
        self.assertTrue(SKU.objects.filter(marque__s_marques__sous_categorie__nom="Liquide Vaisselle").exists())
        self.assertTrue(SKU.objects.filter(marque__s_marques__sous_categorie__nom="Poudre Matic").exists())
        toilet_paper = SousCategorie.objects.get(categorie__nom="Papier", nom="Toilet Paper")
        self.assertEqual(set(toilet_paper.segments.values_list("nom", flat=True)), {"2 PLIS", "3 PLIS"})
