#!/usr/bin/env python3
import time
import schedule
import logging
from datetime import datetime
from configparser import ConfigParser
from scripts.api_client import fetch_crypto_data
from scripts.db_operations import initialize_database, store_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crypto_pipeline.log'),
        logging.StreamHandler()
    ]
)

def run_pipeline():
    """Execute one complete data pipeline cycle"""
    logging.info("Starting pipeline cycle")
    
    try:
        # 1. Fetch data
        df = fetch_crypto_data()
        if df is None or df.empty:
            logging.warning("No data received from API")
            return False
        
        # 2. Store data
        if not store_data(df):
            logging.error("Failed to store data")
            return False
        
        # 3. Log sample data
        logging.info(f"Sample data:\n{df[['symbol','price']].head(3).to_string(index=False)}")
        return True
        
    except Exception as e:
        logging.error(f"Pipeline error: {e}", exc_info=True)
        return False

def main():
    """Main application entry point"""
    try:
        logging.info("=== Starting Crypto Data Pipeline ===")
        
        # 1. Initialize database
        if not initialize_database():
            logging.error("Database initialization failed")
            return
        
        # 2. Get configuration
        config = ConfigParser()
        config.read('config/config.ini')
        interval = int(config['POSTGRES']['sync_interval'])
        
        # 3. Immediate first run
        run_pipeline()
        
        # 4. Schedule periodic runs
        schedule.every(interval).seconds.do(run_pipeline)
        logging.info(f"Pipeline started (runs every {interval}s)")
        logging.info("Press Ctrl+C to stop...")
        
        # 5. Main loop
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except KeyboardInterrupt:
        logging.info("Pipeline stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
    finally:
        logging.info("=== Pipeline shutdown ===")

if __name__ == "__main__":
    main()