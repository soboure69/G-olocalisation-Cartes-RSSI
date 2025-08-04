"""
Module de préprocessing des données RSSI pour la géolocalisation indoor.

Ce module contient les fonctions nécessaires pour charger, nettoyer et préparer
les données RSSI pour l'entraînement des modèles de machine learning.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict, Any
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSIDataProcessor:
    """
    Classe pour le préprocessing des données RSSI.
    
    Cette classe encapsule toutes les opérations de préprocessing nécessaires
    pour préparer les données RSSI à l'entraînement des modèles.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def load_rssi_data(self, data_path: str) -> Dict[str, pd.DataFrame]:
        """
        Charge les fichiers de données RSSI.
        
        Args:
            data_path (str): Chemin vers le dossier contenant les fichiers RSSI
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionnaire contenant les DataFrames chargés
        """
        logger.info(f"Chargement des données depuis {data_path}")
        
        data_files = {
            'rssi_0': f'{data_path}/RSSI_0.csv',
            'rssi_1': f'{data_path}/RSSI_1.csv', 
            'rssi_2': f'{data_path}/RSSI_2.csv',
            'rssi_3': f'{data_path}/RSSI_3.csv'
        }
        
        dataframes = {}
        for key, file_path in data_files.items():
            try:
                df = pd.read_csv(file_path, header=None)
                dataframes[key] = df
                logger.info(f"✓ {key}: {df.shape}")
            except FileNotFoundError:
                logger.error(f"✗ Fichier non trouvé: {file_path}")
                raise
                
        return dataframes
    
    def create_feature_matrix(self, dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Crée la matrice de features à partir des données RSSI.
        
        Args:
            dataframes (Dict[str, pd.DataFrame]): Dictionnaire des DataFrames RSSI
            
        Returns:
            pd.DataFrame: Matrice de features combinée
        """
        logger.info("Création de la matrice de features")
        
        # Concaténer les données RSSI des 4 capteurs
        feature_matrices = []
        
        for key, df in dataframes.items():
            # Supprimer les colonnes avec trop de NaN
            df_clean = df.dropna(axis=1, thresh=len(df) * 0.5)
            feature_matrices.append(df_clean)
            
        # Combiner toutes les features
        X = pd.concat(feature_matrices, axis=1, ignore_index=True)
        
        # Supprimer les lignes avec des NaN
        X = X.dropna()
        
        logger.info(f"Matrice de features créée: {X.shape}")
        return X
    
    def generate_synthetic_targets(self, n_samples: int, 
                                 x_range: Tuple[float, float] = (0, 100),
                                 y_range: Tuple[float, float] = (0, 100)) -> pd.DataFrame:
        """
        Génère des coordonnées cibles synthétiques pour la démonstration.
        
        Args:
            n_samples (int): Nombre d'échantillons
            x_range (Tuple[float, float]): Plage des coordonnées X
            y_range (Tuple[float, float]): Plage des coordonnées Y
            
        Returns:
            pd.DataFrame: DataFrame avec les coordonnées X et Y
        """
        logger.info(f"Génération de {n_samples} coordonnées cibles synthétiques")
        
        np.random.seed(42)  # Pour la reproductibilité
        
        # Génération de coordonnées avec une distribution réaliste
        x_coords = np.random.uniform(x_range[0], x_range[1], n_samples)
        y_coords = np.random.uniform(y_range[0], y_range[1], n_samples)
        
        # Ajouter un peu de structure spatiale
        # Les signaux RSSI plus forts correspondent à des positions spécifiques
        targets = pd.DataFrame({
            'x': x_coords,
            'y': y_coords
        })
        
        return targets
    
    def preprocess_data(self, X: pd.DataFrame, y: pd.DataFrame, 
                       test_size: float = 0.2, 
                       random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, 
                                                       np.ndarray, np.ndarray]:
        """
        Préprocesse les données pour l'entraînement.
        
        Args:
            X (pd.DataFrame): Matrice de features
            y (pd.DataFrame): Variables cibles
            test_size (float): Proportion du jeu de test
            random_state (int): Graine aléatoire
            
        Returns:
            Tuple: X_train, X_test, y_train, y_test standardisés
        """
        logger.info("Préprocessing des données")
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Standardisation des features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.is_fitted = True
        
        logger.info(f"✓ Données d'entraînement: {X_train_scaled.shape}")
        logger.info(f"✓ Données de test: {X_test_scaled.shape}")
        
        return X_train_scaled, X_test_scaled, y_train.values, y_test.values
    
    def get_data_statistics(self, X: pd.DataFrame, y: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcule les statistiques descriptives des données.
        
        Args:
            X (pd.DataFrame): Matrice de features
            y (pd.DataFrame): Variables cibles
            
        Returns:
            Dict[str, Any]: Statistiques descriptives
        """
        stats = {
            'n_samples': len(X),
            'n_features': X.shape[1],
            'missing_values': X.isnull().sum().sum(),
            'feature_stats': X.describe(),
            'target_stats': y.describe(),
            'rssi_range': {
                'min': X.min().min(),
                'max': X.max().max(),
                'mean': X.mean().mean()
            }
        }
        
        return stats
