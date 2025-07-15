# Géolocalisation-Cartes-RSSI
Construction d’une fonction qui à partir des 4 forces de signal des bornes (cartes RSSI) reçues donne la position (géolocalisation)

# Projet de Prédiction de Position à partir de Données RSSI

Ce projet vise à estimer la position d'un objet ou d'une personne dans un environnement fermé (indoor positioning) à l'aide de signaux RSSI (Received Signal Strength Indicator) émis par des capteurs. L'approche combine plusieurs modèles de machine learning afin de comparer leurs performances et de sélectionner automatiquement le meilleur.

---

## 📁 Contenu du projet

* `notebook.ipynb` : Script principal avec entraînement, évaluation, dashboard interactif et export HTML.
* `modeles_sauvegardes/` : Contient le meilleur modèle sauvegardé.
* `rapports/` : Contient un rapport HTML complet (scores, heatmaps, etc).

---

## 🌐 Objectif

Prédire la position (X, Y) d'un point à partir d'un vecteur RSSI en utilisant :

* Random Forest
* XGBoost
* Deep Neural Network (TensorFlow/Keras)

Puis :

* Comparer les performances (R², MAE, MSE)
* Générer un dashboard et un rapport automatique

---

## 🤖 Données attendues

* Données RSSI en entrée : matrice de `n x m` (n exemples, m capteurs)
* Cibles : coordonnées X et Y réelles

---

## 🚀 Fonctionnalités principales

### 1. Entraînement multi-modèle

* Standardisation des données
* Entraînement de 3 modèles de régression multi-sorties
* Évaluation via R², MAE, MSE
* Sélection automatique du meilleur modèle selon le R²

### 2. Sauvegarde automatique du meilleur modèle

* En `joblib` pour les modèles classiques
* En `.h5` pour le DNN (Keras)

### 3. Cartes de chaleur des erreurs

* Calcul de l'erreur spatiale (distance euclidienne)
* Cartes de chaleur interactives avec `plotly`

### 4. Dashboard interactif (Dash)

* Visualisation des performances
* Saisie utilisateur en direct pour la prédiction
* Carte de la position prédite

### 5. Rapport HTML généré automatiquement

* Scores par modèle
* Visualisations des erreurs
* Stocké dans le dossier `/rapports/`

---

## 📊 Exécution

```bash
# Installer les dépendances (exemple avec pip)
pip install -r requirements.txt

# Lancer le notebook

```

Puis accéder à l'interface sur : [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## 🔍 Exemples de visualisations

* Graphique barres comparatif : R², MAE, MSE
* Cartes de chaleur interactives d'erreurs
* Carte de position prédite (avec le point rouge)

---

## 📖 Auteurs & Crédits

Projet réalisé dans le cadre d'une évaluation de compétences en data science appliquée à la géolocalisation indoor.

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Vous pouvez l'utiliser, le modifier et le redistribuer librement.
