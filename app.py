import streamlit as st
import os
from src.converter import SpadlConverter
from src.vaep_engine import VAEPEngine
from src.visualize import plot_player_passes
from config import DATA_PATH

st.set_page_config(page_title="Soccer Analytics Pro", layout="wide")

st.title("⚽ Soccer Analytics Pro - Moteur VAEP")

# --- FONCTION CACHÉE (Pour ne pas recalculer à chaque fois) ---
@st.cache_data
def run_analysis(file_path):
    # Transformation en objets POO
    converter = SpadlConverter(file_path)
    evenements = converter.generate_events()
    
    # Moteur VAEP
    engine = VAEPEngine(evenements)
    engine.extract_phases()
    engine.train_and_calculate_vaep()
    
    # Retourne le classement
    return engine.get_player_rankings()

# --- SIDEBAR ---
source = st.sidebar.radio("Source des données", ["Uploader un fichier", "Fichiers du dossier local"])

if source == "Uploader un fichier":
    file_path = st.sidebar.file_uploader("Choisir un CSV", type="csv")
else:
    fichiers = [f for f in os.listdir(DATA_PATH) if f.endswith('.csv')]
    selected = st.sidebar.selectbox("Sélectionnez un match", fichiers)
    file_path = os.path.join(DATA_PATH, selected)

# --- ANALYSE ---
if file_path:
    # On lance l'analyse uniquement si on change de fichier
    df = run_analysis(file_path)
    
    st.write("### 🏆 Classement des joueurs", df.head(10))
    
    # --- VISUALISATION ---
    st.write("### 🎨 Visualisation individuelle")
    joueurs = sorted([str(j) for j in df['Joueur'].unique()])
    joueur_select = st.selectbox("Choisir un joueur pour voir ses passes", joueurs)
    
    # Ici, pas besoin de bouton, le simple changement de joueur met à jour l'image
    fig = plot_player_passes(file_path, joueur_select)
    if fig:
        st.pyplot(fig)
else:
    st.info("Veuillez sélectionner ou uploader un fichier pour commencer l'analyse.")