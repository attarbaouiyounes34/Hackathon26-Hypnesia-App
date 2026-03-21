import csv
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# =============================================================================
# BASE DE DONNÉES SIMPLIFIÉE 
# Sources : ADEME / INIES + données équipe
# =============================================================================
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
        "empreinte_carbone_kgCO2": 80,
        "consommation_eau_L": 185,
        "duree_vie_annees": 52,
        "distance_parcourue_km": 200,
        "dechet_recyclable_pct": 60,
        "sanitaire_cov": "B"
    },
    "Brique": {
        "empreinte_carbone_kgCO2": 45,
        "consommation_eau_L": 110,
        "duree_vie_annees": 80,
        "distance_parcourue_km": 250,
        "dechet_recyclable_pct": 80,
        "sanitaire_cov": "A"
    },
    "Pierre": {
        "empreinte_carbone_kgCO2": 15,
        "consommation_eau_L": 30,
        "duree_vie_annees": 200,
        "distance_parcourue_km": 100,
        "dechet_recyclable_pct": 100,
        "sanitaire_cov": "A+"
    },
    "Acier": {
        "empreinte_carbone_kgCO2": 110,
        "consommation_eau_L": 600,
        "duree_vie_annees": 50,
        "distance_parcourue_km": 600,
        "dechet_recyclable_pct": 99,
        "sanitaire_cov": "B"
    },
    "Plâtre": {
        "empreinte_carbone_kgCO2": 10,
        "consommation_eau_L": 25,
        "duree_vie_annees": 30,
        "distance_parcourue_km": 200,
        "dechet_recyclable_pct": 100,
        "sanitaire_cov": "A"
    },
    "Aluminium": {
        "empreinte_carbone_kgCO2": 90,
        "consommation_eau_L": 475,
        "duree_vie_annees": 40,
        "distance_parcourue_km": 800,
        "dechet_recyclable_pct": 95,
        "sanitaire_cov": "A"
    },
    "PVC": {
        "empreinte_carbone_kgCO2": 52,
        "consommation_eau_L": 290,
        "duree_vie_annees": 27,
        "distance_parcourue_km": 500,
        "dechet_recyclable_pct": 30,
        "sanitaire_cov": "B"
    },
    "Carrelage": {
        "empreinte_carbone_kgCO2": 25,
        "consommation_eau_L": 180,
        "duree_vie_annees": 40,
        "distance_parcourue_km": 600,
        "dechet_recyclable_pct": 30,
        "sanitaire_cov": "A"
    },
    "Parquet": {
        "empreinte_carbone_kgCO2": -5,
        "consommation_eau_L": 38,
        "duree_vie_annees": 43,
        "distance_parcourue_km": 300,
        "dechet_recyclable_pct": 90,
        "sanitaire_cov": "A+"
    },
    "Plastique": {
        "empreinte_carbone_kgCO2": 90,
        "consommation_eau_L": 170,
        "duree_vie_annees": 30,
        "distance_parcourue_km": 1200,
        "dechet_recyclable_pct": 25,
        "sanitaire_cov": "B"
    }
}

