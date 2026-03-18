import csv
import os
from flask import Flask, jsonify

app = Flask(__name__)

# --- 1. NOTRE BASE DE DONNÉES ÉCOLOGIQUES (Sources : ADEME / INIES) ---
# On y met tous les critères.
ECO_DATA = {
    "Bois": {
        "empreinte_carbone_kgCO2": -15, # Négatif = stocke le carbone
        "consommation_eau_L": 20,
        "duree_vie_annees": 50,
        "distance_parcourue_km": 150,
        "dechet_recyclable_pct": 95,
        "sanitaire_cov": "A+" # Qualité de l'air
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

# --- 2. FONCTION POUR LIRE LE EXCEL (CSV) ---
def lire_excel_v1():
    donnees_vr = []
    # Assure-toi que le fichier Excel_V1.csv est dans le même dossier
    if not os.path.exists("Excel_V1.csv"):
        return [{"erreur": "Fichier Excel_V1.csv introuvable"}]
        
    with open("Excel_V1.csv", mode='r', encoding='utf-8') as f:
        # On utilise le bon délimiteur (souvent point-virgule ou virgule)
        reader = csv.DictReader(f, delimiter=',') 
        for row in reader:
            element = row.get('Éléments')
            materiau = row.get('Matériaux')
            couleur = row.get('Couleurs')
            
            # On récupère les stats écolos de ce matériau (ou des stats vides si inconnu)
            stats_ecolo = ECO_DATA.get(materiau, {
                "empreinte_carbone_kgCO2": 0, "consommation_eau_L": 0, 
                "duree_vie_annees": 0, "distance_parcourue_km": 0, 
                "dechet_recyclable_pct": 0, "sanitaire_cov": "Inconnu"
            })
            
            # On fusionne ce qui vient du CSV avec nos stats écolos
            item = {
                "element": element,
                "materiau": materiau,
                "couleur": couleur,
                "ecologie": stats_ecolo
            }
            donnees_vr.append(item)
    return donnees_vr

# --- 3. LES ROUTES DE L'API (Ce que le casque VR va interroger) ---

@app.route('/api/tout', methods=['GET'])
def get_all_data():
    """Renvoie toute la base de données fusionnée (utile pour les ROB/IA au lancement)"""
    data = lire_excel_v1()
    return jsonify(data)

@app.route('/api/materiau/<nom_materiau>', methods=['GET'])
def get_materiau_stats(nom_materiau):
    """Permet au casque VR de demander les stats d'un seul matériau spécifique"""
    # On cherche dans notre dictionnaire (avec une majuscule au début)
    stats = ECO_DATA.get(nom_materiau.capitalize())
    if stats:
        return jsonify({"materiau": nom_materiau, "statistiques": stats})
    else:
        return jsonify({"erreur": "Matériau non trouvé"}), 404

# --- LANCEMENT DU SERVEUR ---
if __name__ == '__main__':
    print("Lancement de l'API de Transition Écologique sur le port 5000...")
    # host='0.0.0.0' permet aux autres ordis (et au casque VR) du réseau local de s'y connecter
    app.run(host='0.0.0.0', port=5000, debug=True)
