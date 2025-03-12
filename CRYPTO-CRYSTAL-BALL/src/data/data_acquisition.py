import yfinance as yf
import ccxt
import cryptocompare
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import logging
import time
from typing import Dict, List, Optional, Tuple
import websocket
import json

class DataAcquisition:
    """
    Class to handle cryptocurrency data acquisition from multiple sources
    with built-in redundancy and minute-by-minute granularity
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sources = {
            'yfinance': self._get_yfinance_data,
            'ccxt_binance': self._get_ccxt_binance_data,
            'cryptocompare': self._get_cryptocompare_data,
            'binance_api': self._get_binance_api_data,
            'coinbase_api': self._get_coinbase_api_data
        }
        
        # Initialize exchanges
        self.binance = ccxt.binance()
        self.coinbase = ccxt.coinbase()
        
        # WebSocket connections for live data
        self.ws_connections = {}
        
    def get_historical_data(self, symbol: str, start_date: str, end_date: str,
                          months: int = 1, years: int = 1) -> pd.DataFrame:
        """
        Get historical minute-by-minute data using multiple sources with redundancy
        """
        data = None
        errors = []
        
        for source_name, source_func in self.sources.items():
            try:
                self.logger.info(f"Attempting to fetch data from {source_name}")
                data = source_func(symbol, start_date, end_date)
                if data is not None and not data.empty:
                    self.logger.info(f"Successfully retrieved data from {source_name}")
                    break
            except Exception as e:
                error_msg = f"Error fetching data from {source_name}: {str(e)}"
                self.logger.error(error_msg)
                errors.append(error_msg)
                continue
        
        if data is None or data.empty:
            raise Exception(f"Failed to fetch data from all sources. Errors: {errors}")
        
        return self._process_data(data)
    
    def start_live_data_stream(self, symbol: str, callback) -> None:
        """Start streaming live minute-by-minute data"""
        # Initialize WebSocket connections for multiple sources
        self._setup_binance_websocket(symbol, callback)
        self._setup_coinbase_websocket(symbol, callback)
    
    def stop_live_data_stream(self, symbol: str) -> None:
        """Stop streaming live data"""
        for ws in self.ws_connections.get(symbol, []):
            ws.close()
        self.ws_connections[symbol] = []
    
    def _get_yfinance_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get data from Yahoo Finance"""
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start_date, end=end_date, interval='1m')
        return data
    
    def _get_ccxt_binance_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get data from Binance using CCXT"""
        timeframe = '1m'
        since = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
        end = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp() * 1000)
        
        ohlcv = self.binance.fetch_ohlcv(symbol, timeframe, since, limit=1000)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    
    def _get_cryptocompare_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get data from CryptoCompare"""
        # Extract the base currency from the symbol (e.g., 'BTC' from 'BTCUSDT')
        base_currency = symbol.replace('USDT', '')
        
        limit = 2000  # Maximum limit per request
        data = cryptocompare.get_historical_price_minute(
            base_currency,
            'USDT',
            limit=limit,
            exchange='Binance'
        )
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('timestamp', inplace=True)
        return df
    
    def _get_binance_api_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get data from Binance public API"""
        base_url = "https://api.binance.com/api/v3/klines"
        interval = "1m"
        
        start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
        end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp() * 1000)
        
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_ts,
            "endTime": end_ts,
            "limit": 1000
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                       'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                                       'taker_buy_quote', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    
    def _get_coinbase_api_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get data from Coinbase public API"""
        base_url = "https://api.pro.coinbase.com"
        product_id = symbol.replace('USDT', '-USD')  # Convert format (e.g., 'BTC-USD')
        
        # Coinbase Pro API endpoint for historical data
        endpoint = f"/products/{product_id}/candles"
        
        start_ts = datetime.strptime(start_date, '%Y-%m-%d').isoformat()
        end_ts = datetime.strptime(end_date, '%Y-%m-%d').isoformat()
        
        params = {
            "start": start_ts,
            "end": end_ts,
            "granularity": 60  # 60 seconds = 1 minute
        }
        
        response = requests.get(f"{base_url}{endpoint}", params=params)
        data = response.json()
        
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df.set_index('timestamp', inplace=True)
        return df
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process and clean the data"""
        # Ensure consistent column names
        df = df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })
        
        # Add technical indicators
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['RSI'] = self._calculate_rsi(df['close'])
        df['MACD'], df['Signal'] = self._calculate_macd(df['close'])
        df['BB_upper'], df['BB_lower'] = self._calculate_bollinger_bands(df['close'])
        
        # Add time-based features
        df['hour'] = df.index.hour
        df['minute'] = df.index.minute
        df['day_of_week'] = df.index.dayofweek
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def _calculate_macd(self, prices: pd.Series,
                       fast_period: int = 12,
                       slow_period: int = 26,
                       signal_period: int = 9) -> Tuple[pd.Series, pd.Series]:
        """Calculate MACD and Signal line"""
        fast_ema = prices.ewm(span=fast_period, adjust=False).mean()
        slow_ema = prices.ewm(span=slow_period, adjust=False).mean()
        macd = fast_ema - slow_ema
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        return macd, signal
    
    def _calculate_bollinger_bands(self, prices: pd.Series,
                                 period: int = 20,
                                 num_std: int = 2) -> Tuple[pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        return upper_band, lower_band
    
    def _setup_binance_websocket(self, symbol: str, callback) -> None:
        """Setup WebSocket connection to Binance"""
        def on_message(ws, message):
            data = json.loads(message)
            callback(data, 'binance')
        
        def on_error(ws, error):
            self.logger.error(f"Binance WebSocket error: {error}")
        
        def on_close(ws):
            self.logger.info("Binance WebSocket connection closed")
        
        def on_open(ws):
            self.logger.info("Binance WebSocket connection opened")
            subscribe_message = {
                "method": "SUBSCRIBE",
                "params": [f"{symbol.lower()}@kline_1m"],
                "id": 1
            }
            ws.send(json.dumps(subscribe_message))
        
        ws = websocket.WebSocketApp(
            f"wss://stream.binance.com:9443/ws",
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open
        )
        
        if symbol not in self.ws_connections:
            self.ws_connections[symbol] = []
        self.ws_connections[symbol].append(ws)
        
        # Start WebSocket connection in a separate thread
        import threading
        ws_thread = threading.Thread(target=ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()
    
    def _setup_coinbase_websocket(self, symbol: str, callback) -> None:
        """Setup WebSocket connection to Coinbase"""
        def on_message(ws, message):
            data = json.loads(message)
            callback(data, 'coinbase')
        
        def on_error(ws, error):
            self.logger.error(f"Coinbase WebSocket error: {error}")
        
        def on_close(ws):
            self.logger.info("Coinbase WebSocket connection closed")
        
        def on_open(ws):
            self.logger.info("Coinbase WebSocket connection opened")
            subscribe_message = {
                "type": "subscribe",
                "product_ids": [symbol.replace('USDT', '-USD')],
                "channels": ["matches"]
            }
            ws.send(json.dumps(subscribe_message))
        
        ws = websocket.WebSocketApp(
            "wss://ws-feed.pro.coinbase.com",
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open
        )
        
        if symbol not in self.ws_connections:
            self.ws_connections[symbol] = []
        self.ws_connections[symbol].append(ws)
        
        # Start WebSocket connection in a separate thread
        import threading
        ws_thread = threading.Thread(target=ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()
