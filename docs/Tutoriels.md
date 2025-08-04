# Tutoriels

## 🎓 Guides Pratiques pour le Système de Géolocalisation RSSI

## 🚀 Démarrage Rapide

### Installation Express (5 minutes)
```bash
# 1. Cloner le projet
git clone https://github.com/soboure69/geolocalisation-rssi.git
cd geolocalisation-rssi

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer le projet
python main.py
```

### Premier Test
```bash
# Test sans TensorFlow (plus rapide)
python run_without_tensorflow.py

# Ou installation complète avec TensorFlow
python install_tensorflow.py
```

## 📚 Tutoriel Complet

### Étape 1: Préparation des Données

#### Format des Données RSSI
```csv
AP1_RSSI,AP2_RSSI,AP3_RSSI,...,APn_RSSI
-45.2,-67.8,-52.1,...,-78.9
-43.1,-69.2,-54.3,...,-76.2
```

#### Placement des Fichiers
```bash
data/
├── RSSI_0.csv    # Données de la zone 1
├── RSSI_1.csv    # Données de la zone 2
├── RSSI_2.csv    # Données de la zone 3
└── RSSI_3.csv    # Données de la zone 4
```

### Étape 2: Configuration
```python
# config.py - Personnaliser selon vos besoins
@dataclass
class DataConfig:
    data_path: str = "data"
    test_size: float = 0.2
    random_state: int = 42
```

### Étape 3: Entraînement
```python
from src.data_preprocessing import RSSIDataProcessor
from src.models import ModelManager, RSSIRandomForestModel

def main():
    # 1. Chargement des données
    processor = RSSIDataProcessor()
    dataframes = processor.load_rssi_data('data')
    
    # 2. Préparation
    X = processor.create_feature_matrix(dataframes)
    y = processor.generate_synthetic_targets(len(X))
    X_train, X_test, y_train, y_test = processor.preprocess_data(X, y)
    
    # 3. Entraînement
    manager = ModelManager()
    manager.add_model("Random Forest", RSSIRandomForestModel())
    manager.train_all_models(X_train, y_train)
    
    # 4. Évaluation
    manager.evaluate_all_models(X_test, y_test)
    return manager
```

### Étape 4: Dashboard
```python
from src.dashboard import create_dashboard

dashboard = create_dashboard(model_manager, stats)
dashboard.run_server(debug=True, port=8050)
```

## 🔧 Utilisation Avancée

### Optimisation des Hyperparamètres
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 15, 20]
}

grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)
```

### Ajouter un Nouveau Modèle
```python
class RSSISVMModel(BaseRSSIModel):
    def __init__(self, **kwargs):
        self.model = SVR(**kwargs)
    
    def train(self, X, y):
        self.model.fit(X, y)
    
    def predict(self, X):
        return self.model.predict(X)
```

## 💡 Cas d'Usage

### 1. Bureau d'Entreprise
- Localisation d'employés
- Gestion des espaces
- Sécurité des accès

### 2. Centre Commercial
- Navigation client
- Analyse de trafic
- Marketing géolocalisé

### 3. Hôpital
- Suivi des équipements
- Localisation du personnel
- Gestion des urgences

## 🆘 Dépannage

### Problèmes Courants

#### TensorFlow non installé
```bash
# Solution 1: Utiliser sans TensorFlow
python run_without_tensorflow.py

# Solution 2: Installer TensorFlow
pip install tensorflow==2.13.0
```

#### Erreur de données
```python
# Vérifier le format des données
processor = RSSIDataProcessor()
dataframes = processor.load_rssi_data('data')
print(f"Forme des données: {[df.shape for df in dataframes]}")
```

#### Dashboard ne démarre pas
```bash
# Vérifier les dépendances
pip install dash plotly

# Lancer sur un autre port
dashboard.run_server(port=8051)
```

---

**Pour plus d'aide, consultez FAQ.md ou ouvrez une issue GitHub ! 🎯**
