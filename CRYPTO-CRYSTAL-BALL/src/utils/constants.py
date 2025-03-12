"""Constants for the CRYSTAL-CRYPTO-BALL application"""

# Supported cryptocurrencies
SUPPORTED_CRYPTOCURRENCIES = [
    "BTCUSDT", "ETHUSDT", "ETHFIUSDT", "1INCHUSDT", "AAVEUSDT", "ACEUSDT", "ACHUSDT",
    "ACXUSDT", "ADAUSDT", "AEROUSDT", "AEVOUSDT", "AIUSDT", "AI16ZUSDT", "AIOZUSDT",
    "AIXBTUSDT", "ALCHUSDT", "ALGOUSDT", "ALICEUSDT", "ALPHAUSDT", "ALTUSDT", "ANIMEUSDT",
    "ANKRUSDT", "APEUSDT", "API3USDT", "APTUSDT", "ARUSDT", "ARBUSDT", "ARPAUSDT",
    "ASTRUSDT", "ATHUSDT", "ATOMUSDT", "AUCTIONUSDT", "AVAUSDT", "AVAAIUSDT", "AVAXUSDT",
    "AXSUSDT", "B3USDT", "1MBABYDOGEUSDT", "BAKEUSDT", "BALUSDT", "BANUSDT", "BANANAUSDT",
    "BANDUSDT", "BATUSDT", "BBUSDT", "BCHUSDT", "BELUSDT", "BERAUSDT", "BICOUSDT",
    "BIGTIMEUSDT", "BIOUSDT", "BLASTUSDT", "BNBUSDT", "BNTUSDT", "BNXUSDT", "BOMEUSDT",
    "1000BONKUSDT", "BROCCOLIUSDT", "BSVUSDT", "BUZZUSDT", "C98USDT", "CAKEUSDT",
    "CATIUSDT", "CELOUSDT", "CELRUSDT", "CETUSUSDT", "CFXUSDT", "CGPTUSDT", "CHRUSDT",
    "CHZUSDT", "CKBUSDT", "COMPUSDT", "COOKIEUSDT", "COTIUSDT", "COWUSDT", "CRVUSDT",
    "CTCUSDT", "CTSIUSDT", "CVXUSDT", "CYBERUSDT", "DEGENUSDT", "DENTUSDT", "DEXEUSDT",
    "DFUSDT", "DOGEUSDT", "DOTUSDT", "DUSKUSDT", "DYDXUSDT", "EDUUSDT", "EGLDUSDT",
    "EIGENUSDT", "ENAUSDT", "ENJUSDT", "ENSUSDT", "EOSUSDT", "ETCUSDT", "FARTCOINUSDT",
    "FETUSDT", "FILUSDT", "FLMUSDT", "FLOCKUSDT", "1000FLOKIUSDT", "FLOWUSDT", "FORTHUSDT",
    "FOXYUSDT", "FTNUSDT", "FUELUSDT", "FWOGUSDT", "FXSUSDT", "GALAUSDT", "GASUSDT",
    "GIGAUSDT", "GLMUSDT", "GMTUSDT", "GMXUSDT", "GNOUSDT", "GOATUSDT", "GODSUSDT",
    "GPSUSDT", "GRASSUSDT", "GRIFFAINUSDT", "GRTUSDT", "HBARUSDT", "HEIUSDT", "HIFIUSDT",
    "HIPPOUSDT", "HIVEUSDT", "HMSTRUSDT", "ICPUSDT", "ICXUSDT", "IMXUSDT", "INJUSDT",
    "IOUSDT", "IOSTUSDT", "IOTAUSDT", "IOTXUSDT", "IPUSDT", "JUSDT", "JAILSTOOLUSDT",
    "JASMYUSDT", "JELLYJELLYUSDT", "JTOUSDT", "JUPUSDT", "KAITOUSDT", "KASUSDT", "KAVAUSDT",
    "KDAUSDT", "KNCUSDT", "KOMAUSDT", "KSMUSDT", "10000LADYSUSDT", "LAYERUSDT", "LDOUSDT",
    "LEVERUSDT", "LINAUSDT", "LINKUSDT", "LOOKSUSDT", "LPTUSDT", "LQTYUSDT", "LRCUSDT",
    "LSKUSDT", "LTCUSDT", "LUCEUSDT", "LUMIAUSDT", "LUNA2USDT", "1000LUNCUSDT", "MAGICUSDT",
    "MANAUSDT", "MANTAUSDT", "MASKUSDT", "MAVUSDT", "MEUSDT", "MELANIAUSDT", "MEMEUSDT",
    "MEWUSDT", "MINAUSDT", "MKRUSDT", "MOCAUSDT", "MOODENGUSDT", "MOVEUSDT", "MOVRUSDT",
    "MTLUSDT", "NCUSDT", "NEARUSDT", "NEIROETHUSDT", "NEOUSDT", "NMRUSDT", "NOTUSDT",
    "ONDOUSDT", "ONEUSDT", "ONTUSDT", "OPUSDT", "ORCAUSDT", "ORDIUSDT", "OXTUSDT",
    "PAXGUSDT", "PENDLEUSDT", "PENGUUSDT", "PEOPLEUSDT", "1000PEPEUSDT", "PERPUSDT",
    "PHAUSDT", "PHBUSDT", "PIPPINUSDT", "PLUMEUSDT", "PNUTUSDT", "POLUSDT", "POLYXUSDT",
    "PONKEUSDT", "PROMUSDT", "PYTHUSDT", "QNTUSDT", "QTUMUSDT", "RADUSDT", "1000RATSUSDT",
    "RDNTUSDT", "REZUSDT", "RIFUSDT", "RLCUSDT", "RONUSDT", "RSRUSDT", "RUNEUSDT",
    "RVNUSDT", "SUSDT", "SAFEUSDT", "SAGAUSDT", "SANDUSDT", "1000SATSUSDT", "SCRTUSDT",
    "SEIUSDT", "SFPUSDT", "SHELLUSDT", "1000SHIBUSDT", "SKLUSDT", "SNXUSDT", "SOLUSDT",
    "SOLVUSDT", "SONICUSDT", "SSVUSDT", "STGUSDT", "STORJUSDT", "STXUSDT", "SUIUSDT",
    "SUNDOGUSDT", "SUSHIUSDT", "SWARMSUSDT", "SXPUSDT", "TAIKOUSDT", "TAOUSDT", "THETAUSDT",
    "TIAUSDT", "TLMUSDT", "TNSRUSDT", "TOKENUSDT", "TONUSDT", "TRBUSDT", "TRUMPUSDT",
    "TRXUSDT", "TSTUSDT", "TURBOUSDT", "UNIUSDT", "USTCUSDT", "USUALUSDT", "UXLINKUSDT",
    "VANAUSDT", "VELOUSDT", "VETUSDT", "VINEUSDT", "VTHOUSDT", "VVVUSDT", "WUSDT",
    "WIFUSDT", "WLDUSDT", "WOOUSDT", "XUSDT", "XAIUSDT", "1000XECUSDT", "XIONUSDT",
    "XLMUSDT", "XRPUSDT", "XTZUSDT", "YGGUSDT", "ZENUSDT", "ZEREBROUSDT", "ZILUSDT",
    "ZKUSDT", "ZRCUSDT", "ZRXUSDT"
]

