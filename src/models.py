"""
Module des modèles de machine learning pour la géolocalisation RSSI.

Ce module contient les implémentations des différents modèles utilisés pour
prédire la position à partir des signaux RSSI.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb

# Import TensorFlow avec gestion d'erreurs robuste
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, optimizers, callbacks
    
    # Vérifier que TensorFlow fonctionne correctement
    tf.config.experimental.enable_tensor_float_32_execution(False)
    
    # Configuration pour éviter les warnings
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    TENSORFLOW_AVAILABLE = True
    print(f"✅ TensorFlow {tf.__version__} disponible et configuré")
    
except ImportError as e:
    print(f"⚠️ TensorFlow non disponible: {e}")
    print("💡 Le projet fonctionnera avec Random Forest et XGBoost uniquement")
    TENSORFLOW_AVAILABLE = False
    tf = None
    keras = None
    
except Exception as e:
    print(f"⚠️ Erreur lors de la configuration TensorFlow: {e}")
    print("💡 TensorFlow installé mais configuration échouée")
    TENSORFLOW_AVAILABLE = False
    tf = None
    keras = None

import joblib
from typing import Dict, Tuple, Any, List
import logging
import os

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Classe pour évaluer les performances des modèles."""
    
    @staticmethod
    def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calcule les métriques de performance pour un modèle.
        
        Args:
            y_true (np.ndarray): Valeurs réelles
            y_pred (np.ndarray): Valeurs prédites
            
        Returns:
            Dict[str, float]: Dictionnaire des métriques
        """
        metrics = {
            'r2_score': r2_score(y_true, y_pred),
            'mae': mean_absolute_error(y_true, y_pred),
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred))
        }
        
        # Calcul de l'erreur euclidienne moyenne pour la géolocalisation
        if y_true.shape[1] == 2:  # Coordonnées X, Y
            euclidean_errors = np.sqrt(
                (y_true[:, 0] - y_pred[:, 0])**2 + 
                (y_true[:, 1] - y_pred[:, 1])**2
            )
            metrics['mean_euclidean_error'] = np.mean(euclidean_errors)
            metrics['median_euclidean_error'] = np.median(euclidean_errors)
            
        return metrics


class RSSIRandomForestModel:
    """Modèle Random Forest pour la géolocalisation RSSI."""
    
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1
        )
        self.is_trained = False
        
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Entraîne le modèle Random Forest."""
        logger.info("Entraînement du modèle Random Forest...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("✓ Random Forest entraîné")
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Effectue des prédictions."""
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant de faire des prédictions")
        return self.model.predict(X)
    
    def get_feature_importance(self) -> np.ndarray:
        """Retourne l'importance des features."""
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné")
        return self.model.feature_importances_


class RSSIXGBoostModel:
    """Modèle XGBoost pour la géolocalisation RSSI."""
    
    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1, 
                 random_state: int = 42):
        self.model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=random_state,
            n_jobs=-1
        )
        self.is_trained = False
        
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Entraîne le modèle XGBoost."""
        logger.info("Entraînement du modèle XGBoost...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("✓ XGBoost entraîné")
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Effectue des prédictions."""
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant de faire des prédictions")
        return self.model.predict(X)


