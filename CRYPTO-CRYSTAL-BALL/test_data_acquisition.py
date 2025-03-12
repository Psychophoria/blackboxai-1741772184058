"""Test data acquisition functionality"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.data_acquisition import DataAcquisition
from datetime import datetime, timedelta

def test_data_acquisition():
    """Test data acquisition from multiple sources"""
    print("Testing Data Acquisition...")
    
    # Initialize data acquisition
    da = DataAcquisition()
    
    # Test parameters
    symbol = "BTCUSDT"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)  # Get 1 week of data
    
    try:
        # Test historical data acquisition
        print(f"\nTesting historical data acquisition for {symbol}...")
        data = da.get_historical_data(
            symbol,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        print("Data shape:", data.shape)
        print("Columns:", data.columns.tolist())
        print("First few rows:")
        print(data.head())
        
        # Test live data streaming
        print("\nTesting live data streaming...")
        def callback(data, source):
            print(f"Received data from {source}:", data)
        
        print("Starting live data stream...")
        da.start_live_data_stream(symbol, callback)
        
        # Wait for some data
        print("Waiting for live data (5 seconds)...")
        import time
        time.sleep(5)
        
        # Stop streaming
        print("Stopping live data stream...")
        da.stop_live_data_stream(symbol)
        
        print("\nData acquisition tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        raise

if __name__ == "__main__":
    test_data_acquisition()
