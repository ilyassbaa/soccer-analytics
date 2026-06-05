import pandas as pd
from sklearn.linear_model import LogisticRegression
from src.models import PhaseDeJeu, Joueur

class VAEPEngine:
    """Moteur d'Intelligence Artificielle pour calculer le score VAEP."""
    
    def __init__(self, evenements, k_actions=15):
        self.evenements = evenements
        self.k_actions = k_actions
        self.phases_valides = []
        self.joueurs_stats = {} # Dictionnaire pour stocker nos objets Joueur

    def extract_phases(self):
        """Regroupe les événements en possessions et garde celles de 2 à 5 passes."""
        print("--> Extraction des phases de jeu (règle des 2 à 5 passes)...")
        
        # CORRECTION : Grouper les événements par ID de possession ET par équipe
        possessions = {}
        for event in self.evenements:
            cle = (event.possession_id, event.equipe) # <-- La clé contient maintenant l'équipe
            if cle not in possessions:
                possessions[cle] = []
            possessions[cle].append(event)
            
        # Créer les objets PhaseDeJeu
        for (poss_id, equipe), events in possessions.items():
            if not events: continue
                
            phase = PhaseDeJeu(id_possession=poss_id, equipe=equipe)
            
            for e in events:
                phase.ajouter_evenement(e, e.index_global)
                
            if phase.est_valide():
                self.phases_valides.append(phase)
                
        print(f"    {len(self.phases_valides)} phases valides trouvées.")
        return self.phases_valides

    def train_and_calculate_vaep(self):
        """Entraîne les modèles P_marquer et P_encaisser et calcule le VAEP."""
        print(f"--> Entraînement du modèle VAEP (k={self.k_actions} actions futures)...")
        
        X_data = []
        y_scores = []
        y_concedes = []
        
        # Préparation des données d'entraînement (Data Labeling)
        for phase in self.phases_valides:
            idx = phase.index_fin
            # Regarder k actions dans le futur
            future_events = [e for e in self.evenements if idx <= e.index_global <= idx + self.k_actions]
            
            # Y a-t-il eu un tir par l'équipe ou contre l'équipe ?
            scored = 1 if any(e.equipe == phase.equipe and e.type_action == 'Shot' for e in future_events) else 0
            conceded = 1 if any(e.equipe != phase.equipe and e.type_action == 'Shot' for e in future_events) else 0
            
            y_scores.append(scored)
            y_concedes.append(conceded)
            
            total_dxg, total_dxt = phase.obtenir_totaux()
            
            # Features pour le Machine Learning
            features = [
                len([e for e in phase.evenements if e.type_action == 'Pass']), # Nombre de passes
                phase.evenements[0].start_x, phase.evenements[0].start_y,      # Coordonnées début
                phase.evenements[-1].end_x, phase.evenements[-1].end_y,        # Coordonnées fin
                total_dxg, total_dxt                                           # Totaux danger
            ]
            X_data.append(features)

        # Si pas de données, on arrête
        if not X_data: return

        # Création du DataFrame pour sklearn
        X = pd.DataFrame(X_data).fillna(0)
        
        # Modèles
        model_scores = LogisticRegression(max_iter=1000, class_weight='balanced')
        model_concedes = LogisticRegression(max_iter=1000, class_weight='balanced')
        
        # Prédictions
        p_marquer = model_scores.fit(X, y_scores).predict_proba(X)[:, 1] if sum(y_scores) > 0 else [0.0]*len(X)
        p_encaisser = model_concedes.fit(X, y_concedes).predict_proba(X)[:, 1] if sum(y_concedes) > 0 else [0.0]*len(X)

        # Calcul du score final pour chaque phase et attribution aux joueurs
        print("--> Évaluation des joueurs...")
        for i, phase in enumerate(self.phases_valides):
            vaep = p_marquer[i] - p_encaisser[i]
            total_dxg, total_dxt = phase.obtenir_totaux()
            joueurs_impliques = phase.obtenir_joueurs_impliques()
            
            for nom_joueur in joueurs_impliques:
                if pd.isna(nom_joueur): continue
                    
                cle = (nom_joueur, phase.equipe)
                if cle not in self.joueurs_stats:
                    self.joueurs_stats[cle] = Joueur(nom_joueur, phase.equipe)
                    
                self.joueurs_stats[cle].ajouter_statistiques(total_dxg, total_dxt, vaep)

    def get_player_rankings(self):
        """Retourne le classement des joueurs sous forme de DataFrame Pandas."""
        records = []
        for joueur in self.joueurs_stats.values():
            records.append({
                'Joueur': joueur.nom,
                'Equipe': joueur.equipe,
                'Actions_Jouees': joueur.actions_jouees,
                'Total_DXG': joueur.total_dxg,
                'Total_DXT': joueur.total_dxt,
                'Score_VAEP': joueur.score_vaep
            })
            
        df = pd.DataFrame(records)
        return df.sort_values(by='Score_VAEP', ascending=False) if not df.empty else df