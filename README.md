# Soccer Analytics Pro: Moteur VAEP

Un système d'analyse tactique de niveau industriel basé sur l'IA pour évaluer la performance des joueurs de football via le framework VAEP (Valuing Actions by Estimating Probabilities).

## 🚀 Fonctionnalités
- **Architecture POO** : Structure modulaire et orientée objet pour une maintenance facilitée.
- **IA Performante** : Calcul du score VAEP basé sur l'impact réel des actions (optimisé pour les séquences de 2 à 5 passes).
- **Interface Web** : Tableau de bord interactif avec Streamlit pour l'analyse visuelle et le scouting.
- **Traitement par lots (Batch)** : Possibilité d'analyser des saisons entières via script CLI.

## 📂 Structure du projet
- `app.py` : Interface web interactive (Streamlit).
- `main.py` : Script de traitement par lots (Batch Processing) pour les analyses saisonnières.
- `converter.py` : Moteur de conversion de données brutes vers objets métier (SPADL).
- `vaep_engine.py` : Cœur de l'IA et calcul du score VAEP.
- `math_engine.py` : Calculs mathématiques des métriques (DXT, DXG).
- `models.py` : Définition des objets métier (Joueurs, Matchs, Événements).
- `visualize.py` : Moteur de rendu graphique pour les cartes de progression.
- `requirements.txt` : Dépendances du projet.
- `.gitignore` : Configuration Git pour garder le projet propre.

## 🛠 Installation
1. Clonez le dépôt :
```bash
git clone https://github.com/ilyassbaa/soccer-analytics.git

```

2. Installez les dépendances :
```bash
pip install -r requirements.txt

```



## 🖥 Utilisation

### Mode Web (Recommandé)

Lancez l'interface interactive pour visualiser les données et explorer les joueurs :

```bash
python -m streamlit run app.py

```

### Mode Batch (Analyse de saison)

Utilisez le script `main.py` pour générer un rapport global sur tous les fichiers présents dans le dossier `data/` :

```bash
python main.py

```