# =============================================================================
# BASE DE DONNÉES DÉTAILLÉE (toutes les lignes du fichier Excel de l'équipe)
# Colonnes : element, materiau, type, sanitaire_cov, duree_vie_annees,
#            consommation_eau_L, empreinte_carbone_kgCO2, distance_parcourue_km
# =============================================================================
FULL_DATA = [
    # --- Fenetre ---
    {"element": "Fenetre", "materiau": "Aluminium", "type": "Noir",         "sanitaire_cov": "A",  "duree_vie_annees": 40,     "consommation_eau_L": 450, "empreinte_carbone_kgCO2": 85,  "distance_parcourue_km": 800},
    {"element": "Fenetre", "materiau": "Bois",      "type": "Chene",        "sanitaire_cov": "A+", "duree_vie_annees": 35,     "consommation_eau_L": 110, "empreinte_carbone_kgCO2": -28, "distance_parcourue_km": 300},
    {"element": "Fenetre", "materiau": "Bois",      "type": "Accajou",      "sanitaire_cov": "A+", "duree_vie_annees": 45,     "consommation_eau_L": 150, "empreinte_carbone_kgCO2": 12,  "distance_parcourue_km": 8000},
    {"element": "Fenetre", "materiau": "Bois",      "type": "Pin",          "sanitaire_cov": "A+", "duree_vie_annees": 25,     "consommation_eau_L": 90,  "empreinte_carbone_kgCO2": -32, "distance_parcourue_km": 250},
    {"element": "Fenetre", "materiau": "PVC",       "type": "PVC",          "sanitaire_cov": "B",  "duree_vie_annees": 30,     "consommation_eau_L": 300, "empreinte_carbone_kgCO2": 55,  "distance_parcourue_km": 500},

    # --- Mur ---
    {"element": "Mur",     "materiau": "Beton",     "type": "Blanc",        "sanitaire_cov": "B",  "duree_vie_annees": 70,     "consommation_eau_L": 280, "empreinte_carbone_kgCO2": 140, "distance_parcourue_km": 300},
    {"element": "Mur",     "materiau": "Beton",     "type": "Gris",         "sanitaire_cov": "B",  "duree_vie_annees": 70,     "consommation_eau_L": 250, "empreinte_carbone_kgCO2": 120, "distance_parcourue_km": 150},
    {"element": "Mur",     "materiau": "Bois",      "type": "Chene",        "sanitaire_cov": "A+", "duree_vie_annees": 50,     "consommation_eau_L": 40,  "empreinte_carbone_kgCO2": -40, "distance_parcourue_km": 200},
    {"element": "Mur",     "materiau": "Bois",      "type": "Hetre",        "sanitaire_cov": "A+", "duree_vie_annees": 45,     "consommation_eau_L": 42,  "empreinte_carbone_kgCO2": -38, "distance_parcourue_km": 200},
    {"element": "Mur",     "materiau": "Bois",      "type": "Erable",       "sanitaire_cov": "A+", "duree_vie_annees": 45,     "consommation_eau_L": 45,  "empreinte_carbone_kgCO2": -35, "distance_parcourue_km": 400},
    {"element": "Mur",     "materiau": "Bois",      "type": "Accajou",      "sanitaire_cov": "A+", "duree_vie_annees": 60,     "consommation_eau_L": 60,  "empreinte_carbone_kgCO2": 10,  "distance_parcourue_km": 8500},
    {"element": "Mur",     "materiau": "Bois",      "type": "Pin",          "sanitaire_cov": "A+", "duree_vie_annees": 35,     "consommation_eau_L": 35,  "empreinte_carbone_kgCO2": -45, "distance_parcourue_km": 150},
    {"element": "Mur",     "materiau": "Brique",    "type": "Orange/Rouge", "sanitaire_cov": "A",  "duree_vie_annees": 80,     "consommation_eau_L": 110, "empreinte_carbone_kgCO2": 45,  "distance_parcourue_km": 250},
    {"element": "Mur",     "materiau": "Pierre",    "type": "Gris",         "sanitaire_cov": "A+", "duree_vie_annees": "100+", "consommation_eau_L": 30,  "empreinte_carbone_kgCO2": 15,  "distance_parcourue_km": 100},
    {"element": "Mur",     "materiau": "Platre",    "type": "Blanc/Beige",  "sanitaire_cov": "A",  "duree_vie_annees": 30,     "consommation_eau_L": 25,  "empreinte_carbone_kgCO2": 10,  "distance_parcourue_km": 200},

    # --- Porte ---
    {"element": "Porte",   "materiau": "Bois",      "type": "Chene",        "sanitaire_cov": "A+", "duree_vie_annees": 40,     "consommation_eau_L": 80,  "empreinte_carbone_kgCO2": -15, "distance_parcourue_km": 250},
    {"element": "Porte",   "materiau": "Bois",      "type": "Hetre",        "sanitaire_cov": "A+", "duree_vie_annees": 35,     "consommation_eau_L": 85,  "empreinte_carbone_kgCO2": -12, "distance_parcourue_km": 250},
    {"element": "Porte",   "materiau": "Bois",      "type": "Erable",       "sanitaire_cov": "A+", "duree_vie_annees": 35,     "consommation_eau_L": 85,  "empreinte_carbone_kgCO2": -10, "distance_parcourue_km": 450},
    {"element": "Porte",   "materiau": "Bois",      "type": "Accajou",      "sanitaire_cov": "A+", "duree_vie_annees": 45,     "consommation_eau_L": 95,  "empreinte_carbone_kgCO2": 20,  "distance_parcourue_km": 8000},
    {"element": "Porte",   "materiau": "Bois",      "type": "Pin",          "sanitaire_cov": "A+", "duree_vie_annees": 30,     "consommation_eau_L": 70,  "empreinte_carbone_kgCO2": -20, "distance_parcourue_km": 200},
    {"element": "Porte",   "materiau": "PVC",       "type": "PVC",          "sanitaire_cov": "B",  "duree_vie_annees": 25,     "consommation_eau_L": 280, "empreinte_carbone_kgCO2": 50,  "distance_parcourue_km": 500},
    {"element": "Porte",   "materiau": "Aluminium", "type": "Noir",         "sanitaire_cov": "A",  "duree_vie_annees": 40,     "consommation_eau_L": 500, "empreinte_carbone_kgCO2": 95,  "distance_parcourue_km": 800},
    {"element": "Porte",   "materiau": "Acier",     "type": "Argent",       "sanitaire_cov": "B",  "duree_vie_annees": 50,     "consommation_eau_L": 600, "empreinte_carbone_kgCO2": 110, "distance_parcourue_km": 600},

    # --- Sol ---
    {"element": "Sol",     "materiau": "Beton",     "type": "Gris",         "sanitaire_cov": "B",  "duree_vie_annees": 30,     "consommation_eau_L": 120, "empreinte_carbone_kgCO2": 40,  "distance_parcourue_km": 150},
    {"element": "Sol",     "materiau": "Carrelage", "type": "Blanc",        "sanitaire_cov": "A",  "duree_vie_annees": 40,     "consommation_eau_L": 180, "empreinte_carbone_kgCO2": 25,  "distance_parcourue_km": 600},
    {"element": "Sol",     "materiau": "Parquet",   "type": "Chene",        "sanitaire_cov": "A+", "duree_vie_annees": 50,     "consommation_eau_L": 35,  "empreinte_carbone_kgCO2": -12, "distance_parcourue_km": 300},
    {"element": "Sol",     "materiau": "Parquet",   "type": "Hetre",        "sanitaire_cov": "A+", "duree_vie_annees": 40,     "consommation_eau_L": 38,  "empreinte_carbone_kgCO2": -10, "distance_parcourue_km": 300},
    {"element": "Sol",     "materiau": "Parquet",   "type": "Erable",       "sanitaire_cov": "A+", "duree_vie_annees": 45,     "consommation_eau_L": 40,  "empreinte_carbone_kgCO2": -8,  "distance_parcourue_km": 500},
    {"element": "Sol",     "materiau": "Parquet",   "type": "Accajou",      "sanitaire_cov": "A+", "duree_vie_annees": 50,     "consommation_eau_L": 50,  "empreinte_carbone_kgCO2": 25,  "distance_parcourue_km": 8500},
    {"element": "Sol",     "materiau": "Parquet",   "type": "Pin",          "sanitaire_cov": "A+", "duree_vie_annees": 30,     "consommation_eau_L": 25,  "empreinte_carbone_kgCO2": -18, "distance_parcourue_km": 200},

    # --- Toit ---
    {"element": "Toit",    "materiau": "Beton",     "type": "Gris",         "sanitaire_cov": "B",  "duree_vie_annees": 40,     "consommation_eau_L": 90,  "empreinte_carbone_kgCO2": 20,  "distance_parcourue_km": 200},
    {"element": "Toit",    "materiau": "Bois",      "type": "Marron",       "sanitaire_cov": "A+", "duree_vie_annees": 50,     "consommation_eau_L": 45,  "empreinte_carbone_kgCO2": -35, "distance_parcourue_km": 250},
]

