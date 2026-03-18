import csv
import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Correction Bug 3 : autorise les requêtes du casque VR et des pages web

# --- 1. NOTRE BASE DE DONNÉES ÉCOLOGIQUES (Sources : ADEME / INIES) ---
ECO_DATA = {
    "Bois": {
        "empreinte_carbone_kgCO2": -15,
        "consommation_eau_L": 20,
        "duree_vie_annees": 50,
        "distance_parcourue_km": 150,
        "dechet_recyclable_pct": 95,
        "sanitaire_cov": "A+"
    },
    "Béton": {
        "empreinte_carbone_kgCO2": 45,
        "consommation_eau_L": 150,
        "duree_vie_annees": 100,
        "distance_parcourue_km": 50,
        "dechet_recyclable_pct": 60,
        "sanitaire_cov": "A"
    },
    "Brique": {
        "empreinte_carbone_kgCO2": 35,
        "consommation_eau_L": 80,
        "duree_vie_annees": 100,
        "distance_parcourue_km": 200,
        "dechet_recyclable_pct": 80,
        "sanitaire_cov": "A+"
    },
    "Pierre": {
        "empreinte_carbone_kgCO2": 10,
        "consommation_eau_L": 30,
        "duree_vie_annees": 200,
        "distance_parcourue_km": 500,
        "dechet_recyclable_pct": 100,
        "sanitaire_cov": "A+"
    },
    "Acier": {
        "empreinte_carbone_kgCO2": 80,
        "consommation_eau_L": 200,
        "duree_vie_annees": 80,
        "distance_parcourue_km": 1000,
        "dechet_recyclable_pct": 99,
        "sanitaire_cov": "A+"
    },
    "Plâtre": {
        "empreinte_carbone_kgCO2": 25,
        "consommation_eau_L": 60,
        "duree_vie_annees": 50,
        "distance_parcourue_km": 100,
        "dechet_recyclable_pct": 100,
        "sanitaire_cov": "A+"
    }
}

# --- 2. FICHIER CSV ---
CSV_FILE = "Excel_V1.csv"  # Correction Bug 1 : une seule variable, cohérente partout

def lire_excel_v1():
    donnees_vr = []

    # Correction Bug 1 : on vérifie et on ouvre le MÊME fichier
    if not os.path.exists(CSV_FILE):
        return [{"erreur": f"Fichier {CSV_FILE} introuvable"}]

    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                element  = row.get('Éléments')
                materiau = row.get('Matériaux')
                couleur  = row.get('Couleurs')

                # Correction Bug 2 : recherche insensible à la casse + strip()
                nom_normalise = materiau.strip().capitalize() if materiau else ""
                stats_ecolo = ECO_DATA.get(nom_normalise, {
                    "empreinte_carbone_kgCO2": 0,
                    "consommation_eau_L": 0,
                    "duree_vie_annees": 0,
                    "distance_parcourue_km": 0,
                    "dechet_recyclable_pct": 0,
                    "sanitaire_cov": "Inconnu"
                })

                donnees_vr.append({
                    "element":  element,
                    "materiau": materiau,
                    "couleur":  couleur,
                    "ecologie": stats_ecolo
                })

    except Exception as e:
        return [{"erreur": f"Erreur de lecture du CSV : {str(e)}"}]

    return donnees_vr


# --- 3. LES ROUTES DE L'API ---

@app.route('/api/tout', methods=['GET'])
def get_all_data():
    """Renvoie toute la base de données fusionnée (CSV + stats écologiques)"""
    data = lire_excel_v1()
    # Correction : si erreur dans le CSV, on renvoie un vrai code HTTP 500
    if len(data) == 1 and "erreur" in data[0]:
        return jsonify(data[0]), 500
    return jsonify(data)


@app.route('/api/materiau/<nom_materiau>', methods=['GET'])
def get_materiau_stats(nom_materiau):
    """Renvoie les stats écologiques d'un matériau (insensible à la casse)"""
    # Correction Bug 2 : strip() + capitalize() pour gérer "beton", "BETON", " Béton "
    nom_normalise = nom_materiau.strip().capitalize()
    stats = ECO_DATA.get(nom_normalise)
    if stats:
        return jsonify({"materiau": nom_normalise, "statistiques": stats})
    else:
        return jsonify({"erreur": f"Matériau '{nom_materiau}' non trouvé",
                        "materiaux_disponibles": list(ECO_DATA.keys())}), 404


@app.route('/api/materiaux', methods=['GET'])
def get_liste_materiaux():
    """Liste tous les matériaux disponibles dans la base — utile pour le casque VR"""
    return jsonify({"materiaux": list(ECO_DATA.keys())})


# --- LANCEMENT DU SERVEUR ---
if __name__ == '__main__':
    print("Lancement de l'API de Transition Écologique sur le port 5000...")
    print(f"Matériaux disponibles : {list(ECO_DATA.keys())}")
    # host='0.0.0.0' permet aux autres machines du réseau local (casque VR) de s'y connecter
    app.run(host='0.0.0.0', port=5000, debug=True)
