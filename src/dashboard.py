"""
Dashboard interactif pour la géolocalisation RSSI.

Ce module crée une interface web interactive permettant de visualiser
les résultats des modèles et de faire des prédictions en temps réel.
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import joblib
import os
from typing import Dict, Any
import logging

from .models import ModelManager
from .visualization import RSSIVisualizer

logger = logging.getLogger(__name__)


class RSSIDashboard:
    """Classe principale pour le dashboard interactif."""
    
    def __init__(self, model_manager: ModelManager, data_stats: Dict[str, Any]):
        self.app = dash.Dash(__name__)
        self.model_manager = model_manager
        self.data_stats = data_stats
        self.visualizer = RSSIVisualizer()
        
        self._setup_layout()
        self._setup_callbacks()
        
    def _setup_layout(self):
        """Configure la mise en page du dashboard."""
        
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("🎯 Dashboard de Géolocalisation RSSI", 
                       style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
                html.Hr()
            ]),
            
            # Statistiques générales
            html.Div([
                html.H2("📊 Statistiques des Données", style={'color': '#34495e'}),
                html.Div([
                    html.Div([
                        html.H4(f"{self.data_stats['n_samples']}", 
                               style={'margin': 0, 'color': '#e74c3c'}),
                        html.P("Échantillons", style={'margin': 0})
                    ], className='stat-box', style={'textAlign': 'center', 'padding': 20, 
                                                   'backgroundColor': '#ecf0f1', 'margin': 10, 
                                                   'borderRadius': 10, 'flex': 1}),
                    
                    html.Div([
                        html.H4(f"{self.data_stats['n_features']}", 
                               style={'margin': 0, 'color': '#3498db'}),
                        html.P("Features", style={'margin': 0})
                    ], className='stat-box', style={'textAlign': 'center', 'padding': 20, 
                                                   'backgroundColor': '#ecf0f1', 'margin': 10, 
                                                   'borderRadius': 10, 'flex': 1}),
                    
                    html.Div([
                        html.H4(f"{self.data_stats['rssi_range']['mean']:.1f} dBm", 
                               style={'margin': 0, 'color': '#2ecc71'}),
                        html.P("RSSI Moyen", style={'margin': 0})
                    ], className='stat-box', style={'textAlign': 'center', 'padding': 20, 
                                                   'backgroundColor': '#ecf0f1', 'margin': 10, 
                                                   'borderRadius': 10, 'flex': 1}),
                    
                ], style={'display': 'flex', 'justifyContent': 'space-around'}),
                html.Hr()
            ]),
            
            # Comparaison des modèles
            html.Div([
                html.H2("🏆 Comparaison des Modèles", style={'color': '#34495e'}),
                dcc.Graph(id='model-comparison-graph'),
                html.Hr()
            ]),
            
            # Prédiction interactive
            html.Div([
                html.H2("🔮 Prédiction Interactive", style={'color': '#34495e'}),
                
                html.Div([
                    # Panel de saisie
                    html.Div([
                        html.H4("Saisie des valeurs RSSI", style={'color': '#7f8c8d'}),
                        html.Div([
                            html.Label("Capteur 1 (dBm):", style={'fontWeight': 'bold'}),
                            dcc.Input(
                                id='rssi-1',
                                type='number',
                                value=-50,
                                min=-100,
                                max=-20,
                                step=0.1,
                                style={'width': '100%', 'padding': 5, 'margin': '5px 0'}
                            )
                        ], style={'margin': '10px 0'}),
                        
                        html.Div([
                            html.Label("Capteur 2 (dBm):", style={'fontWeight': 'bold'}),
                            dcc.Input(
                                id='rssi-2',
                                type='number',
                                value=-45,
                                min=-100,
                                max=-20,
                                step=0.1,
                                style={'width': '100%', 'padding': 5, 'margin': '5px 0'}
                            )
                        ], style={'margin': '10px 0'}),
                        
                        html.Div([
                            html.Label("Capteur 3 (dBm):", style={'fontWeight': 'bold'}),
                            dcc.Input(
                                id='rssi-3',
                                type='number',
                                value=-55,
                                min=-100,
                                max=-20,
                                step=0.1,
                                style={'width': '100%', 'padding': 5, 'margin': '5px 0'}
                            )
                        ], style={'margin': '10px 0'}),
                        
                        html.Div([
                            html.Label("Capteur 4 (dBm):", style={'fontWeight': 'bold'}),
                            dcc.Input(
                                id='rssi-4',
                                type='number',
                                value=-48,
                                min=-100,
                                max=-20,
                                step=0.1,
                                style={'width': '100%', 'padding': 5, 'margin': '5px 0'}
                            )
                        ], style={'margin': '10px 0'}),
                        
                        html.Button(
                            "🎯 Prédire Position",
                            id='predict-button',
                            n_clicks=0,
                            style={
                                'width': '100%',
                                'padding': 15,
                                'backgroundColor': '#3498db',
                                'color': 'white',
                                'border': 'none',
                                'borderRadius': 5,
                                'fontSize': 16,
                                'fontWeight': 'bold',
                                'cursor': 'pointer',
                                'margin': '20px 0'
                            }
                        )
                    ], style={
                        'width': '30%',
                        'padding': 20,
                        'backgroundColor': '#f8f9fa',
                        'borderRadius': 10,
                        'margin': 10
                    }),
                    
                    # Résultats de prédiction
                    html.Div([
                        html.H4("Résultats de Prédiction", style={'color': '#7f8c8d'}),
                        html.Div(id='prediction-results', style={'fontSize': 16}),
                        dcc.Graph(id='prediction-map')
                    ], style={
                        'width': '65%',
                        'padding': 20,
                        'backgroundColor': '#f8f9fa',
                        'borderRadius': 10,
                        'margin': 10
                    })
                    
                ], style={'display': 'flex', 'justifyContent': 'space-between'}),
                html.Hr()
            ]),
            
            # Analyse des erreurs
            html.Div([
                html.H2("📈 Analyse des Erreurs", style={'color': '#34495e'}),
                dcc.Graph(id='error-analysis-graph'),
                html.Hr()
            ]),
            
            # Footer
            html.Div([
                html.P("🚀 Dashboard créé avec Dash & Plotly | Géolocalisation RSSI",
                      style={'textAlign': 'center', 'color': '#7f8c8d', 'marginTop': 30})
            ])
            
        ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': 20})
    
    def _setup_callbacks(self):
        """Configure les callbacks interactifs."""
        
        @self.app.callback(
            Output('model-comparison-graph', 'figure'),
            Input('model-comparison-graph', 'id')
        )
        def update_model_comparison(_):
            """Met à jour le graphique de comparaison des modèles."""
            results_df = self.model_manager.get_results_summary()
            return self.visualizer.plot_model_comparison(results_df)
        
        @self.app.callback(
            [Output('prediction-results', 'children'),
             Output('prediction-map', 'figure')],
            [Input('predict-button', 'n_clicks')],
            [State('rssi-1', 'value'),
             State('rssi-2', 'value'),
             State('rssi-3', 'value'),
             State('rssi-4', 'value')]
        )
        def make_prediction(n_clicks, rssi1, rssi2, rssi3, rssi4):
            """Effectue une prédiction basée sur les valeurs RSSI saisies."""
            
            if n_clicks == 0:
                return "Cliquez sur 'Prédire Position' pour obtenir une prédiction.", go.Figure()
            
            # Préparer les données d'entrée
            rssi_values = [rssi1, rssi2, rssi3, rssi4]
            
            # Créer un vecteur de features (répéter les valeurs RSSI pour correspondre au nombre de features)
            n_features = self.data_stats['n_features']
            input_features = np.tile(rssi_values, n_features // 4 + 1)[:n_features].reshape(1, -1)
            
            # Obtenir le meilleur modèle
            best_model_name = self.model_manager.best_model
            best_model = self.model_manager.results[best_model_name]['model']
            
            # Faire la prédiction
            prediction = best_model.predict(input_features)[0]
            
            # Préparer les résultats
            results_div = html.Div([
                html.H5(f"Modèle utilisé: {best_model_name}", 
                       style={'color': '#2c3e50', 'marginBottom': 10}),
                html.P([
                    html.Strong("Position prédite: "),
                    f"X = {prediction[0]:.2f}, Y = {prediction[1]:.2f}"
                ], style={'fontSize': 14, 'margin': '5px 0'}),
                html.P([
                    html.Strong("Valeurs RSSI utilisées: "),
                    f"[{rssi1}, {rssi2}, {rssi3}, {rssi4}] dBm"
                ], style={'fontSize': 12, 'color': '#7f8c8d', 'margin': '5px 0'})
            ])
            
            # Créer la carte de position
            fig = go.Figure()
            
            # Ajouter la position prédite
            fig.add_trace(go.Scatter(
                x=[prediction[0]],
                y=[prediction[1]],
                mode='markers',
                marker=dict(
                    size=20,
                    color='red',
                    symbol='star',
                    line=dict(width=2, color='darkred')
                ),
                name='Position prédite',
                text=f'Prédiction: ({prediction[0]:.1f}, {prediction[1]:.1f})',
                hoverinfo='text'
            ))
            
            # Ajouter les positions des capteurs (hypothétiques)
            sensor_positions = [(0, 0), (100, 0), (100, 100), (0, 100)]
            sensor_names = ['Capteur 1', 'Capteur 2', 'Capteur 3', 'Capteur 4']
            
            for i, (x, y) in enumerate(sensor_positions):
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers',
                    marker=dict(
                        size=15,
                        color='blue',
                        symbol='square'
                    ),
                    name=sensor_names[i],
                    text=f'{sensor_names[i]}: {rssi_values[i]} dBm',
                    hoverinfo='text'
                ))
            
            fig.update_layout(
                title="Carte de Position Prédite",
                xaxis_title="Coordonnée X",
                yaxis_title="Coordonnée Y",
                showlegend=True,
                height=400,
                plot_bgcolor='lightgray'
            )
            
            return results_div, fig
        
        @self.app.callback(
            Output('error-analysis-graph', 'figure'),
            Input('error-analysis-graph', 'id')
        )
        def update_error_analysis(_):
            """Met à jour l'analyse des erreurs."""
            
            # Obtenir les résultats du meilleur modèle
            best_model_name = self.model_manager.best_model
            if best_model_name and best_model_name in self.model_manager.results:
                result = self.model_manager.results[best_model_name]
                
                # Créer un graphique factice pour la démonstration
                # En réalité, vous utiliseriez les vraies données de test
                np.random.seed(42)
                n_points = 100
                y_true = np.random.uniform(0, 100, (n_points, 2))
                y_pred = y_true + np.random.normal(0, 5, (n_points, 2))
                
                return self.visualizer.plot_error_heatmap(y_true, y_pred)
            
            return go.Figure()
    
    def run_server(self, debug: bool = True, port: int = 8050):
        """Lance le serveur du dashboard."""
        logger.info(f"Lancement du dashboard sur http://127.0.0.1:{port}")
        try:
          self.app.run(debug=debug, port=port)
        except AttributeError:
          self.app.run_server(debug=debug, port=port)


def create_dashboard(model_manager: ModelManager, data_stats: Dict[str, Any]) -> RSSIDashboard:
    """
    Crée et configure le dashboard.
    
    Args:
        model_manager (ModelManager): Gestionnaire des modèles entraînés
        data_stats (Dict[str, Any]): Statistiques des données
        
    Returns:
        RSSIDashboard: Instance du dashboard configuré
    """
    return RSSIDashboard(model_manager, data_stats)