# =============================================================================
# FICHIER CSV (pour /api/tout)
# =============================================================================
CSV_FILE = "Excel_V1.csv"

def lire_excel_v1():
    if not os.path.exists(CSV_FILE):
        return None
    try:
        donnees_vr = []
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                materiau = row.get('Materiaux', '')
                nom_normalise = materiau.strip().capitalize() if materiau else ""
                stats_ecolo = ECO_DATA.get(nom_normalise, {
                    "empreinte_carbone_kgCO2": 0, "consommation_eau_L": 0,
                    "duree_vie_annees": 0, "distance_parcourue_km": 0,
                    "dechet_recyclable_pct": 0, "sanitaire_cov": "Inconnu"
                })
                donnees_vr.append({
                    "element":  row.get('Elements'),
                    "materiau": materiau,
                    "couleur":  row.get('Couleurs'),
                    "ecologie": stats_ecolo
                })
        return donnees_vr
    except Exception as e:
        return None


# =============================================================================
# ROUTES DE L'API
# =============================================================================

@app.route('/api/materiaux', methods=['GET'])
def get_liste_materiaux():
    """Liste tous les materiaux disponibles dans ECO_DATA"""
    return jsonify({"materiaux": list(ECO_DATA.keys())})


@app.route('/api/materiau/<nom_materiau>', methods=['GET'])
def get_materiau_stats(nom_materiau):
    """Stats ecologiques d'un materiau (insensible a la casse)
    Ex : /api/materiau/Bois  ou  /api/materiau/bois
    """
    nom_normalise = nom_materiau.strip().capitalize()
    stats = ECO_DATA.get(nom_normalise)
    if stats:
        return jsonify({"materiau": nom_normalise, "statistiques": stats})
    return jsonify({
        "erreur": f"Materiau '{nom_materiau}' non trouve",
        "materiaux_disponibles": list(ECO_DATA.keys())
    }), 404


