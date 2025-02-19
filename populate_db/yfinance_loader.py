import yfinance as yf
import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import logging
from typing import Optional, List, Dict
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.db_params = {
            "dbname": os.getenv("DB_NAME", "stock_data"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432")
        }

    def __enter__(self):
        self.conn = psycopg2.connect(**self.db_params)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

#TODO: This has not been tested! GPT Magic, i originally create the DB with raw sql
def ensure_table_exists(self):
    """
    Check if futures_data table exists and create it if it doesn't
    """
    with self.conn.cursor() as cur:
        # Check if table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'futures_data'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            logger.info("Creating futures_data table")
            cur.execute("""
                CREATE TABLE futures_data (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(20) NOT NULL,
                    trade_date DATE NOT NULL,
                    open_price NUMERIC(15, 5) NOT NULL,
                    high_price NUMERIC(15, 5) NOT NULL,
                    low_price NUMERIC(15, 5) NOT NULL,
                    close_price NUMERIC(15, 5) NOT NULL,
                    volume BIGINT NOT NULL,
                    source VARCHAR(50) DEFAULT 'yfinance',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_symbol_date UNIQUE (symbol, trade_date)
                );
                
                CREATE INDEX idx_futures_symbol ON futures_data(symbol);
                CREATE INDEX idx_futures_date ON futures_data(trade_date);
            """)
            self.conn.commit()
            logger.info("Successfully created futures_data table")
        else:
            logger.debug("futures_data table already exists")
            
    return self.conn

class StockDataIngestion:
    def __init__(self, start_date: str = "1900-01-01"):
        self.start_date = start_date
        self.retry_attempts = 3
        self.retry_delay = 5  # seconds

    def get_stock_history(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        Download stock history with retry logic
        """
        for attempt in range(self.retry_attempts):
            try:
                data = yf.download(ticker, start=self.start_date, progress=False)
                if data is None:
                    logger.warning(f"No data retrieved for {ticker}")
                    return None
                return data
            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{self.retry_attempts} failed for {ticker}: {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"All attempts failed for {ticker}")
                    return None

    def insert_data_into_postgres(self, conn, ticker: str, data: pd.DataFrame, source: str = "yfinance") -> bool:
        """
        Insert data into PostgreSQL with better error handling
        """
        if data is None or data.empty:
            logger.warning(f"No data to insert for {ticker}")
            return False

        success = True
        inserted_rows = 0
        skipped_rows = 0

        try:
            with conn.cursor() as cur:
                for idx, row in data.iterrows():
                    # Convert index to string first, then to datetime
                    trade_date = datetime.strptime(str(idx)[:10], '%Y-%m-%d')
                    
                    values = {
                        'open_price': float(row['Open'].item()),
                        'high_price': float(row['High'].item()),
                        'low_price': float(row['Low'].item()),
                        'close_price': float(row['Close'].item()),
                        'volume': int(row['Volume'].item())
                    }

                    # Validate data
                    if any(pd.isna(v) for v in values.values()):
                        skipped_rows += 1
                        continue

                    try:
                        cur.execute("""
                            INSERT INTO futures_data 
                            (symbol, trade_date, open_price, high_price, low_price, close_price, volume, source)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (symbol, trade_date) DO UPDATE SET
                            open_price = EXCLUDED.open_price,
                            high_price = EXCLUDED.high_price,
                            low_price = EXCLUDED.low_price,
                            close_price = EXCLUDED.close_price,
                            volume = EXCLUDED.volume,
                            source = EXCLUDED.source
                        """, (ticker, trade_date, *values.values(), source))
                        inserted_rows += 1

                    except Exception as e:
                        logger.error(f"Error inserting row for {ticker} on {trade_date}: {e}")
                        conn.rollback()
                        success = False
                        break

                if success:
                    conn.commit()
                    logger.info(f"Successfully processed {ticker}: {inserted_rows} rows inserted, {skipped_rows} rows skipped")

        except Exception as e:
            logger.error(f"Database error for {ticker}: {e}")
            conn.rollback()
            success = False

        return success

    def process_tickers(self, tickers: List[str]) -> Dict[str, bool]:
        """
        Process multiple tickers and return results
        """
        results = {}
        
        with DatabaseConnection() as conn:
            for ticker in tickers:
                logger.info(f"Processing {ticker}")
                data = self.get_stock_history(ticker)
                if data is not None:
                    success = self.insert_data_into_postgres(conn, ticker, data)
                    results[ticker] = success
                else:
                    results[ticker] = False
                    
        return results

def main():
    ingestion = StockDataIngestion()
    # For initial testing with one stock
    # test_ticker = "GC=F"
    # results = ingestion.process_tickers([test_ticker])
    
    tickers = ["GC=F", "SI=F", "CL=F"]  # Add more tickers as needed
    results = ingestion.process_tickers(tickers)
    
    # Print summary
    for ticker, success in results.items():
        status = "Successfully processed" if success else "Failed to process"
        logger.info(f"{status}: {ticker}")

if __name__ == "__main__":
    main()
