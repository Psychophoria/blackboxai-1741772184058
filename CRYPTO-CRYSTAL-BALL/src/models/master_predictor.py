import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import joblib
import os

from ..utils.constants import MODEL_INFO
from ..Lstm_model import LSTMPredictor
from ..Catboost_Regressor import CatBoostPredictor
from ..lgbm_model import LGBMRegressorModel
from ..Prophet_model import MProphet
from ..Random_Forest_Regressor import RandomForestPredictor
from ..Xgboost_model import XGBoost_Predictor

class MasterPredictor:
    """
    Master prediction system that combines predictions from all models
    with dynamic weighting based on performance metrics
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.models = {}
        self.weights = {}
        self.performance_metrics = {}
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize all prediction models"""
        try:
            self.models = {
                'LSTM': LSTMPredictor(),
                'CatBoost': CatBoostPredictor(),
                'LightGBM': LGBMRegressorModel(),
                'Prophet': MProphet('configs/prophet_config.yaml'),
                'RandomForest': RandomForestPredictor(),
                'XGBoost': XGBoost_Predictor('configs/xgboost_config.yaml')
            }
            
            # Initialize equal weights
            total_models = len(self.models)
            self.weights = {model: 1.0/total_models for model in self.models.keys()}
            
        except Exception as e:
            self.logger.error(f"Error initializing models: {str(e)}")
            raise
    
    def train_models(self, data: pd.DataFrame, enabled_models: Dict[str, bool]) -> None:
        """
        Train all enabled models and update their weights based on performance
        """
        try:
            performance_scores = {}
            
            for model_name, enabled in enabled_models.items():
                if not enabled:
                    continue
                
                self.logger.info(f"Training {model_name} model...")
                
                if model_name == 'LSTM':
                    performance = self._train_lstm(data)
                elif model_name == 'CatBoost':
                    performance = self._train_catboost(data)
                elif model_name == 'LightGBM':
                    performance = self._train_lightgbm(data)
                elif model_name == 'Prophet':
                    performance = self._train_prophet(data)
                elif model_name == 'RandomForest':
                    performance = self._train_random_forest(data)
                elif model_name == 'XGBoost':
                    performance = self._train_xgboost(data)
                
                performance_scores[model_name] = performance
            
            # Update weights based on performance
            self._update_weights(performance_scores)
            
        except Exception as e:
            self.logger.error(f"Error training models: {str(e)}")
            raise
    
    def predict(self, data: pd.DataFrame, forecast_length: Dict[str, int],
                enabled_models: Dict[str, bool]) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
        Generate predictions from all enabled models and combine them
        """
        try:
            predictions = {}
            total_minutes = forecast_length['hours'] * 60 + forecast_length['days'] * 24 * 60
            
            for model_name, enabled in enabled_models.items():
                if not enabled:
                    continue
                
                self.logger.info(f"Generating predictions with {model_name}...")
                
                if model_name == 'LSTM':
                    pred = self._predict_lstm(data, total_minutes)
                elif model_name == 'CatBoost':
                    pred = self._predict_catboost(data, total_minutes)
                elif model_name == 'LightGBM':
                    pred = self._predict_lightgbm(data, total_minutes)
                elif model_name == 'Prophet':
                    pred = self._predict_prophet(data, total_minutes)
                elif model_name == 'RandomForest':
                    pred = self._predict_random_forest(data, total_minutes)
                elif model_name == 'XGBoost':
                    pred = self._predict_xgboost(data, total_minutes)
                
                predictions[model_name] = pred
            
            # Generate master prediction
            master_prediction = self._generate_master_prediction(predictions)
            
            return master_prediction, predictions
            
        except Exception as e:
            self.logger.error(f"Error generating predictions: {str(e)}")
            raise
    
    def _train_lstm(self, data: pd.DataFrame) -> float:
        """Train LSTM model and return performance metric"""
        model = self.models['LSTM']
        X_train, X_test, y_train, y_test = model.prepare_data(data)
        history = model.train_model(X_train, y_train, X_test, y_test)
        y_pred = model.predict(X_test)
        return model.evaluate_model(y_test, y_pred)
    
    def _train_catboost(self, data: pd.DataFrame) -> float:
        """Train CatBoost model and return performance metric"""
        model = self.models['CatBoost']
        X_train, X_test, y_train, y_test = model.yfdown(data.index[0], data.index[-1])
        best_params = model.search_catboost(X_train, y_train)
        pred = model.train_model(X_train, y_train, X_test, y_test, best_params)
        return model.evaluate_model(y_test, pred)
    
    def _train_lightgbm(self, data: pd.DataFrame) -> float:
        """Train LightGBM model and return performance metric"""
        model = self.models['LightGBM']
        X_train, X_test, y_train, y_test = model.yfdown(data.index[0], data.index[-1])
        grid_search, best_params = model.grid(X_train, y_train, X_test, y_test)
        trained_model = model.model(X_train, y_train, X_test, y_test, best_params)
        rmse = model.yhat(data.index[0], trained_model, X_test, y_test)
        return rmse
    
    def _train_prophet(self, data: pd.DataFrame) -> float:
        """Train Prophet model and return performance metric"""
        model = self.models['Prophet']
        model.data = data
        model.fit_predict()
        performance = model.cross_validate()
        return performance['rmse'].mean()
    
    def _train_random_forest(self, data: pd.DataFrame) -> float:
        """Train Random Forest model and return performance metric"""
        model = self.models['RandomForest']
        df = model.download_and_prepare_data(data.index[0], data.index[-1])
        X, y = model.prepare_features_and_target(df)
        X_test, y_test, predictions, mse, mae, r2 = model.train_and_evaluate_model(X, y)
        return np.sqrt(mse)
    
    def _train_xgboost(self, data: pd.DataFrame) -> float:
        """Train XGBoost model and return performance metric"""
        model = self.models['XGBoost']
        df = model.download_data()
        X_train, X_test, y_train, y_test = model.prepare_data(df)
        best_params = model.optimize_xgb(X_train, y_train)
        model.train_model(X_train, y_train, best_params)
        y_pred = model.predict(X_test)
        rmse, _, _ = model.evaluate(y_test, y_pred)
        return rmse
    
    def _predict_lstm(self, data: pd.DataFrame, total_minutes: int) -> pd.DataFrame:
        """Generate predictions using LSTM model"""
        model = self.models['LSTM']
        predictions = []
        current_data = data.copy()
        
        for _ in range(total_minutes):
            X = model.prepare_prediction_data(current_data)
            pred = model.predict(X)
            predictions.append(pred[-1][0])
            
            # Update data for next prediction
            new_row = current_data.iloc[-1].copy()
            new_row['Close'] = pred[-1][0]
            current_data = current_data.append(new_row)
        
        # Create prediction DataFrame
        dates = pd.date_range(start=data.index[-1], periods=total_minutes+1, freq='T')[1:]
        return pd.DataFrame(predictions, index=dates, columns=['Close'])
    
    def _predict_catboost(self, data: pd.DataFrame, total_minutes: int) -> pd.DataFrame:
        """Generate predictions using CatBoost model"""
        model = self.models['CatBoost']
        predictions = []
        current_data = data.copy()
        
        for _ in range(total_minutes):
            X = model.prepare_prediction_data(current_data)
            pred = model.predict(X)
            predictions.append(pred[-1])
            
            # Update data for next prediction
            new_row = current_data.iloc[-1].copy()
            new_row['Close'] = pred[-1]
            current_data = current_data.append(new_row)
        
        dates = pd.date_range(start=data.index[-1], periods=total_minutes+1, freq='T')[1:]
        return pd.DataFrame(predictions, index=dates, columns=['Close'])
    
    def _predict_lightgbm(self, data: pd.DataFrame, total_minutes: int) -> pd.DataFrame:
        """Generate predictions using LightGBM model"""
        model = self.models['LightGBM']
        predictions = []
        current_data = data.copy()
        
        for _ in range(total_minutes):
            X = model.prepare_prediction_data(current_data)
            pred = model.predict(X)
            predictions.append(pred[-1])
            
            new_row = current_data.iloc[-1].copy()
            new_row['Close'] = pred[-1]
            current_data = current_data.append(new_row)
        
        dates = pd.date_range(start=data.index[-1], periods=total_minutes+1, freq='T')[1:]
        return pd.DataFrame(predictions, index=dates, columns=['Close'])
    
    def _predict_prophet(self, data: pd.DataFrame, total_minutes: int) -> pd.DataFrame:
        """Generate predictions using Prophet model"""
        model = self.models['Prophet']
        future = model.model.make_future_dataframe(periods=total_minutes, freq='T')
        forecast = model.model.predict(future)
        return forecast.set_index('ds')['yhat'].tail(total_minutes)
    
    def _predict_random_forest(self, data: pd.DataFrame, total_minutes: int) -> pd.DataFrame:
        """Generate predictions using Random Forest model"""
        model = self.models['RandomForest']
        predictions = []
        current_data = data.copy()
        
        for _ in range(total_minutes):
            X = model.prepare_prediction_data(current_data)
            pred = model.predict(X)
            predictions.append(pred[-1])
            
            new_row = current_data.iloc[-1].copy()
            new_row['Close'] = pred[-1]
            current_data = current_data.append(new_row)
        
        dates = pd.date_range(start=data.index[-1], periods=total_minutes+1, freq='T')[1:]
        return pd.DataFrame(predictions, index=dates, columns=['Close'])
    
    def _predict_xgboost(self, data: pd.DataFrame, total_minutes: int) -> pd.DataFrame:
        """Generate predictions using XGBoost model"""
        model = self.models['XGBoost']
        predictions = []
        current_data = data.copy()
        
        for _ in range(total_minutes):
            X = model.prepare_prediction_data(current_data)
            pred = model.predict(X)
            predictions.append(pred[-1])
            
            new_row = current_data.iloc[-1].copy()
            new_row['Close'] = pred[-1]
            current_data = current_data.append(new_row)
        
        dates = pd.date_range(start=data.index[-1], periods=total_minutes+1, freq='T')[1:]
        return pd.DataFrame(predictions, index=dates, columns=['Close'])
    
    def _update_weights(self, performance_scores: Dict[str, float]) -> None:
        """Update model weights based on performance metrics"""
        # Convert RMSE to accuracy score (higher is better)
        accuracy_scores = {
            model: 1.0 / (1.0 + score)
            for model, score in performance_scores.items()
        }
        
        # Calculate total accuracy
        total_accuracy = sum(accuracy_scores.values())
        
        # Update weights based on relative accuracy
        self.weights = {
            model: score / total_accuracy
            for model, score in accuracy_scores.items()
        }
        
        self.logger.info(f"Updated model weights: {self.weights}")
    
    def _generate_master_prediction(self, predictions: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Generate master prediction by combining individual predictions"""
        # Align all predictions to the same index
        aligned_predictions = []
        for model_name, pred in predictions.items():
            weighted_pred = pred['Close'] * self.weights[model_name]
            aligned_predictions.append(weighted_pred)
        
        # Combine predictions using weighted average
        master_prediction = sum(aligned_predictions)
        
        return pd.DataFrame(master_prediction, columns=['Close'])
    
    def save_models(self, directory: str) -> None:
        """Save all trained models"""
        os.makedirs(directory, exist_ok=True)
        
        for model_name, model in self.models.items():
            model_path = os.path.join(directory, f"{model_name.lower()}_model.joblib")
            joblib.dump(model, model_path)
        
        # Save weights
        weights_path = os.path.join(directory, "model_weights.joblib")
        joblib.dump(self.weights, weights_path)
    
    def load_models(self, directory: str) -> None:
        """Load all saved models"""
        for model_name in self.models.keys():
            model_path = os.path.join(directory, f"{model_name.lower()}_model.joblib")
            self.models[model_name] = joblib.load(model_path)
        
        # Load weights
        weights_path = os.path.join(directory, "model_weights.joblib")
        self.weights = joblib.load(weights_path)
