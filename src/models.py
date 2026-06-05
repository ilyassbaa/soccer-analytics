import pandas as pd

class Joueur:
    """Représente un intervenant dans le match selon le cahier des charges."""
    def __init__(self, nom, equipe):
        self.nom = nom
        self.equipe = equipe
        self.actions_jouees = 0
        self.total_dxg = 0.0
        self.total_dxt = 0.0
        self.score_vaep = 0.0

    def ajouter_statistiques(self, dxg, dxt, vaep):
        """Méthode pour accumuler les performances du joueur."""
        self.actions_jouees += 1
        self.total_dxg += dxg
        self.total_dxt += dxt
        self.score_vaep += vaep

    def __str__(self):
        return f"{self.nom} ({self.equipe}) - VAEP: {self.score_vaep:.4f}"

class Evenement:
    """Représente une action individuelle sur la balle."""
    def __init__(self, type_action, joueur, equipe, start_x, start_y, end_x, end_y):
        self.type_action = type_action
        self.joueur = joueur
        self.equipe = equipe
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.dxg = 0.0 # Sera calculé plus tard par le MathEngine
        self.dxt = 0.0 # Sera calculé plus tard par le MathEngine

class PhaseDeJeu:
    """Représente une possession. Valide la règle stricte des 2 à 5 passes."""
    def __init__(self, id_possession, equipe):
        self.id_possession = id_possession
        self.equipe = equipe
        self.evenements = []
        self.index_fin = None

    def ajouter_evenement(self, evenement, index_global):
        self.evenements.append(evenement)
        self.index_fin = index_global

    def est_valide(self):
        """Vérifie si la phase respecte le cahier des charges (2 à 5 passes)."""
        nombre_passes = sum(1 for e in self.evenements if e.type_action == 'Pass')
        return 2 <= nombre_passes <= 5

    def obtenir_totaux(self):
        """Calcule le danger total généré lors de cette phase."""
        passes = [e for e in self.evenements if e.type_action == 'Pass']
        total_dxg = sum(p.dxg for p in passes)
        total_dxt = sum(p.dxt for p in passes)
        return total_dxg, total_dxt

    def obtenir_joueurs_impliques(self):
        """Retourne la liste des noms des joueurs ayant fait une passe dans cette phase."""
        passes = [e for e in self.evenements if e.type_action == 'Pass']
        # Utilisation d'un set pour éviter les doublons si un joueur fait 2 passes
        return list(set(p.joueur for p in passes if pd.notna(p.joueur)))