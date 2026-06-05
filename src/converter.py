import pandas as pd
from src.models import Evenement
from src.math_engine import SoccerMathEngine

class SpadlConverter:
    """
    Convertisseur de données brutes vers le format universel orienté objet (SPADL).
    Isole la logique de traitement des fichiers du moteur mathématique.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.evenements = []

    def load_and_clean(self):
        """Charge le CSV et nettoie les données spatiales (Data Cleaning)."""
        print(f"--> Chargement des données depuis {self.file_path}...")
        
        # low_memory=False évite les avertissements (DtypeWarning) sur les très gros fichiers
        self.df = pd.read_csv(self.file_path, low_memory=False)
        
        # Colonnes SPADL de base requises
        cols_requises = ['index', 'possession', 'period', 'timestamp', 'team_name', 'player_name', 
                         'event_type_name', 'location_x', 'location_y', 'end_location_x', 
                         'end_location_y', 'outcome_name']
        
        # Filtrer seulement les colonnes présentes pour éviter les crashs si le format varie
        cols_presentes = [c for c in cols_requises if c in self.df.columns]
        self.df = self.df[cols_presentes].copy()
        
        # Remplir les coordonnées de fin manquantes
        if 'end_location_x' in self.df.columns and 'location_x' in self.df.columns:
            self.df['end_location_x'] = self.df['end_location_x'].fillna(self.df['location_x'])
            self.df['end_location_y'] = self.df['end_location_y'].fillna(self.df['location_y'])
        
        # Supprimer les événements sans coordonnées
        self.df = self.df.dropna(subset=['location_x', 'location_y']).reset_index(drop=True)
        return self.df

    def generate_events(self):
        """Convertit les lignes du DataFrame Pandas en objets POO de la classe Evenement."""
        if self.df is None:
            self.load_and_clean()

        print("--> Conversion des données brutes en objets métiers POO...")
        
        for index, row in self.df.iterrows():
            # Création de l'objet métier défini dans models.py
            event = Evenement(
                type_action=row.get('event_type_name', 'Unknown'),
                joueur=row.get('player_name', None),
                equipe=row.get('team_name', None),
                start_x=row['location_x'],
                start_y=row['location_y'],
                end_x=row['end_location_x'],
                end_y=row['end_location_y']
            )
            
            # Enrichissement mathématique directement via notre MathEngine !
            event.dxg = SoccerMathEngine.calculate_dxg(event.start_x, event.start_y, event.end_x, event.end_y)
            event.dxt = SoccerMathEngine.calculate_dxt(event.start_x, event.start_y, event.end_x, event.end_y)
            
            # Ajout dynamique d'attributs supplémentaires nécessaires pour le triage des possessions
            event.possession_id = row.get('possession', None)
            event.period = row.get('period', None)
            event.timestamp = row.get('timestamp', None)
            event.outcome_name = row.get('outcome_name', None)
            event.index_global = index # Pour regarder 'k' actions dans le futur
            
            self.evenements.append(event)
            
        return self.evenements