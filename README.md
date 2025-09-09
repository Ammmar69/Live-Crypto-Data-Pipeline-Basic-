# Crypto Data Pipeline Live

A real-time cryptocurrency data pipeline that fetches live market data from an API, stores it in a PostgreSQL database, and visualizes it in Power BI. This project demonstrates a complete ETL (Extract, Transform, Load) workflow for financial data processing.

## Overview

This pipeline continuously collects cryptocurrency market data including price, volume, and price changes at regular intervals. The data is structured, stored in a relational database, and made available for visualization and analysis.

## Features

- Real-time cryptocurrency data fetching from API
- Automated data storage in PostgreSQL with error handling
- Configurable data collection intervals
- Power BI dashboard for data visualization
- Robust logging and error handling

## Project Structure

```
crypto-data-pipeline/
│
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── config/
│   └── config.ini         # Configuration file
├── scripts/
│   ├── api_client.py      # API data fetching module
│   ├── db_operations.py   # Database operations
│   ├── postgres_sync.py   # PostgreSQL synchronization
│   └── __init__.py
└── Power Bi/
    └── OUTPUT.pbix        # Power BI dashboard file only for the output not properly built
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Power BI Desktop (for visualization)

### Installation

1. Clone the repository:
```
git clone <repository-url>
cd crypto-data-pipeline
```

2. Install required Python packages:
```
pip install -r requirements.txt
```

3. Configure the database connection:
   - Edit `config/config.ini` with your PostgreSQL credentials
   - Set the desired sync interval and cryptocurrency symbols

### Configuration

Update the `config/config.ini` file with your specific settings:

```ini
[API]
base_url = https://api.binance.com
endpoint = /api/v3/ticker/24hr
symbols = BTCUSDT, ETHUSDT, ADAUSDT

[POSTGRES]
host = localhost
port = 5432
database = crypto_db
user = your_username
password = your_password
sync_interval = 60
```

## Usage

Run the main pipeline:

```
python main.py
```

The application will:
1. Initialize the database table if it doesn't exist
2. Fetch data for the specified cryptocurrencies
3. Store the data in PostgreSQL
4. Continue fetching at the configured interval

## Database Schema

The data is stored in the `crypto_prices` table with the following structure:

- id: Primary key (auto-incrementing)
- timestamp: Data collection timestamp
- symbol: Cryptocurrency symbol (e.g., BTCUSDT)
- price: Current price
- price_change: Absolute price change
- price_change_percent: Percentage price change
- volume: Trading volume
- last_trade_time: Time of last trade
- created_at: Record creation timestamp

## Visualization

Open the `Power Bi/OUTPUT.pbix` file in Power BI Desktop to view the pre-configured dashboard showing:

- Price trends over time
- Volume analysis
- Price change comparisons
- Real-time market data visualization

## Technologies Used

- Python
- PostgreSQL
- SQLAlchemy (ORM)
- Power BI
- Binance API 

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
