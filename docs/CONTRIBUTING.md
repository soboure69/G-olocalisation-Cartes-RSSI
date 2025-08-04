# Guide de Contribution

## 🤝 Comment Contribuer au Projet Géolocalisation RSSI

Merci de votre intérêt pour contribuer à ce projet ! Ce guide vous explique comment participer efficacement au développement.

## 📋 Table des Matières

- [Code de Conduite](#code-de-conduite)
- [Types de Contributions](#types-de-contributions)
- [Configuration de l'Environnement](#configuration-de-lenvironnement)
- [Processus de Contribution](#processus-de-contribution)
- [Standards de Code](#standards-de-code)
- [Tests](#tests)
- [Documentation](#documentation)

## 🤖 Code de Conduite

Ce projet adhère aux principes suivants :
- **Respect** : Traiter tous les contributeurs avec respect
- **Collaboration** : Favoriser un environnement collaboratif
- **Qualité** : Maintenir des standards de code élevés
- **Apprentissage** : Encourager l'apprentissage mutuel

## 🎯 Types de Contributions

### 🐛 Rapports de Bugs
- Utilisez les templates d'issues GitHub
- Incluez des étapes de reproduction détaillées
- Fournissez les informations système (OS, Python, versions)

### ✨ Nouvelles Fonctionnalités
- Discutez d'abord dans une issue
- Proposez une conception claire
- Implémentez avec des tests

### 📚 Documentation
- Améliorations du README
- Ajout d'exemples
- Corrections de typos
- Traductions

### 🔧 Améliorations de Code
- Optimisations de performance
- Refactoring
- Correction de code smell

## 🛠️ Configuration de l'Environnement

### Prérequis
```bash
# Python 3.8+
python --version

# Git
git --version
```

### Installation pour Développement
```bash
# 1. Cloner le repository
git clone https://github.com/votre-username/geolocalisation-rssi.git
cd geolocalisation-rssi

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Installer les dépendances de développement
pip install -r requirements.txt
pip install -e .

# 4. Installer les outils de développement
pip install pre-commit
pre-commit install
```

### Vérification de l'Installation
```bash
# Lancer les tests
pytest tests/

# Vérifier le style de code
flake8 src/
black --check src/
isort --check-only src/
```

## 🔄 Processus de Contribution

### 1. Fork et Clone
```bash
# Fork sur GitHub, puis clone
git clone https://github.com/VOTRE-USERNAME/geolocalisation-rssi.git
cd geolocalisation-rssi
git remote add upstream https://github.com/ORIGINAL-OWNER/geolocalisation-rssi.git
```

### 2. Créer une Branche
```bash
# Créer une branche pour votre feature/fix
git checkout -b feature/nom-de-votre-feature
# ou
git checkout -b fix/description-du-fix
```

### 3. Développer
- Écrivez du code propre et documenté
- Ajoutez des tests pour vos modifications
- Respectez les conventions de nommage
- Committez régulièrement avec des messages clairs

### 4. Tests et Qualité
```bash
# Lancer tous les tests
pytest tests/ -v

# Vérifier la couverture
pytest --cov=src tests/

# Formater le code
black src/ tests/
isort src/ tests/

# Vérifier le linting
flake8 src/ tests/
```

### 5. Pull Request
```bash
# Pousser votre branche
git push origin feature/nom-de-votre-feature

# Créer une Pull Request sur GitHub
```

## 📏 Standards de Code

### Style Python
- **PEP 8** : Standard de style Python
- **Black** : Formatage automatique
- **isort** : Tri des imports
- **flake8** : Linting

### Conventions de Nommage
```python
# Variables et fonctions : snake_case
def process_rssi_data():
    signal_strength = -45

# Classes : PascalCase
class RSSIDataProcessor:
    pass

# Constantes : UPPER_CASE
MAX_SIGNAL_STRENGTH = -30
```

### Documentation
```python
def train_model(X_train: np.ndarray, y_train: np.ndarray) -> Dict[str, Any]:
    """
    Entraîne un modèle de géolocalisation RSSI.
    
    Args:
        X_train: Données d'entraînement (n_samples, n_features)
        y_train: Cibles d'entraînement (n_samples, 2)
        
    Returns:
        Dict contenant les métriques d'entraînement
        
    Raises:
        ValueError: Si les données sont invalides
    """
    pass
```

### Messages de Commit
```
type(scope): description courte

Description plus détaillée si nécessaire

- feat: nouvelle fonctionnalité
- fix: correction de bug
- docs: documentation
- style: formatage
- refactor: refactoring
- test: ajout de tests
- chore: maintenance

Exemples:
feat(models): ajouter support pour XGBoost
fix(preprocessing): corriger gestion des NaN
docs(readme): mettre à jour instructions d'installation
```

## 🧪 Tests

### Structure des Tests
```
tests/
├── test_data_preprocessing.py
├── test_models.py
├── test_visualization.py
├── test_dashboard.py
└── conftest.py
```

### Écriture de Tests
```python
import pytest
import numpy as np
from src.data_preprocessing import RSSIDataProcessor

class TestRSSIDataProcessor:
    def test_load_rssi_data(self):
        """Test le chargement des données RSSI."""
        processor = RSSIDataProcessor()
        # Test implementation
        
    def test_preprocess_data_invalid_input(self):
        """Test la gestion des entrées invalides."""
        with pytest.raises(ValueError):
            # Test qui doit lever une exception
```

### Lancer les Tests
```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=src

# Tests spécifiques
pytest tests/test_models.py::TestRSSIRandomForestModel

# Tests en mode verbose
pytest -v
```

## 📖 Documentation

### Types de Documentation
1. **Docstrings** : Documentation du code
2. **README** : Vue d'ensemble du projet
3. **Tutoriels** : Guides pas à pas
4. **API Reference** : Documentation technique

### Génération de Documentation
```bash
# Installer sphinx (si nécessaire)
pip install sphinx sphinx-rtd-theme

# Générer la documentation
cd docs/
make html
```

## 🚀 Checklist avant Pull Request

- [ ] Les tests passent tous
- [ ] Le code respecte les standards de style
- [ ] La documentation est mise à jour
- [ ] Les nouveaux fichiers ont des headers appropriés
- [ ] Les dépendances sont mises à jour si nécessaire
- [ ] La Pull Request a une description claire
- [ ] Les commits ont des messages descriptifs

## 🆘 Aide et Support

### Ressources
- **Issues GitHub** : Pour les bugs et questions
- **Discussions** : Pour les idées et discussions générales
- **Wiki** : Documentation détaillée
- **Email** : contact@projet-rssi.com

### Mentors et Reviewers
- **@maintainer1** : Architecture et modèles ML
- **@maintainer2** : Frontend et visualisations
- **@maintainer3** : Tests et CI/CD

## 🏆 Reconnaissance

Les contributeurs sont reconnus dans :
- Le fichier `CONTRIBUTORS.md`
- Les release notes
- La page "About" du projet

### Hall of Fame
Contributeurs avec plus de 10 commits :
- 🥇 **Contributeur Principal** - 50+ commits
- 🥈 **Contributeur Actif** - 25+ commits
- 🥉 **Contributeur Régulier** - 10+ commits

## 📝 Licence

En contribuant à ce projet, vous acceptez que vos contributions soient sous la même licence que le projet (voir `LICENSE.md`).

---

**Merci de contribuer à l'amélioration de la géolocalisation indoor ! 🎯📡**