class RSSIDNNModel:
    """Modèle Deep Neural Network pour la géolocalisation RSSI."""
    
    def __init__(self, input_dim: int, hidden_layers: List[int] = [128, 64, 32]):
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow n'est pas disponible. Installez-le avec: pip install tensorflow")
        
        self.input_dim = input_dim
        self.hidden_layers = hidden_layers
        self.model = self._build_model()
        self.is_trained = False
        
    def _build_model(self) -> keras.Model:
        """Construit l'architecture du réseau de neurones optimisée."""
        model = keras.Sequential()
        
        # Couche d'entrée avec normalisation
        model.add(layers.Dense(self.hidden_layers[0], 
                              activation='relu', 
                              input_shape=(self.input_dim,),
                              kernel_regularizer=keras.regularizers.l2(0.001)))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.3))
        
        # Couches cachées avec normalisation
        for units in self.hidden_layers[1:]:
            model.add(layers.Dense(units, 
                                 activation='relu',
                                 kernel_regularizer=keras.regularizers.l2(0.001)))
            model.add(layers.BatchNormalization())
            model.add(layers.Dropout(0.3))
            
        # Couche de sortie (2 neurones pour X et Y)
        model.add(layers.Dense(2, activation='linear'))
        
        # Compilation avec optimiseur amélioré
        optimizer = keras.optimizers.Adam(
            learning_rate=0.001,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-07
        )
        
        model.compile(
            optimizer=optimizer,
            loss='mse',
            metrics=['mae', 'mse']
        )
        
        return model
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
              X_val: np.ndarray = None, y_val: np.ndarray = None,
              epochs: int = 150, batch_size: int = 32) -> keras.callbacks.History:
        """Entraîne le modèle DNN avec callbacks avancés."""
        logger.info("Entraînement du modèle DNN...")
        
        # Callbacks améliorés
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss' if X_val is not None else 'loss',
                patience=15, 
                restore_best_weights=True,
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss' if X_val is not None else 'loss',
                factor=0.5, 
                patience=8,
                min_lr=1e-7,
                verbose=1
            ),
            keras.callbacks.ModelCheckpoint(
                'models/best_dnn_model.h5',
                monitor='val_loss' if X_val is not None else 'loss',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Créer le dossier models s'il n'existe pas
        os.makedirs('models', exist_ok=True)
        
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
            logger.info(f"Utilisation de données de validation: {X_val.shape[0]} échantillons")
            
        history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1,
            shuffle=True
        )
        
        self.is_trained = True
        logger.info(f"✓ DNN entraîné sur {len(history.history['loss'])} époques")
        return history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Effectue des prédictions."""
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant de faire des prédictions")
        return self.model.predict(X)


class ModelManager:
    """Gestionnaire pour entraîner et comparer plusieurs modèles."""
    
    def __init__(self):
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_score = -np.inf
        
    def add_model(self, name: str, model) -> None:
        """Ajoute un modèle au gestionnaire."""
        self.models[name] = model
        
    def train_all_models(self, X_train: np.ndarray, y_train: np.ndarray,
                        X_val: np.ndarray = None, y_val: np.ndarray = None) -> None:
        """Entraîne tous les modèles."""
        logger.info("Entraînement de tous les modèles...")
        
        for name, model in self.models.items():
            logger.info(f"Entraînement de {name}...")
            
            if isinstance(model, RSSIDNNModel) and X_val is not None:
                model.train(X_train, y_train, X_val, y_val)
            else:
                model.train(X_train, y_train)
                
    def evaluate_all_models(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Dict]:
        """Évalue tous les modèles sur le jeu de test."""
        logger.info("Évaluation de tous les modèles...")
        
        for name, model in self.models.items():
            logger.info(f"Évaluation de {name}...")
            
            y_pred = model.predict(X_test)
            metrics = ModelEvaluator.calculate_metrics(y_test, y_pred)
            
            self.results[name] = {
                'model': model,
                'predictions': y_pred,
                'metrics': metrics
            }
            
            # Mise à jour du meilleur modèle
            if metrics['r2_score'] > self.best_score:
                self.best_score = metrics['r2_score']
                self.best_model = name
                
        logger.info(f"Meilleur modèle: {self.best_model} (R² = {self.best_score:.4f})")
        
    def get_results_summary(self) -> pd.DataFrame:
        """Retourne un résumé des résultats."""
        summary_data = []
        
        for name, result in self.results.items():
            metrics = result['metrics']
            summary_data.append({
                'Model': name,
                'R²': metrics['r2_score'],
                'MAE': metrics['mae'],
                'MSE': metrics['mse'],
                'RMSE': metrics['rmse'],
                'Mean_Euclidean_Error': metrics.get('mean_euclidean_error', 'N/A')
            })
            
        return pd.DataFrame(summary_data).sort_values('R²', ascending=False)
    
    def save_best_model(self, save_path: str) -> None:
        """Sauvegarde le meilleur modèle."""
        if self.best_model is None:
            raise ValueError("Aucun modèle n'a été évalué")
            
        os.makedirs(save_path, exist_ok=True)
        best_model_obj = self.results[self.best_model]['model']
        
        if isinstance(best_model_obj, RSSIDNNModel):
            model_path = os.path.join(save_path, f"{self.best_model}_model.h5")
            best_model_obj.model.save(model_path)
        else:
            model_path = os.path.join(save_path, f"{self.best_model}_model.joblib")
            joblib.dump(best_model_obj.model, model_path)
            
        logger.info(f"Meilleur modèle sauvegardé: {model_path}")
        
        # Sauvegarder les métriques
        metrics_path = os.path.join(save_path, "model_metrics.json")
        import json
        with open(metrics_path, 'w') as f:
            json.dump(self.results[self.best_model]['metrics'], f, indent=2)
