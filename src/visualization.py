"""
Module de visualisation pour l'analyse des données RSSI et des résultats de géolocalisation.

Ce module contient toutes les fonctions nécessaires pour créer des visualisations
interactives et des rapports visuels pour le projet de géolocalisation.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)

# Configuration du style matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class RSSIVisualizer:
    """Classe pour créer des visualisations des données RSSI et des résultats."""
    
    def __init__(self):
        self.colors = px.colors.qualitative.Set3
        
    def plot_rssi_distribution(self, dataframes: Dict[str, pd.DataFrame]) -> go.Figure:
        """
        Crée un graphique de distribution des valeurs RSSI par capteur.
        
        Args:
            dataframes (Dict[str, pd.DataFrame]): Données RSSI par capteur
            
        Returns:
            go.Figure: Figure Plotly interactive
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[f'Capteur {i}' for i in range(4)],
            vertical_spacing=0.1
        )
        
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        
        for i, (key, df) in enumerate(dataframes.items()):
            # Aplatir les données et supprimer les NaN
            values = df.values.flatten()
            values = values[~np.isnan(values)]
            
            row, col = positions[i]
            
            fig.add_trace(
                go.Histogram(
                    x=values,
                    name=f'Capteur {i}',
                    nbinsx=50,
                    opacity=0.7
                ),
                row=row, col=col
            )
            
        fig.update_layout(
            title="Distribution des valeurs RSSI par capteur",
            height=600,
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Valeur RSSI (dBm)")
        fig.update_yaxes(title_text="Fréquence")
        
        return fig
    
    def plot_rssi_heatmap(self, df: pd.DataFrame, title: str = "Heatmap RSSI") -> go.Figure:
        """
        Crée une heatmap des valeurs RSSI.
        
        Args:
            df (pd.DataFrame): DataFrame des valeurs RSSI
            title (str): Titre du graphique
            
        Returns:
            go.Figure: Figure Plotly interactive
        """
        # Calculer la corrélation entre les colonnes
        corr_matrix = df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu',
            zmid=0
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Features",
            yaxis_title="Features"
        )
        
        return fig
    
    def plot_model_comparison(self, results_df: pd.DataFrame) -> go.Figure:
        """
        Crée un graphique comparatif des performances des modèles.
        
        Args:
            results_df (pd.DataFrame): DataFrame avec les résultats des modèles
            
        Returns:
            go.Figure: Figure Plotly interactive
        """
        metrics = ['R²', 'MAE', 'MSE', 'RMSE']
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=metrics,
            vertical_spacing=0.15
        )
        
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        for i, metric in enumerate(metrics):
            if metric in results_df.columns:
                row, col = positions[i]
                
                fig.add_trace(
                    go.Bar(
                        x=results_df['Model'],
                        y=results_df[metric],
                        name=metric,
                        marker_color=colors[i],
                        showlegend=False
                    ),
                    row=row, col=col
                )
                
        fig.update_layout(
            title="Comparaison des performances des modèles",
            height=600
        )
        
        return fig
    
    def plot_prediction_scatter(self, y_true: np.ndarray, y_pred: np.ndarray, 
                               model_name: str) -> go.Figure:
        """
        Crée un scatter plot des prédictions vs valeurs réelles.
        
        Args:
            y_true (np.ndarray): Valeurs réelles
            y_pred (np.ndarray): Valeurs prédites
            model_name (str): Nom du modèle
            
        Returns:
            go.Figure: Figure Plotly interactive
        """
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['Coordonnée X', 'Coordonnée Y'],
            horizontal_spacing=0.1
        )
        
        # Scatter plot pour X
        fig.add_trace(
            go.Scatter(
                x=y_true[:, 0],
                y=y_pred[:, 0],
                mode='markers',
                name='X',
                marker=dict(color='blue', opacity=0.6)
            ),
            row=1, col=1
        )
        
        # Scatter plot pour Y
        fig.add_trace(
            go.Scatter(
                x=y_true[:, 1],
                y=y_pred[:, 1],
                mode='markers',
                name='Y',
                marker=dict(color='red', opacity=0.6)
            ),
            row=1, col=2
        )
        
        # Ligne de référence parfaite
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        
        for col in [1, 2]:
            fig.add_trace(
                go.Scatter(
                    x=[min_val, max_val],
                    y=[min_val, max_val],
                    mode='lines',
                    name='Prédiction parfaite',
                    line=dict(color='black', dash='dash'),
                    showlegend=(col == 1)
                ),
                row=1, col=col
            )
        
        fig.update_layout(
            title=f"Prédictions vs Valeurs réelles - {model_name}",
            height=400
        )
        
        fig.update_xaxes(title_text="Valeurs réelles")
        fig.update_yaxes(title_text="Valeurs prédites")
        
        return fig
    
    def plot_error_heatmap(self, y_true: np.ndarray, y_pred: np.ndarray, 
                          grid_size: int = 20) -> go.Figure:
        """
        Crée une heatmap des erreurs de géolocalisation.
        
        Args:
            y_true (np.ndarray): Positions réelles
            y_pred (np.ndarray): Positions prédites
            grid_size (int): Taille de la grille pour la heatmap
            
        Returns:
            go.Figure: Figure Plotly interactive
        """
        # Calculer les erreurs euclidiennes
        errors = np.sqrt((y_true[:, 0] - y_pred[:, 0])**2 + 
                        (y_true[:, 1] - y_pred[:, 1])**2)
        
        # Créer une grille pour la heatmap
        x_min, x_max = y_true[:, 0].min(), y_true[:, 0].max()
        y_min, y_max = y_true[:, 1].min(), y_true[:, 1].max()
        
        x_grid = np.linspace(x_min, x_max, grid_size)
        y_grid = np.linspace(y_min, y_max, grid_size)
        
        # Interpoler les erreurs sur la grille
        from scipy.interpolate import griddata
        
        xi, yi = np.meshgrid(x_grid, y_grid)
        zi = griddata((y_true[:, 0], y_true[:, 1]), errors, 
                     (xi, yi), method='linear', fill_value=0)
        
        fig = go.Figure(data=go.Heatmap(
            z=zi,
            x=x_grid,
            y=y_grid,
            colorscale='Reds',
            colorbar=dict(title="Erreur (unités)")
        ))
        
        # Ajouter les points de données
        fig.add_trace(go.Scatter(
            x=y_true[:, 0],
            y=y_true[:, 1],
            mode='markers',
            marker=dict(color='blue', size=4, opacity=0.6),
            name='Positions réelles'
        ))
        
        fig.update_layout(
            title="Carte de chaleur des erreurs de géolocalisation",
            xaxis_title="Coordonnée X",
            yaxis_title="Coordonnée Y"
        )
        
        return fig
    
    def plot_feature_importance(self, importance_scores: np.ndarray, 
                               feature_names: List[str] = None) -> go.Figure:
        """
        Crée un graphique d'importance des features.
        
        Args:
            importance_scores (np.ndarray): Scores d'importance
            feature_names (List[str]): Noms des features
            
        Returns:
            go.Figure: Figure Plotly interactive
        """
        if feature_names is None:
            feature_names = [f'Feature_{i}' for i in range(len(importance_scores))]
            
        # Trier par importance décroissante
        sorted_indices = np.argsort(importance_scores)[::-1]
        top_20_indices = sorted_indices[:20]  # Top 20 features
        
        fig = go.Figure(data=go.Bar(
            x=importance_scores[top_20_indices],
            y=[feature_names[i] for i in top_20_indices],
            orientation='h',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title="Importance des 20 principales features",
            xaxis_title="Score d'importance",
            yaxis_title="Features",
            height=600
        )
        
        return fig
    
    def create_dashboard_layout(self, results: Dict[str, Any]) -> Dict[str, go.Figure]:
        """
        Crée un ensemble de graphiques pour le dashboard.
        
        Args:
            results (Dict[str, Any]): Résultats des modèles
            
        Returns:
            Dict[str, go.Figure]: Dictionnaire des figures
        """
        figures = {}
        
        # Graphique de comparaison des modèles
        if 'results_summary' in results:
            figures['model_comparison'] = self.plot_model_comparison(
                results['results_summary']
            )
        
        # Graphiques de prédiction pour le meilleur modèle
        if 'best_model_results' in results:
            best_results = results['best_model_results']
            figures['prediction_scatter'] = self.plot_prediction_scatter(
                best_results['y_true'],
                best_results['y_pred'],
                best_results['model_name']
            )
            
            figures['error_heatmap'] = self.plot_error_heatmap(
                best_results['y_true'],
                best_results['y_pred']
            )
        
        return figures


def save_figures_to_html(figures: Dict[str, go.Figure], output_path: str) -> None:
    """
    Sauvegarde toutes les figures dans un fichier HTML.
    
    Args:
        figures (Dict[str, go.Figure]): Dictionnaire des figures
        output_path (str): Chemin de sortie du fichier HTML
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rapport de Géolocalisation RSSI</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .figure-container { margin: 30px 0; }
            h1, h2 { color: #333; }
        </style>
    </head>
    <body>
        <h1>Rapport d'Analyse - Géolocalisation RSSI</h1>
    """
    
    for title, fig in figures.items():
        html_content += f"""
        <div class="figure-container">
            <h2>{title.replace('_', ' ').title()}</h2>
            <div id="{title}"></div>
        </div>
        """
    
    html_content += """
    <script>
    """
    
    for title, fig in figures.items():
        fig_json = fig.to_json()
        html_content += f"""
        Plotly.newPlot('{title}', {fig_json});
        """
    
    html_content += """
    </script>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    logger.info(f"Rapport HTML sauvegardé: {output_path}")
