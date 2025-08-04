"""
Configuration globale du projet de géolocalisation RSSI.

Ce module contient tous les paramètres configurables du projet,
permettant une gestion centralisée des hyperparamètres et des chemins.
"""

import os
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class DataConfig:
    """Configuration pour le traitement des données."""
    
    # Chemins des données
    data_path: str = "data"
    rssi_files: List[str] = None
    
    # Paramètres de préprocessing
    test_size: float = 0.2
    random_state: int = 42
    missing_threshold: float = 0.5  # Seuil pour supprimer les colonnes avec trop de NaN
    
    # Plages des coordonnées synthétiques
    x_range: tuple = (0, 100)
    y_range: tuple = (0, 100)
    
    def __post_init__(self):
        if self.rssi_files is None:
            self.rssi_files = [
                "RSSI_0.csv",
                "RSSI_1.csv", 
                "RSSI_2.csv",
                "RSSI_3.csv"
            ]


@dataclass
class ModelConfig:
    """Configuration pour les modèles de machine learning."""
    
    # Random Forest
    rf_n_estimators: int = 100
    rf_max_depth: int = None
    rf_min_samples_split: int = 2
    rf_min_samples_leaf: int = 1
    
    # XGBoost
    xgb_n_estimators: int = 100
    xgb_learning_rate: float = 0.1
    xgb_max_depth: int = 6
    xgb_subsample: float = 0.8
    xgb_colsample_bytree: float = 0.8
    
    # Deep Neural Network
    dnn_hidden_layers: List[int] = None
    dnn_dropout_rate: float = 0.3
    dnn_learning_rate: float = 0.001
    dnn_batch_size: int = 32
    dnn_epochs: int = 100
    dnn_patience: int = 10
    
    # Paramètres généraux
    random_state: int = 42
    n_jobs: int = -1
    
    def __post_init__(self):
        if self.dnn_hidden_layers is None:
            self.dnn_hidden_layers = [128, 64, 32]


@dataclass
class VisualizationConfig:
    """Configuration pour les visualisations."""
    
    # Paramètres des graphiques
    figure_width: int = 800
    figure_height: int = 600
    color_palette: str = "Set3"
    
    # Heatmap des erreurs
    heatmap_grid_size: int = 20
    heatmap_colorscale: str = "Reds"
    
    # Dashboard
    dashboard_port: int = 8050
    dashboard_debug: bool = False
    
    # Rapports
    report_format: str = "html"
    include_interactive: bool = True


@dataclass
class PathConfig:
    """Configuration des chemins de fichiers."""
    
    # Dossiers principaux
    project_root: str = os.path.dirname(os.path.abspath(__file__))
    data_dir: str = "data"
    src_dir: str = "src"
    models_dir: str = "models"
    reports_dir: str = "reports"
    logs_dir: str = "logs"
    outputs_dir: str = "outputs"
    
    # Fichiers de sortie
    model_metrics_file: str = "model_metrics.json"
    training_log_file: str = "training.log"
    
    def get_full_path(self, relative_path: str) -> str:
        """Retourne le chemin complet à partir d'un chemin relatif."""
        return os.path.join(self.project_root, relative_path)
    
    def ensure_directories(self):
        """Crée tous les dossiers nécessaires."""
        directories = [
            self.data_dir, self.models_dir, self.reports_dir,
            self.logs_dir, self.outputs_dir
        ]
        
        for directory in directories:
            full_path = self.get_full_path(directory)
            os.makedirs(full_path, exist_ok=True)


@dataclass
class ExperimentConfig:
    """Configuration pour les expériences et le tracking."""
    
    # Métadonnées de l'expérience
    experiment_name: str = "rssi_geolocation"
    version: str = "1.0.0"
    description: str = "Géolocalisation indoor basée sur les signaux RSSI"
    
    # Paramètres d'évaluation
    cross_validation_folds: int = 5
    evaluation_metrics: List[str] = None
    
    # Sauvegarde
    save_predictions: bool = True
    save_models: bool = True
    save_plots: bool = True
    
    # Reproductibilité
    set_random_seeds: bool = True
    random_seed: int = 42
    
    def __post_init__(self):
        if self.evaluation_metrics is None:
            self.evaluation_metrics = [
                "r2_score", "mae", "mse", "rmse", "mean_euclidean_error"
            ]


class ProjectConfig:
    """Configuration principale du projet."""
    
    def __init__(self):
        self.data = DataConfig()
        self.models = ModelConfig()
        self.visualization = VisualizationConfig()
        self.paths = PathConfig()
        self.experiment = ExperimentConfig()
        
        # Assurer que les dossiers existent
        self.paths.ensure_directories()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit la configuration en dictionnaire."""
        return {
            "data": self.data.__dict__,
            "models": self.models.__dict__,
            "visualization": self.visualization.__dict__,
            "paths": self.paths.__dict__,
            "experiment": self.experiment.__dict__
        }
    
    def save_config(self, filepath: str = None):
        """Sauvegarde la configuration dans un fichier JSON."""
        import json
        
        if filepath is None:
            filepath = self.paths.get_full_path("config.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_config(cls, filepath: str):
        """Charge la configuration depuis un fichier JSON."""
        import json
        
        with open(filepath, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        
        config = cls()
        
        # Mettre à jour les configurations
        for section_name, section_data in config_dict.items():
            if hasattr(config, section_name):
                section = getattr(config, section_name)
                for key, value in section_data.items():
                    if hasattr(section, key):
                        setattr(section, key, value)
        
        return config


# Configuration par défaut
DEFAULT_CONFIG = ProjectConfig()


# Fonctions utilitaires
def get_config() -> ProjectConfig:
    """Retourne la configuration par défaut."""
    return DEFAULT_CONFIG


def set_random_seeds(seed: int = None):
    """Configure les graines aléatoires pour la reproductibilité."""
    import random
    import numpy as np
    import tensorflow as tf
    
    if seed is None:
        seed = DEFAULT_CONFIG.experiment.random_seed
    
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    
    # Pour sklearn
    import os
    os.environ['PYTHONHASHSEED'] = str(seed)


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """Configure le système de logging."""
    import logging
    
    if log_file is None:
        log_file = DEFAULT_CONFIG.paths.get_full_path(
            os.path.join(DEFAULT_CONFIG.paths.logs_dir, 
                        DEFAULT_CONFIG.paths.training_log_file)
        )
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


# Variables d'environnement
def load_env_variables():
    """Charge les variables d'environnement si disponibles."""
    import os
    
    # Exemple de variables d'environnement
    env_vars = {
        'RSSI_DATA_PATH': 'data',
        'RSSI_MODEL_PATH': 'models',
        'RSSI_LOG_LEVEL': 'INFO',
        'RSSI_DASHBOARD_PORT': '8050'
    }
    
    config = get_config()
    
    # Mettre à jour la configuration avec les variables d'environnement
    if 'RSSI_DATA_PATH' in os.environ:
        config.data.data_path = os.environ['RSSI_DATA_PATH']
    
    if 'RSSI_DASHBOARD_PORT' in os.environ:
        config.visualization.dashboard_port = int(os.environ['RSSI_DASHBOARD_PORT'])
    
    return config


if __name__ == "__main__":
    # Test de la configuration
    config = ProjectConfig()
    print("Configuration du projet:")
    print(f"- Dossier de données: {config.data.data_path}")
    print(f"- Nombre d'estimateurs RF: {config.models.rf_n_estimators}")
    print(f"- Port du dashboard: {config.visualization.dashboard_port}")
    
    # Sauvegarder la configuration
    config.save_config()
    print("Configuration sauvegardée dans config.json")
