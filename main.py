import os
import pandas as pd
from src.converter import SpadlConverter
from src.vaep_engine import VAEPEngine
from config import DATA_PATH

def process_batch(data_folder):
    tous_les_joueurs = []

    # 1. Scanner tous les fichiers du dossier
    fichiers = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    
    for fichier in fichiers:
        print(f"\n--- Traitement du match : {fichier} ---")
        path = os.path.join(data_folder, fichier)
        
        # 2. Pipeline complet pour chaque fichier
        converter = SpadlConverter(path)
        evenements = converter.generate_events()
        
        engine = VAEPEngine(evenements, k_actions=15)
        engine.extract_phases()
        engine.train_and_calculate_vaep()
        
        # 3. Récupérer les stats et les ajouter à la liste globale
        stats = engine.get_player_rankings()
        tous_les_joueurs.append(stats)

    # 4. Agréger tout (Batch result)
    print("\n--- Agrégation finale de toute la saison ---")
    saison_complete = pd.concat(tous_les_joueurs)
    classement_final = saison_complete.groupby(['Joueur', 'Equipe']).sum().reset_index()
    
    return classement_final.sort_values(by='Score_VAEP', ascending=False)

if __name__ == "__main__":
    # Assurez-vous que tous vos CSV sont dans le dossier 'data/'
    resultats = process_batch(DATA_PATH)
    print(resultats.head(10).to_string(index=False))