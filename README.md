# 🎯 Géolocalisation Indoor par Signaux RSSI

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10%2B-orange)](https://tensorflow.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.1%2B-green)](https://scikit-learn.org/)
[![Dash](https://img.shields.io/badge/Dash-2.6%2B-purple)](https://dash.plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Système intelligent de géolocalisation indoor utilisant les signaux RSSI et des techniques avancées de machine learning**

## 🌟 Vue d'ensemble

Ce projet implémente un **système de géolocalisation indoor de pointe** qui prédit avec précision la position d'objets ou de personnes dans des environnements fermés en analysant les signaux RSSI (Received Signal Strength Indicator) de multiples capteurs.

### 🎯 Objectifs du projet

- **Prédiction précise** : Estimation des coordonnées (X, Y) avec une erreur minimale
- **Comparaison de modèles** : Évaluation de 3 approches ML différentes
- **Interface interactive** : Dashboard web pour visualisation et prédiction en temps réel
- **Reproductibilité** : Code structuré avec tests et documentation complète
- **Scalabilité** : Architecture modulaire pour extension facile

### 🏆 Points forts techniques

✅ **Architecture modulaire** avec séparation des responsabilités  
✅ **Pipeline ML complet** : preprocessing → training → evaluation → deployment  
✅ **Tests unitaires** pour assurer la qualité du code  
✅ **Configuration centralisée** pour une gestion facile des paramètres  
✅ **Visualisations interactives** avec Plotly et Dash  
✅ **Documentation technique** détaillée  

---

## 🏗️ Architecture du projet

```
Géolocalisation-Cartes-RSSI/
├── 📁 src/                     # Code source principal
│   ├── data_preprocessing.py   # Traitement des données RSSI
│   ├── models.py              # Modèles ML (RF, XGBoost, DNN)
│   ├── visualization.py       # Graphiques et rapports
│   └── dashboard.py           # Interface web interactive
├── 📁 data/                   # Données RSSI brutes
├── 📁 tests/                  # Tests unitaires
├── 📁 models/                 # Modèles sauvegardés
├── 📁 reports/                # Rapports générés
├── 📁 logs/                   # Fichiers de log
├── main.py                    # Script principal
├── config.py                  # Configuration globale
└── requirements.txt           # Dépendances
```

---

## 🤖 Modèles implémentés

| Modèle | Description | Avantages |
|--------|-------------|----------|
| **Random Forest** | Ensemble de trees de décision | Robuste, interprétable, gestion des outliers |
| **XGBoost** | Gradient boosting optimisé | Performance élevée, gestion des données manquantes |
| **Deep Neural Network** | Réseau de neurones profond | Capacité d'apprentissage complexe, non-linéarités |

### 📊 Métriques d'évaluation

- **R² Score** : Coefficient de détermination
- **MAE** : Mean Absolute Error
- **MSE** : Mean Squared Error
- **RMSE** : Root Mean Squared Error
- **Erreur euclidienne** : Distance géométrique réelle

---

## 🚀 Installation et utilisation

### Prérequis

- Python 3.8+
- pip ou conda
- 8GB RAM recommandés

### Installation rapide

```bash
# Cloner le repository
git clone https://github.com/soboure69/Geolocalisation-Cartes-RSSI.git
cd Geolocalisation-Cartes-RSSI

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 🎮 Utilisation

#### 1. Pipeline complet (recommandé)

```bash
# Lancer l'entraînement complet + dashboard
python main.py
```

#### 2. Options avancées

```bash
# Entraînement seulement
python main.py --skip-dashboard

# Dashboard seulement (modèles pré-entraînés)
python main.py --dashboard-only

# Port personnalisé
python main.py --port 8080

# Chemin de données personnalisé
python main.py --data-path /path/to/your/data
```

#### 3. Interface web

Après lancement, accédez au dashboard : **http://127.0.0.1:8050**

---

## 📊 Fonctionnalités avancées

### 🔍 Analyse exploratoire des données
- Distribution des signaux RSSI par capteur
- Matrices de corrélation
- Détection des valeurs aberrantes
- Statistiques descriptives complètes

### 🎯 Prédiction en temps réel
- Interface intuitive pour saisie des valeurs RSSI
- Prédiction instantanée de position
- Visualisation sur carte interactive
- Historique des prédictions

### 📈 Visualisations interactives
- Comparaison des performances des modèles
- Cartes de chaleur des erreurs de géolocalisation
- Scatter plots prédictions vs réalité
- Graphiques d'importance des features

### 📋 Rapports automatiques
- Génération de rapports HTML complets
- Export des métriques en CSV
- Sauvegarde automatique des résultats
- Horodatage des expériences

---

## 🧪 Tests et qualité

```bash
# Lancer les tests unitaires
pytest tests/ -v

# Avec couverture de code
pytest tests/ --cov=src --cov-report=html

# Linting du code
flake8 src/
black src/ --check
```

---

## ⚙️ Configuration

Le fichier `config.py` centralise tous les paramètres :

```python
# Exemple de configuration personnalisée
from config import ProjectConfig

config = ProjectConfig()
config.models.rf_n_estimators = 200  # Plus d'arbres
config.models.dnn_epochs = 150       # Plus d'époques
config.visualization.dashboard_port = 8080  # Port personnalisé
```

---

## 📈 Résultats attendus

### Performance typique
- **R² Score** : 0.85-0.95 (selon la qualité des données)
- **Erreur euclidienne moyenne** : 2-5 mètres
- **Temps d'entraînement** : 2-10 minutes (selon le hardware)

### Cas d'usage
- **Navigation indoor** dans centres commerciaux
- **Tracking d'assets** en entrepôts
- **Systèmes de sécurité** et contrôle d'accès
- **Applications IoT** et smart buildings

---

## 🔬 Améliorations futures

- [ ] **Hyperparameter tuning** automatique avec Optuna
- [ ] **MLOps pipeline** avec MLflow
- [ ] **Modèles ensemble** avancés
- [ ] **API REST** pour intégration
- [ ] **Support multi-étages** (3D)
- [ ] **Algorithmes de filtrage** (Kalman, particules)

---

## 👥 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](docs/CONTRIBUTING.md) pour les guidelines.

### Développement

```bash
# Setup développement
pip install -e .
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install
```

---

## 📚 Documentation technique

- **[Guide d'architecture](docs/architecture.md)** : Détails techniques
- **[API Reference](docs/api.md)** : Documentation des modules
- **[Tutoriels](docs/tutorials/)** : Guides pas-à-pas
- **[FAQ](docs/faq.md)** : Questions fréquentes

---

## 📄 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

---

## 🏆 Auteur

**Projet de démonstration** - Portfolio Data Science

- 🔗 LinkedIn : [https://www.linkedin.com/in/sobourebello/](https://linkedin.com/in/sobourebello/)
- 📧 Email : soboure.bello@gmail.com
- 🌐 Portfolio : [https://github.com/soboure69](https://github.com/soboure69)

---

## ⭐ Remerciements

- Équipe de recherche en géolocalisation indoor
- Communauté open-source Python
- Contributeurs et testeurs

---

<div align="center">
  <strong>🚀 Prêt à révolutionner la géolocalisation indoor ? Commencez dès maintenant !</strong>
</div>
