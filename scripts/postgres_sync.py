from sqlalchemy import create_engine, text
import pandas as pd
from configparser import ConfigParser
import time

def create_pg_engine():
    config = ConfigParser()
    config.read('config/config.ini')
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{config['POSTGRES']['user']}:"
            f"{config['POSTGRES']['password']}@"
            f"{config['POSTGRES']['host']}:"
            f"{config['POSTGRES']['port']}/"
            f"{config['POSTGRES']['database']}",
            pool_pre_ping=True
        )
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")
        return None

def init_pg():
    engine = create_pg_engine()
    if not engine:
        return False
    
    try:
        with engine.connect() as conn:
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                symbol TEXT NOT NULL,
                price DOUBLE PRECISION,
                price_change DOUBLE PRECISION,
                price_change_percent DOUBLE PRECISION,
                volume DOUBLE PRECISION,
                last_trade_time TIMESTAMPTZ,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                UNIQUE(symbol, timestamp)
            """))
            conn.commit()
        return True
    except Exception as e:
        print(f"PostgreSQL init failed: {e}")
        return False

def store_in_pg(df):
    if df is None or df.empty:
        return False
        
    engine = create_pg_engine()
    if not engine:
        return False
        
    try:
        with engine.begin() as conn:
            df.to_sql(
                name='crypto_prices',
                con=conn,
                if_exists='append',
                index=False,
                method='multi'
            )
        return True
    except Exception as e:
        print(f"PostgreSQL store failed: {e}")
        return False