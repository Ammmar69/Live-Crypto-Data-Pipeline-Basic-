from sqlalchemy import create_engine, text
import pandas as pd
from configparser import ConfigParser
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_db_engine():
    """Create and return PostgreSQL engine with retry logic"""
    config = ConfigParser()
    config.read('config/config.ini')
    
    connection_string = (
        f"postgresql+psycopg2://{config['POSTGRES']['user']}:"
        f"{config['POSTGRES']['password']}@"
        f"{config['POSTGRES']['host']}:"
        f"{config['POSTGRES']['port']}/"
        f"{config['POSTGRES']['database']}"
    )
    
    try:
        engine = create_engine(
            connection_string,
            pool_pre_ping=True,
            connect_args={'connect_timeout': 5}
        )
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return None

def initialize_database():
    """Initialize PostgreSQL tables"""
    engine = create_db_engine()
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
            )
            """))
            conn.commit()
        logging.info("Database tables initialized")
        return True
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")
        return False

def store_data(df):
    """Store DataFrame in PostgreSQL"""
    if df is None or df.empty:
        logging.warning("No data to store")
        return False
    
    engine = create_db_engine()
    if not engine:
        return False
    
    try:
        with engine.begin() as conn:  # Auto-commit transaction
            df.to_sql(
                name='crypto_prices',
                con=conn,
                if_exists='append',
                index=False,
                method='multi'
            )
        logging.info(f"Stored {len(df)} records")
        return True
    except Exception as e:
        logging.error(f"Data storage failed: {e}")
        return False