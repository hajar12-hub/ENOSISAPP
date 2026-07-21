# Veille Marche Service

Microservice Django/DRF pour le module "Veille Marché" — Partie 1/3 : Collecte terrain.

## Structure

```
app/
  exceptions/       Exceptions métier custom (DRF APIException)
  management/
    commands/       seed_referentiel.py : peuple des données de test
  migrations/
  models/           Un fichier par entité (14 modèles)
  repositories/      Couche d'accès aux données (referentiel.py, collecte.py)
  serializers/       DRF serializers (referentiel.py, collecte.py)
  services/          Logique métier (referentiel_service.py, collecte_service.py)
  views/             ViewSets DRF (referentiel.py, collecte.py)
  permissions.py
  urls.py
veille_marche_service/   Projet Django (settings, urls, wsgi, asgi)
```

## Démarrage local

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_referentiel
python manage.py runserver 0.0.0.0:8000
```

## Endpoints principaux

- `GET /health`
- `/veille-marche/secteurs/`, `/canaux/`, `/villes/`, `/adresses/`
- `/veille-marche/magasins/`, `/visites/?magasin={id}`
- `/veille-marche/categories/` (lecture seule)
- `/veille-marche/sous-categories/?categorie={id}`
- `/veille-marche/segments/?sous_categorie={id}`
- `/veille-marche/s-marques/?sous_categorie={id}`
- `/veille-marche/concurents/?sous_categorie={id}`
- `/veille-marche/marques/?segment={id}&s_marque={id}&concurent={id}`
- `/veille-marche/skus/?marque={id}`
- `/veille-marche/releves/?visite={id}`
  - POST simple : un relevé
  - POST en lot : `{"releves": [{"sku": "...", "prix_conso_ttc": 5.0, "prix_detail_ttc": 8.0}, ...]}`
    (marque la visite comme "soumise")

## Notes de conception

- Aucun calcul d'index/marge/markup ici : `Releve` stocke uniquement les
  valeurs brutes (prix conso/détail/gros TTC, remises). Les indicateurs
  calculés sont du ressort du module Visualisation (Mois 1, partie 2/3).
- `SousCategorie.type` (`direct` / `segment` / `groupsInline`) détermine
  quel chemin relie la sous-catégorie à `Marque` : directement via
  `SMarque`, via `Segment`, ou via `Concurent` (groupe comparatif).
  `ReferentielService` valide cette cohérence à la création.

  
