# FAQ - Questions Fréquemment Posées

## ❓ Questions Fréquentes sur le Système de Géolocalisation RSSI

## 📋 Table des Matières

- [Installation et Configuration](#installation-et-configuration)
- [Données et Formats](#données-et-formats)
- [Modèles et Performance](#modèles-et-performance)
- [Dashboard et Interface](#dashboard-et-interface)
- [Erreurs Courantes](#erreurs-courantes)
- [Performance et Optimisation](#performance-et-optimisation)

## 🛠️ Installation et Configuration

### Q: Comment installer le projet sans TensorFlow ?
**R:** Utilisez le script simplifié :
```bash
python run_without_tensorflow.py
```
Ce script fonctionne uniquement avec Random Forest et XGBoost, offrant d'excellentes performances sans les complications de TensorFlow.

### Q: TensorFlow ne s'installe pas, que faire ?
**R:** Plusieurs solutions :
1. **Solution recommandée** : Utilisez le projet sans TensorFlow
2. **Installation manuelle** :
   ```bash
   pip install tensorflow-cpu==2.13.0
   ```
3. **Script automatique** :
   ```bash
   python install_tensorflow.py
   ```

### Q: Quelles sont les versions Python supportées ?
**R:** Python 3.8 à 3.11 sont officiellement supportés. Python 3.12+ peut fonctionner mais n'est pas testé.

### Q: Comment configurer l'environnement virtuel ?
**R:**
```bash
# Créer l'environnement
python -m venv venv

# Activer (Windows)
venv\Scripts\activate

# Activer (Linux/Mac)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## 📊 Données et Formats

### Q: Quel format de données RSSI utiliser ?
**R:** Format CSV avec colonnes pour chaque point d'accès :
```csv
AP1_RSSI,AP2_RSSI,AP3_RSSI,AP4_RSSI
-45.2,-67.8,-52.1,-78.9
-43.1,-69.2,-54.3,-76.2
```

### Q: Combien de points d'accès minimum ?
**R:** Minimum 3 points d'accès pour la triangulation, mais 4-8 points d'accès donnent de meilleurs résultats.

### Q: Comment gérer les valeurs manquantes ?
**R:** Le système gère automatiquement les NaN :
- Interpolation pour les valeurs isolées
- Suppression des lignes avec trop de valeurs manquantes
- Imputation par la médiane si nécessaire

### Q: Puis-je utiliser mes propres coordonnées réelles ?
**R:** Oui, modifiez la fonction `generate_synthetic_targets()` :
```python
def load_real_coordinates(self, coord_file):
    """Charge les vraies coordonnées depuis un fichier."""
    coords = pd.read_csv(coord_file)
    return coords[['X', 'Y']].values
```

### Q: Quelle est la plage RSSI acceptable ?
**R:** Typiquement -100 dBm à -30 dBm. Le système normalise automatiquement les valeurs.

## 🤖 Modèles et Performance

### Q: Quel modèle choisir ?
**R:** Recommandations par cas d'usage :
- **Random Forest** : Polyvalent, rapide, bon par défaut
- **XGBoost** : Meilleure précision, plus lent
- **DNN** : Données complexes, nécessite TensorFlow

### Q: Quelles performances attendre ?
**R:** Performances typiques :
- **R² Score** : 0.85-0.95
- **Erreur moyenne** : 1-3 mètres
- **Temps d'entraînement** : 2-30 secondes selon le modèle

### Q: Comment améliorer la précision ?
**R:** Plusieurs approches :
1. **Plus de données** : Augmenter le dataset
2. **Plus de points d'accès** : Améliorer la couverture
3. **Hyperparamètres** : Optimiser les paramètres
4. **Ensemble** : Combiner plusieurs modèles

### Q: Le modèle peut-il fonctionner en temps réel ?
**R:** Oui, les prédictions sont très rapides :
- Random Forest : ~10ms
- XGBoost : ~5ms  
- DNN : ~1ms

## 🌐 Dashboard et Interface

### Q: Comment accéder au dashboard ?
**R:** Après avoir lancé `main.py`, ouvrez votre navigateur sur `http://127.0.0.1:8050`

### Q: Le dashboard ne se charge pas ?
**R:** Vérifications :
1. Port occupé ? Essayez un autre port :
   ```python
   dashboard.run_server(port=8051)
   ```
2. Dépendances manquantes ?
   ```bash
   pip install dash plotly
   ```
3. Firewall ? Vérifiez les paramètres réseau

### Q: Comment personnaliser le dashboard ?
**R:** Modifiez `src/dashboard.py` :
```python
# Ajouter vos propres composants
app.layout = html.Div([
    # Vos composants personnalisés
    html.H1("Mon Dashboard Personnalisé"),
    dcc.Graph(id='mon-graphique')
])
```

### Q: Peut-on exporter les résultats ?
**R:** Oui, plusieurs formats :
- **HTML** : Rapports interactifs automatiques
- **CSV** : Résultats et métriques
- **Images** : Graphiques en PNG/SVG

## 🚨 Erreurs Courantes

### Q: "ModuleNotFoundError: No module named 'tensorflow'"
**R:** TensorFlow n'est pas installé. Solutions :
1. Utiliser `run_without_tensorflow.py`
2. Installer TensorFlow : `pip install tensorflow`
3. Désactiver DNN dans la configuration

### Q: "FileNotFoundError: data/RSSI_0.csv"
**R:** Fichiers de données manquants :
1. Vérifiez que le dossier `data/` existe
2. Placez vos fichiers RSSI_*.csv dans ce dossier
3. Ou modifiez le chemin dans `config.py`

### Q: "ValueError: Input contains NaN"
**R:** Données avec valeurs manquantes :
```python
# Vérifier les données
df = pd.read_csv('data/RSSI_0.csv')
print(df.isnull().sum())

# Le système nettoie automatiquement, mais vérifiez vos données
```

### Q: "Memory Error" lors de l'entraînement
**R:** Dataset trop volumineux :
1. Réduire la taille du dataset
2. Utiliser un échantillon : `df.sample(n=1000)`
3. Augmenter la RAM ou utiliser un serveur plus puissant

### Q: Dashboard très lent
**R:** Optimisations :
1. Réduire la fréquence de mise à jour
2. Utiliser le cache pour les modèles
3. Limiter le nombre de points affichés

## ⚡ Performance et Optimisation

### Q: Comment accélérer l'entraînement ?
**R:** Plusieurs techniques :
```python
# Parallélisation
RSSIRandomForestModel(n_jobs=-1)  # Tous les CPU

# Moins d'estimateurs pour les tests
RSSIXGBoostModel(n_estimators=100)  # Au lieu de 300

# Early stopping pour DNN
RSSIDNNModel(epochs=50)  # Au lieu de 150
```

### Q: Comment réduire l'usage mémoire ?
**R:**
```python
# Batch plus petit pour DNN
dnn_model.train(X_train, y_train, batch_size=16)

# Échantillonnage des données
X_sample = X.sample(n=5000)

# Nettoyage explicite
import gc
gc.collect()
```

### Q: Peut-on utiliser un GPU ?
**R:** Oui, avec TensorFlow-GPU :
```bash
# Installation
pip install tensorflow-gpu==2.13.0

# Vérification
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### Q: Comment sauvegarder les modèles entraînés ?
**R:** Automatique dans le dossier `models/` :
```python
# Chargement manuel
import joblib
model = joblib.load('models/best_random_forest_model.pkl')
```

## 🔧 Configuration Avancée

### Q: Comment changer les hyperparamètres par défaut ?
**R:** Modifiez `config.py` :
```python
@dataclass
class ModelConfig:
    rf_n_estimators: int = 500      # Plus d'arbres
    rf_max_depth: int = 20          # Plus profond
    xgb_learning_rate: float = 0.05 # Plus conservateur
```

### Q: Comment ajouter un nouveau modèle ?
**R:** Créez une classe héritant de `BaseRSSIModel` :
```python
class MonNouveauModele(BaseRSSIModel):
    def train(self, X, y):
        # Votre implémentation
        pass
    
    def predict(self, X):
        # Votre implémentation
        pass
```

### Q: Comment modifier les métriques d'évaluation ?
**R:** Dans `models.py`, ajoutez vos métriques :
```python
def evaluate(self, X_test, y_test):
    predictions = self.predict(X_test)
    
    # Vos métriques personnalisées
    custom_metric = your_custom_function(y_test, predictions)
    
    return {
        'custom_metric': custom_metric,
        # ... autres métriques
    }
```

## 📞 Support et Aide

### Q: Où obtenir de l'aide ?
**R:** Plusieurs options :
1. **Documentation** : Consultez `docs/`
2. **Issues GitHub** : Signalez les bugs
3. **Discussions** : Questions générales
4. **Email** : support@projet-rssi.com

### Q: Comment contribuer au projet ?
**R:** Consultez `docs/CONTRIBUTING.md` pour le guide complet.

### Q: Le projet est-il open source ?
**R:** Oui, sous licence MIT. Voir `docs/LICENSE.md`.

## 🎯 Cas d'Usage Spécifiques

### Q: Utilisation en entreprise ?
**R:** Parfaitement adapté :
- Localisation d'employés
- Gestion des espaces
- Sécurité des accès
- Analytics de mouvement

### Q: Précision pour la navigation ?
**R:** Précision typique de 1-3 mètres, suffisante pour :
- Navigation indoor
- Localisation de zones
- Pas assez précis pour localisation d'objets petits

### Q: Évolutivité du système ?
**R:** Très évolutif :
- Ajout facile de nouveaux modèles
- Support de datasets volumineux
- Architecture modulaire
- API extensible

---

**Cette FAQ est mise à jour régulièrement. Pour d'autres questions, consultez la documentation ou ouvrez une issue ! 🎯📡**
