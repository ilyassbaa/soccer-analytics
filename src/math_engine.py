import numpy as np

class SoccerMathEngine:
    """Classe utilitaire contenant toutes les méthodes de calcul spatial."""
    
    # Grille statique du Terrain (Expected Threat)
    XT_GRID = np.array([
        [0.006, 0.006, 0.007, 0.008, 0.009, 0.011, 0.013, 0.015, 0.017, 0.023, 0.034, 0.080],
        [0.006, 0.006, 0.007, 0.008, 0.009, 0.011, 0.014, 0.016, 0.019, 0.026, 0.040, 0.095],
        [0.006, 0.006, 0.007, 0.008, 0.009, 0.011, 0.014, 0.016, 0.020, 0.028, 0.044, 0.106],
        [0.006, 0.006, 0.007, 0.008, 0.009, 0.011, 0.014, 0.016, 0.020, 0.028, 0.045, 0.109],
        [0.006, 0.006, 0.007, 0.008, 0.009, 0.011, 0.014, 0.016, 0.020, 0.028, 0.045, 0.109],
        [0.006, 0.006, 0.007, 0.008, 0.009, 0.011, 0.014, 0.016, 0.020, 0.028, 0.044, 0.106],
        [0.006, 0.006, 0.007, 0.008, 0.009, 0.011, 0.014, 0.016, 0.019, 0.026, 0.040, 0.095],
        [0.006, 0.006, 0.007, 0.008, 0.009, 0.011, 0.013, 0.015, 0.017, 0.023, 0.034, 0.080]
    ])

    @staticmethod
    def calculate_xg(x, y):
        """Calcule les Expected Goals."""
        goal_center_x, goal_center_y = 120, 40
        goal_post_1_y, goal_post_2_y = 36, 44 
        distance = np.sqrt((goal_center_x - x)**2 + (goal_center_y - y)**2)
        v1 = np.array([120 - x, goal_post_1_y - y])
        v2 = np.array([120 - x, goal_post_2_y - y])
        
        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0: 
            return 0.0
            
        cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle_rad = np.arccos(np.clip(cosine_angle, -1.0, 1.0)) 
        log_odds = 1.5 + (-0.15 * distance) + (1.2 * angle_rad)
        return 1 / (1 + np.exp(-log_odds))

    @classmethod
    def calculate_dxg(cls, start_x, start_y, end_x, end_y):
        """Calcule le Delta Expected Goals (différence)."""
        return cls.calculate_xg(end_x, end_y) - cls.calculate_xg(start_x, start_y)

    @classmethod
    def get_xt_value(cls, x, y):
        """Récupère la valeur de menace d'une zone sur le terrain."""
        x, y = np.clip(x, 0, 119.9), np.clip(y, 0, 79.9)
        return cls.XT_GRID[int(y / 10)][int(x / 10)]

    @classmethod
    def calculate_dxt(cls, start_x, start_y, end_x, end_y):
        """Calcule le Delta Expected Threat (menace générée par une passe)."""
        return cls.get_xt_value(end_x, end_y) - cls.get_xt_value(start_x, start_y)