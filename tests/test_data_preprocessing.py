"""
Tests unitaires pour le module de préprocessing des données RSSI.
"""

import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from unittest.mock import patch, MagicMock

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.data_preprocessing import RSSIDataProcessor


class TestRSSIDataProcessor:
    """Tests pour la classe RSSIDataProcessor."""
    
    def setup_method(self):
        """Configuration avant chaque test."""
        self.processor = RSSIDataProcessor()
        
    def test_initialization(self):
        """Test de l'initialisation du processeur."""
        assert self.processor.scaler is not None
        assert not self.processor.is_fitted
        
    def test_create_feature_matrix(self):
        """Test de création de la matrice de features."""
        # Créer des données de test
        test_data = {
            'rssi_0': pd.DataFrame(np.random.randn(100, 50)),
            'rssi_1': pd.DataFrame(np.random.randn(100, 50)),
            'rssi_2': pd.DataFrame(np.random.randn(100, 50)),
            'rssi_3': pd.DataFrame(np.random.randn(100, 50))
        }
        
        # Tester la création de la matrice
        X = self.processor.create_feature_matrix(test_data)
        
        assert isinstance(X, pd.DataFrame)
        assert len(X) > 0
        assert X.shape[1] > 0
        
    def test_generate_synthetic_targets(self):
        """Test de génération des coordonnées synthétiques."""
        n_samples = 100
        targets = self.processor.generate_synthetic_targets(n_samples)
        
        assert isinstance(targets, pd.DataFrame)
        assert len(targets) == n_samples
        assert list(targets.columns) == ['x', 'y']
        assert targets['x'].min() >= 0
        assert targets['x'].max() <= 100
        assert targets['y'].min() >= 0
        assert targets['y'].max() <= 100
        
    def test_preprocess_data(self):
        """Test du préprocessing complet."""
        # Créer des données de test
        X = pd.DataFrame(np.random.randn(100, 20))
        y = pd.DataFrame({
            'x': np.random.uniform(0, 100, 100),
            'y': np.random.uniform(0, 100, 100)
        })
        
        # Préprocesser
        X_train, X_test, y_train, y_test = self.processor.preprocess_data(X, y)
        
        # Vérifications
        assert X_train.shape[0] == 80  # 80% pour l'entraînement
        assert X_test.shape[0] == 20   # 20% pour le test
        assert y_train.shape[0] == 80
        assert y_test.shape[0] == 20
        assert self.processor.is_fitted
        
    def test_get_data_statistics(self):
        """Test du calcul des statistiques."""
        X = pd.DataFrame(np.random.randn(100, 20))
        y = pd.DataFrame({
            'x': np.random.uniform(0, 100, 100),
            'y': np.random.uniform(0, 100, 100)
        })
        
        stats = self.processor.get_data_statistics(X, y)
        
        assert 'n_samples' in stats
        assert 'n_features' in stats
        assert 'missing_values' in stats
        assert 'feature_stats' in stats
        assert 'target_stats' in stats
        assert 'rssi_range' in stats
        
        assert stats['n_samples'] == 100
        assert stats['n_features'] == 20
        
    @patch('pandas.read_csv')
    def test_load_rssi_data_success(self, mock_read_csv):
        """Test du chargement réussi des données RSSI."""
        # Mock des données CSV
        mock_df = pd.DataFrame(np.random.randn(100, 50))
        mock_read_csv.return_value = mock_df
        
        # Test du chargement
        with tempfile.TemporaryDirectory() as temp_dir:
            # Créer des fichiers factices
            for i in range(4):
                file_path = os.path.join(temp_dir, f'RSSI_{i}.csv')
                mock_df.to_csv(file_path, index=False)
            
            dataframes = self.processor.load_rssi_data(temp_dir)
            
            assert len(dataframes) == 4
            assert all(f'rssi_{i}' in dataframes for i in range(4))
            
    def test_load_rssi_data_file_not_found(self):
        """Test du chargement avec fichier manquant."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Ne pas créer les fichiers
            with pytest.raises(FileNotFoundError):
                self.processor.load_rssi_data(temp_dir)
                
    def test_create_feature_matrix_with_nan(self):
        """Test de création de matrice avec des valeurs NaN."""
        # Créer des données avec des NaN
        test_data = {
            'rssi_0': pd.DataFrame(np.random.randn(100, 50)),
            'rssi_1': pd.DataFrame(np.random.randn(100, 50)),
            'rssi_2': pd.DataFrame(np.random.randn(100, 50)),
            'rssi_3': pd.DataFrame(np.random.randn(100, 50))
        }
        
        # Ajouter des NaN
        test_data['rssi_0'].iloc[:, :10] = np.nan
        
        X = self.processor.create_feature_matrix(test_data)
        
        # Vérifier que les NaN ont été gérés
        assert not X.isnull().any().any()
        
    def test_synthetic_targets_custom_ranges(self):
        """Test de génération avec des plages personnalisées."""
        n_samples = 50
        x_range = (10, 90)
        y_range = (20, 80)
        
        targets = self.processor.generate_synthetic_targets(
            n_samples, x_range, y_range
        )
        
        assert targets['x'].min() >= x_range[0]
        assert targets['x'].max() <= x_range[1]
        assert targets['y'].min() >= y_range[0]
        assert targets['y'].max() <= y_range[1]


class TestIntegration:
    """Tests d'intégration pour le pipeline complet."""
    
    def test_full_pipeline(self):
        """Test du pipeline complet de préprocessing."""
        processor = RSSIDataProcessor()
        
        # Créer des données de test réalistes
        test_dataframes = {}
        for i in range(4):
            # Simuler des données RSSI avec des valeurs réalistes
            data = np.random.uniform(-80, -30, (200, 100))
            # Ajouter quelques NaN
            mask = np.random.random((200, 100)) < 0.1
            data[mask] = np.nan
            test_dataframes[f'rssi_{i}'] = pd.DataFrame(data)
        
        # Pipeline complet
        X = processor.create_feature_matrix(test_dataframes)
        y = processor.generate_synthetic_targets(len(X))
        X_train, X_test, y_train, y_test = processor.preprocess_data(X, y)
        stats = processor.get_data_statistics(X, y)
        
        # Vérifications finales
        assert X_train.shape[0] > 0
        assert X_test.shape[0] > 0
        assert y_train.shape[0] == X_train.shape[0]
        assert y_test.shape[0] == X_test.shape[0]
        assert stats['n_samples'] > 0
        assert stats['n_features'] > 0
        assert processor.is_fitted


if __name__ == "__main__":
    pytest.main([__file__])
