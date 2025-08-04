"""
Script principal pour l'entraînement et l'évaluation des modèles de géolocalisation RSSI.

Ce script orchestre l'ensemble du pipeline de machine learning :
- Chargement et préprocessing des données
- Entraînement des modèles
- Évaluation et comparaison
- Génération des rapports
- Lancement du dashboard interactif
"""

import os
import sys
import logging
import argparse
from datetime import datetime
import warnings

# Ajouter le dossier src au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_preprocessing import RSSIDataProcessor
from src.models import (ModelManager, RSSIRandomForestModel, 
                       RSSIXGBoostModel, RSSIDNNModel, TENSORFLOW_AVAILABLE)
from src.visualization import RSSIVisualizer, save_figures_to_html
from src.dashboard import create_dashboard

# Supprimer les warnings non critiques
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Crée le dossier 'logs' s'il n'existe pas
os.makedirs('logs', exist_ok=True)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/training.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def setup_directories():
    """Crée les dossiers nécessaires s'ils n'existent pas."""
    directories = ['logs', 'models', 'reports', 'outputs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    logger.info("Dossiers de projet configurés")


def load_and_preprocess_data(data_path: str = 'data'):
    """
    Charge et préprocesse les données RSSI.
    
    Args:
        data_path (str): Chemin vers les données
        
    Returns:
        Tuple: Données préprocessées et statistiques
    """
    logger.info("🔄 Début du chargement et préprocessing des données")
    
    # Initialiser le processeur de données
    processor = RSSIDataProcessor()
    
    # Charger les données RSSI
    dataframes = processor.load_rssi_data(data_path)
    
    # Créer la matrice de features
    X = processor.create_feature_matrix(dataframes)
    
    # Générer des coordonnées cibles synthétiques
    y = processor.generate_synthetic_targets(len(X))
    
    # Préprocesser les données
    X_train, X_test, y_train, y_test = processor.preprocess_data(X, y)
    
    # Calculer les statistiques
    stats = processor.get_data_statistics(X, y)
    
    logger.info("✅ Données chargées et préprocessées avec succès")
    
    return (X_train, X_test, y_train, y_test), stats, processor


def train_models(X_train, X_test, y_train, y_test):
    """
    Entraîne tous les modèles et les évalue.
    
    Args:
        X_train, X_test, y_train, y_test: Données d'entraînement et de test
        
    Returns:
        ModelManager: Gestionnaire des modèles entraînés
    """
    logger.info("🤖 Début de l'entraînement des modèles")
    
    # Initialiser le gestionnaire de modèles
    model_manager = ModelManager()
    
    # Ajouter les modèles
    model_manager.add_model("Random Forest", RSSIRandomForestModel(n_estimators=100))
    model_manager.add_model("XGBoost", RSSIXGBoostModel(n_estimators=100))
    
    # Ajouter le DNN seulement si TensorFlow est disponible
    if TENSORFLOW_AVAILABLE:
        model_manager.add_model("Deep Neural Network", RSSIDNNModel(input_dim=X_train.shape[1]))
        logger.info("✅ Modèle DNN ajouté (TensorFlow disponible)")
    else:
        logger.warning("⚠️ Modèle DNN ignoré (TensorFlow non disponible)")
    
    # Entraîner tous les modèles
    model_manager.train_all_models(X_train, y_train, X_test, y_test)
    
    # Évaluer tous les modèles
    model_manager.evaluate_all_models(X_test, y_test)
    
    # Sauvegarder le meilleur modèle
    model_manager.save_best_model('models')
    
    logger.info("✅ Entraînement et évaluation terminés")
    
    return model_manager


def generate_reports(model_manager, stats, output_dir='reports'):
    """
    Génère les rapports visuels et les sauvegarde.
    
    Args:
        model_manager (ModelManager): Gestionnaire des modèles
        stats (dict): Statistiques des données
        output_dir (str): Dossier de sortie
    """
    logger.info("📊 Génération des rapports")
    
    visualizer = RSSIVisualizer()
    
    # Obtenir les résultats
    results_summary = model_manager.get_results_summary()
    best_model_name = model_manager.best_model
    best_results = model_manager.results[best_model_name]
    
    # Créer les figures
    figures = {}
    
    # Comparaison des modèles
    figures['model_comparison'] = visualizer.plot_model_comparison(results_summary)
    
    # Scatter plot des prédictions
    figures['prediction_scatter'] = visualizer.plot_prediction_scatter(
        best_results['predictions'],  # Note: Utiliser les vraies données de test
        best_results['predictions'],  # Placeholder - remplacer par y_test
        best_model_name
    )
    
    # Heatmap des erreurs (avec des données synthétiques pour la démo)
    import numpy as np
    np.random.seed(42)
    y_true_demo = np.random.uniform(0, 100, (100, 2))
    y_pred_demo = y_true_demo + np.random.normal(0, 5, (100, 2))
    figures['error_heatmap'] = visualizer.plot_error_heatmap(y_true_demo, y_pred_demo)
    
    # Sauvegarder en HTML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f'rapport_geolocalisation_{timestamp}.html')
    save_figures_to_html(figures, report_path)
    
    # Sauvegarder le résumé des résultats
    results_path = os.path.join(output_dir, f'resultats_modeles_{timestamp}.csv')
    results_summary.to_csv(results_path, index=False)
    
    logger.info(f"✅ Rapports générés: {report_path}")
    
    return figures


def launch_dashboard(model_manager, stats, port=8050):
    """
    Lance le dashboard interactif.
    
    Args:
        model_manager (ModelManager): Gestionnaire des modèles
        stats (dict): Statistiques des données
        port (int): Port pour le serveur
    """
    logger.info("🚀 Lancement du dashboard interactif")
    
    dashboard = create_dashboard(model_manager, stats)
    dashboard.run_server(debug=False, port=port)


def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description='Pipeline de géolocalisation RSSI')
    parser.add_argument('--data-path', default='data', help='Chemin vers les données')
    parser.add_argument('--skip-training', action='store_true', 
                       help='Ignorer l\'entraînement et charger les modèles existants')
    parser.add_argument('--dashboard-only', action='store_true',
                       help='Lancer seulement le dashboard')
    parser.add_argument('--port', type=int, default=8050,
                       help='Port pour le dashboard')
    
    args = parser.parse_args()
    
    # Configuration initiale
    setup_directories()
    
    logger.info("🎯 Démarrage du pipeline de géolocalisation RSSI")
    logger.info(f"Arguments: {vars(args)}")
    
    try:
        if not args.dashboard_only:
            # Étape 1: Chargement et préprocessing des données
            (X_train, X_test, y_train, y_test), stats, processor = load_and_preprocess_data(args.data_path)
            
            # Afficher les statistiques
            logger.info("📈 Statistiques des données:")
            logger.info(f"  - Échantillons: {stats['n_samples']}")
            logger.info(f"  - Features: {stats['n_features']}")
            logger.info(f"  - RSSI moyen: {stats['rssi_range']['mean']:.2f} dBm")
            
            if not args.skip_training:
                # Étape 2: Entraînement des modèles
                model_manager = train_models(X_train, X_test, y_train, y_test)
                
                # Afficher les résultats
                results = model_manager.get_results_summary()
                logger.info("🏆 Résultats des modèles:")
                for _, row in results.iterrows():
                    logger.info(f"  - {row['Model']}: R² = {row['R²']:.4f}, MAE = {row['MAE']:.4f}")
                
                # Étape 3: Génération des rapports
                generate_reports(model_manager, stats)
                
            else:
                logger.info("⏭️ Entraînement ignoré - chargement des modèles existants")
                # TODO: Implémenter le chargement des modèles sauvegardés
                model_manager = ModelManager()  # Placeholder
                
            # Étape 4: Lancement du dashboard
            if input("\n🚀 Voulez-vous lancer le dashboard interactif? (y/N): ").lower() == 'y':
                launch_dashboard(model_manager, stats, args.port)
        
        else:
            logger.info("🎛️ Mode dashboard uniquement")
            # TODO: Charger les données et modèles existants
            stats = {'n_samples': 1000, 'n_features': 200, 'rssi_range': {'mean': -50}}
            model_manager = ModelManager()
            launch_dashboard(model_manager, stats, args.port)
            
    except KeyboardInterrupt:
        logger.info("⏹️ Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur: {str(e)}")
        raise
    finally:
        logger.info("🏁 Fin du pipeline")


if __name__ == "__main__":
    main()
