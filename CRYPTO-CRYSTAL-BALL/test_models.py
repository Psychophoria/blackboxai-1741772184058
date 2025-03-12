"""Test individual model functionality"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.data_acquisition import DataAcquisition
from Lstm_model import LSTMPredictor
from Catboost_Regressor import CatBoostPredictor
from lgbm_model import LGBMRegressorModel
from Prophet_model import MProphet
from Random_Forest_Regressor import RandomForestPredictor
from Xgboost_model import XGBoost_Predictor
from datetime import datetime, timedelta

def test_model(model_name, model_class, data):
    """Test a specific model"""
    print(f"\nTesting {model_name}...")
    try:
        # Initialize model
        model = model_class()
        
        if model_name == "Prophet":
            # Prophet has different initialization
            model = model_class("configs/prophet_config.yaml")
        elif model_name == "XGBoost":
            # XGBoost has different initialization
            model = model_class("configs/xgboost_config.yaml")
        
        # Train and predict
        if model_name == "Prophet":
            model.data = data
            model.fit_predict()
            performance = model.cross_validate()
            print(f"{model_name} Performance:", performance)
        else:
            # For other models
            if hasattr(model, 'run'):
                result = model.run(data.index[0], data.index[-1])
                print(f"{model_name} Result:", result)
            else:
                # Fallback to individual steps
                if hasattr(model, 'prepare_data'):
                    X_train, X_test, y_train, y_test = model.prepare_data(data)
                else:
                    X_train, X_test, y_train, y_test = model.yfdown(data.index[0], data.index[-1])
                
                if hasattr(model, 'train_model'):
                    model.train_model(X_train, y_train, X_test, y_test)
                elif hasattr(model, 'fit'):
                    model.fit(X_train, y_train)
                
                predictions = model.predict(X_test)
                print(f"{model_name} Predictions shape:", predictions.shape)
        
        print(f"{model_name} tested successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing {model_name}: {str(e)}")
        return False

def test_all_models():
    """Test all prediction models"""
    print("Testing all models...")
    
    # Get test data
    da = DataAcquisition()
    symbol = "BTCUSDT"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        print(f"\nGetting test data for {symbol}...")
        data = da.get_historical_data(
            symbol,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        print("Data shape:", data.shape)
        
        # Test each model
        models = {
            "LSTM": LSTMPredictor,
            "CatBoost": CatBoostPredictor,
            "LightGBM": LGBMRegressorModel,
            "Prophet": MProphet,
            "RandomForest": RandomForestPredictor,
            "XGBoost": XGBoost_Predictor
        }
        
        results = {}
        for model_name, model_class in models.items():
            results[model_name] = test_model(model_name, model_class, data)
        
        # Print summary
        print("\nTest Results Summary:")
        for model_name, success in results.items():
            status = "PASSED" if success else "FAILED"
            print(f"{model_name}: {status}")
        
        # Check if all tests passed
        if all(results.values()):
            print("\nAll model tests completed successfully!")
        else:
            print("\nSome model tests failed!")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        raise

if __name__ == "__main__":
    test_all_models()
