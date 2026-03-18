# 🌱 API Transition Écologique — Hackathon IUT Béziers 2026

API REST développée par l'équipe R&T dans le cadre du **7ème Hackathon de l'IUT de Béziers**,  
en réponse au sujet proposé par **Hypnésia** : utiliser la réalité virtuelle comme outil de transition écologique.

---

## 📋 Description

Cette API fournit des données écologiques sur les matériaux de construction (empreinte carbone, consommation d'eau, durée de vie...).  
Elle sert de **backend commun** pour l'ensemble de l'équipe :
- Les **MMI** peuvent l'appeler depuis leur dashboard web
- Les **ROB-IA** peuvent l'interroger depuis le casque VR
- Les données sont au format **JSON**, prêtes à l'emploi

---

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/VOTRE_NOM/VOTRE_REPO.git
cd VOTRE_REPO
```

### 2. Installer les dépendances
```bash
pip install flask flask-cors
```

### 3. Lancer le serveur
```bash
python api_vr.py
```

Le serveur démarre sur le port **5000** et est accessible sur tout le réseau local.

---

## 🌐 Routes disponibles

### `GET /api/materiaux`
Liste tous les matériaux disponibles dans la base.

**Exemple de réponse :**
```json
{
  "materiaux": ["Bois", "Béton", "Brique", "Pierre", "Acier", "Plâtre"]
}
```

---

### `GET /api/materiau/<nom>`
Retourne les statistiques écologiques d'un matériau précis.  
Le nom est insensible à la casse (`bois`, `BOIS` et `Bois` fonctionnent).

**Exemple :** `GET /api/materiau/Bois`

```json
{
  "materiau": "Bois",
  "statistiques": {
    "empreinte_carbone_kgCO2": -15,
    "consommation_eau_L": 20,
    "duree_vie_annees": 50,
    "distance_parcourue_km": 150,
    "dechet_recyclable_pct": 95,
    "sanitaire_cov": "A+"
  }
}
```

> ℹ️ Une empreinte carbone **négative** signifie que le matériau **stocke** du carbone (cas du Bois).

---

### `GET /api/tout`
Retourne la fusion complète du fichier CSV avec les stats écologiques.  
Utile pour charger toutes les données en une seule requête au démarrage de l'application VR.

**Exemple de réponse :**
```json
[
  {
    "element": "Mur",
    "materiau": "Bois",
    "couleur": "Marron",
    "ecologie": {
      "empreinte_carbone_kgCO2": -15,
      "consommation_eau_L": 20,
      ...
    }
  }
]
```

---

## 📁 Fichier CSV requis

L'API attend un fichier `Excel_V1.csv` dans le même dossier, avec ce format :

```
Éléments,Matériaux,Couleurs
Mur,Bois,Marron
Sol,Béton,Gris
Toit,Acier,Argent
```

> Si le fichier est absent, `/api/tout` renvoie une erreur 500 explicite.

---

## 📡 Accès depuis le réseau local

Une fois le serveur lancé, les autres membres de l'équipe peuvent y accéder via l'IP du serveur.  
L'IP s'affiche au démarrage dans le terminal, par exemple :

```
* Running on http://172.24.127.30:5000
```

Ils peuvent alors appeler : `http://172.24.127.30:5000/api/materiaux`

> Le CORS est activé : les appels depuis une page web ou un casque VR sont autorisés.

---

## 📊 Données écologiques (Sources : ADEME / INIES)

| Matériau | CO₂ (kg) | Eau (L) | Durée de vie | Recyclable | COV |
|----------|----------|---------|--------------|------------|-----|
| Bois     | -15      | 20      | 50 ans       | 95%        | A+  |
| Béton    | +45      | 150     | 100 ans      | 60%        | A   |
| Brique   | +35      | 80      | 100 ans      | 80%        | A+  |
| Pierre   | +10      | 30      | 200 ans      | 100%       | A+  |
| Acier    | +80      | 200     | 80 ans       | 99%        | A+  |
| Plâtre   | +25      | 60      | 50 ans       | 100%       | A+  |

---

## 👥 Équipe

Hackathon IUT Béziers 2026 — Sujet Hypnésia  
Département **R&T** (Réseaux & Télécommunications)

---

## 📬 Contact commanditaire

**Hypnésia** — M. Thibault Stoyanov  
📧 thibault.stoyanov@hypnesia.com  
📞 06 26 44 58 05
