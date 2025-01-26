import requests
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
from config.settings import DATABASE_URL, SERVICE_ACCOUNT_KEY

# Initialize Firebase Admin SDK
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred, {
    "databaseURL": DATABASE_URL
})

# Reference to the database
firebase_db = db.reference("cryptocurrencies")

# Binance API Base URL
BINANCE_BASE_URL = "https://api.binance.com"

# Fetch historical data from Binance
def fetch_binance_data(symbol, interval, limit=500):
    """
    Fetch historical data from Binance API.
    Args:
    - symbol (str): Cryptocurrency pair (e.g., BTCUSDT)
    - interval (str): Interval for candlestick data (e.g., '1d', '1w', '1M')
    - limit (int): Number of data points to fetch (max 1000)
    """
    endpoint = f"{BINANCE_BASE_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {symbol}: {response.text}")
        return []

# Process Binance data
def process_binance_data(raw_data):
    """
    Process raw Binance data into a usable format.
    Args:
    - raw_data (list): Raw data from Binance API.
    Returns:
    - Dictionary with date as key and price data as value.
    """
    processed_data = {}
    for entry in raw_data:
        date_key = datetime.fromtimestamp(entry[0] / 1000).strftime("%Y-%m-%d")
        processed_data[date_key] = {
            "open_price": float(entry[1]),
            "high": float(entry[2]),
            "low": float(entry[3]),
            "close": float(entry[4]),
        }
    return processed_data

# Populate Firebase Database
def populate_database():
    cryptocurrencies = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    intervals = {
        "monthly": "1M",
        "weekly": "1w",
        "daily": "1d"
    }

    for crypto in cryptocurrencies:
        crypto_data = {}
        for timeframe, interval in intervals.items():
            print(f"Fetching {timeframe} data for {crypto}...")
            raw_data = fetch_binance_data(crypto, interval, limit=12 if interval == "1M" else 52 if interval == "1w" else 365)
            processed_data = process_binance_data(raw_data)
            crypto_data[timeframe] = processed_data

        # Push data to Firebase
        symbol = crypto.replace("USDT", "")
        firebase_db.child(symbol).set(crypto_data)
        print(f"Data for {symbol} added successfully!")

# Run the script
if __name__ == "__main__":
    populate_database()