# Model information
MODEL_INFO = {
    "LSTM": "Deep learning model for sequence prediction",
    "CatBoost": "Gradient boosting on decision trees",
    "LightGBM": "Light Gradient Boosting Machine",
    "Prophet": "Time series forecasting model",
    "RandomForest": "Ensemble learning method",
    "XGBoost": "Extreme Gradient Boosting",
    "MASTER": "Combined prediction using weighted ensemble"
}

# Graph types
GRAPH_TYPES = ["line", "candle", "bar"]

# Overlay types
OVERLAY_TYPES = {
    "buy_sell": "Buy/Sell Signals",
    "high_low": "High/Low Points",
    "volatility": "Volatility Bands",
    "volume": "Volume Profile"
}

# Forecast length limits
FORECAST_LENGTH_LIMITS = {
    "hours": {
        "min": 1,
        "max": 24
    },
    "days": {
        "min": 0,
        "max": 30
    }
}

# Data acquisition settings
DATA_ACQUISITION = {
    "max_retries": 3,
    "retry_delay": 5,  # seconds
    "timeout": 30,  # seconds
    "batch_size": 1000,  # records per request
    "rate_limit": {
        "requests": 10,
        "per_second": 1
    }
}

# WebSocket settings
WEBSOCKET = {
    "reconnect_delay": 5,  # seconds
    "max_reconnects": 5,
    "heartbeat_interval": 30  # seconds
}

# Cache settings
CACHE = {
    "max_size": 1000,  # MB
    "expiry": 3600,  # seconds
    "cleanup_interval": 300  # seconds
}

# Technical indicators
TECHNICAL_INDICATORS = {
    "SMA": {
        "window": 20
    },
    "EMA": {
        "window": 12
    },
    "RSI": {
        "window": 14
    },
    "MACD": {
        "fast": 12,
        "slow": 26,
        "signal": 9
    },
    "Bollinger": {
        "window": 20,
        "std": 2
    }
}

# Model training settings
TRAINING = {
    "validation_split": 0.2,
    "early_stopping_patience": 10,
    "max_epochs": 100,
    "batch_size": 32,
    "learning_rate": 0.001
}

# Prediction settings
PREDICTION = {
    "confidence_threshold": 0.8,
    "update_interval": 60,  # seconds
    "smoothing_window": 5
}

# GUI settings
GUI = {
    "min_width": 800,
    "min_height": 600,
    "default_width": 1200,
    "default_height": 800,
    "refresh_rate": 1000,  # milliseconds
    "animation_speed": 1.0
}
