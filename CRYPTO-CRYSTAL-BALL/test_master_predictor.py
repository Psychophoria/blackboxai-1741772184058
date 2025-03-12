"""Test master predictor functionality"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.master_predictor import MasterPredictor
from src.data.data_acquisition import DataAcquisition
from datetime import datetime, timedelta

def test_master_predictor():
    """Test master predictor functionality"""
    print("Testing Master Predictor...")
    
    # Initialize components
    da = DataAcquisition()
    mp = MasterPredictor()
    
    # Test parameters
    symbol = "BTCUSDT"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Get 1 month of data
    
    try:
        # Get historical data
        print(f"\nGetting historical data for {symbol}...")
        data = da.get_historical_data(
            symbol,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        print("Data shape:", data.shape)
        
        # Test model training
        print("\nTesting model training...")
        enabled_models = {
            "LSTM": True,
            "CatBoost": True,
            "LightGBM": True,
            "Prophet": True,
            "RandomForest": True,
            "XGBoost": True,
            "MASTER": True
        }
        
        mp.train_models(data, enabled_models)
        print("Models trained successfully")
        
        # Test predictions
        print("\nTesting predictions...")
        forecast_length = {
            "hours": 24,
            "days": 7
        }
        
        master_prediction, individual_predictions = mp.predict(
            data,
            forecast_length,
            enabled_models
        )
        
        print("\nMaster Prediction shape:", master_prediction.shape)
        print("Master Prediction first few rows:")
        print(master_prediction.head())
        
        print("\nIndividual Predictions:")
        for model_name, pred in individual_predictions.items():
            print(f"\n{model_name} Prediction shape:", pred.shape)
            print(f"{model_name} first few rows:")
            print(pred.head())
        
        # Test model saving/loading
        print("\nTesting model saving and loading...")
        mp.save_models("models")
        print("Models saved successfully")
        
        mp.load_models("models")
        print("Models loaded successfully")
        
        print("\nMaster predictor tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        raise

if __name__ == "__main__":
    test_master_predictor()