@app.route('/api/elements', methods=['GET'])
def get_elements():
    """Liste tous les elements de construction disponibles
    Ex : Fenetre, Mur, Porte, Sol, Toit
    """
    elements = sorted(set(row["element"] for row in FULL_DATA))
    return jsonify({"elements": elements})


@app.route('/api/element/<nom_element>', methods=['GET'])
def get_element(nom_element):
    """Toutes les options de materiaux pour un element donne
    Ex : /api/element/Mur  ->  tous les materiaux possibles pour un mur
    """
    resultats = [
        row for row in FULL_DATA
        if row["element"].lower() == nom_element.strip().lower()
    ]
    if not resultats:
        elements_dispos = sorted(set(r["element"] for r in FULL_DATA))
        return jsonify({
            "erreur": f"Element '{nom_element}' non trouve",
            "elements_disponibles": elements_dispos
        }), 404
    return jsonify({
        "element":    resultats[0]["element"],
        "nb_options": len(resultats),
        "options":    resultats
    })


@app.route('/api/element/<nom_element>/materiau/<nom_materiau>', methods=['GET'])
def get_element_materiau(nom_element, nom_materiau):
    """Tous les types d'un materiau pour un element donne
    Ex : /api/element/Mur/materiau/Bois  ->  Chene, Hetre, Erable, etc.
    """
    resultats = [
        row for row in FULL_DATA
        if row["element"].lower()  == nom_element.strip().lower()
        and row["materiau"].lower() == nom_materiau.strip().lower()
    ]
    if not resultats:
        return jsonify({
            "erreur": f"Aucun resultat pour {nom_element}/{nom_materiau}"
        }), 404
    return jsonify({
        "element":  resultats[0]["element"],
        "materiau": resultats[0]["materiau"],
        "nb_types": len(resultats),
        "types":    resultats
    })


@app.route('/api/comparer', methods=['GET'])
def comparer_materiaux():
    """Compare deux materiaux cote a cote
    Params : ?mat1=Bois&mat2=Beton
    Ex : /api/comparer?mat1=Bois&mat2=Beton
    """
    mat1 = request.args.get('mat1', '').strip().capitalize()
    mat2 = request.args.get('mat2', '').strip().capitalize()
    if not mat1 or not mat2:
        return jsonify({"erreur": "Parametres manquants : ?mat1=...&mat2=..."}), 400
    stats1 = ECO_DATA.get(mat1)
    stats2 = ECO_DATA.get(mat2)
    if not stats1:
        return jsonify({"erreur": f"Materiau '{mat1}' non trouve"}), 404
    if not stats2:
        return jsonify({"erreur": f"Materiau '{mat2}' non trouve"}), 404
    return jsonify({mat1: stats1, mat2: stats2})


@app.route('/api/tout', methods=['GET'])
def get_all_data():
    """Toutes les donnees detaillees.
    Utilise Excel_V1.csv si present, sinon renvoie FULL_DATA en memoire.
    """
    csv_data = lire_excel_v1()
    if csv_data:
        return jsonify(csv_data)
    return jsonify(FULL_DATA)


# =============================================================================
# LANCEMENT DU SERVEUR
# =============================================================================
if __name__ == '__main__':
    print("=" * 55)
    print("  API Transition Ecologique - Hackathon IUT Beziers 2026")
    print("=" * 55)
    print(f"  Materiaux : {list(ECO_DATA.keys())}")
    print(f"  Lignes details : {len(FULL_DATA)}")
    print(f"  Elements : Fenetre, Mur, Porte, Sol, Toit")
    print("=" * 55)
    print("  Routes :")
    print("    GET /api/materiaux")
    print("    GET /api/materiau/<nom>")
    print("    GET /api/elements")
    print("    GET /api/element/<nom>")
    print("    GET /api/element/<nom>/materiau/<mat>")
    print("    GET /api/comparer?mat1=Bois&mat2=Beton")
    print("    GET /api/tout")
    print("=" * 55)
    app.run(host='0.0.0.0', port=5000, debug=True)
