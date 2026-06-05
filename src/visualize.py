import matplotlib.pyplot as plt
from mplsoccer import Pitch
from src.converter import SpadlConverter
from matplotlib.lines import Line2D # <--- Import nécessaire pour la légende

def plot_player_passes(file_path, player_name):
    # ... (Ton code de conversion reste identique jusqu'à l'étape 3) ...
    
    # 1. Utilisation du Convertisseur POO
    converter = SpadlConverter(file_path)
    evenements = converter.generate_events()
    passes = [e for e in evenements if str(e.joueur) == str(player_name) and e.type_action == 'Pass']
    
    if not passes: return None

    # 2. Création du terrain
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(10, 7))
    fig.patch.set_facecolor('#22312b')

    # 3. Tracer les passes
    for p in passes:
        couleur = '#ad993c' if p.dxt > 0 else '#8a0f0f'
        pitch.arrows(p.start_x, p.start_y, p.end_x, p.end_y, 
                     width=2, headwidth=10, headlength=10, color=couleur, ax=ax, alpha=0.7)

    # 4. AJOUT DES LABELS ET LÉGENDE (La partie qui manquait)
    
    # Titre principal
    plt.title(f"Carte de progression : {player_name}", color='white', size=18, pad=20, weight='bold')
    
    # Création des éléments de légende manuels
    legend_elements = [
        Line2D([0], [0], color='#ad993c', lw=3, label='Passe dangereuse (DXT > 0)'),
        Line2D([0], [0], color='#8a0f0f', lw=3, label='Passe neutre/risque (DXT <= 0)')
    ]
    
    # Ajout de la légende sur le terrain
    ax.legend(handles=legend_elements, loc='lower right', 
              facecolor='#22312b', edgecolor='white', labelcolor='white', fontsize=12)

    return fig