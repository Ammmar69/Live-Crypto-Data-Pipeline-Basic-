import requests
import pandas as pd
from datetime import datetime, timezone
from configparser import ConfigParser

def fetch_crypto_data():
    config = ConfigParser()
    config.read('config/config.ini')
    symbols = [s.strip() for s in config['API']['symbols'].split(',')]
    
    data = []
    for symbol in symbols:
        try:
            url = f"{config['API']['base_url']}{config['API']['endpoint']}?symbol={symbol}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            data.append({
                'timestamp': datetime.now(timezone.utc),
                'symbol': symbol,
                'price': float(result['lastPrice']),
                'price_change': float(result['priceChange']),
                'price_change_percent': float(result['priceChangePercent']),
                'volume': float(result['volume']),
                'last_trade_time': pd.to_datetime(result['closeTime'], unit='ms', utc=True)
            })
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
    
    return pd.DataFrame(data) if data else None