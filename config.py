import os

# Obtient le chemin absolu du dossier racine du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Définit le chemin vers le dossier data de manière dynamique
DATA_PATH = os.path.join(BASE_DIR, "data/")