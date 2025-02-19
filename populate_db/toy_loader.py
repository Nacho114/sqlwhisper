import psycopg2
from dotenv import load_dotenv
import os
import logging
from typing import List, Tuple
import random

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

class ToyDatasetCreator:
    def __init__(self, num_entries=20):
        self.num_entries = num_entries
        
    def create_toy_table(self, conn) -> bool:
        """
        Create the toy_data table if it doesn't exist
        """
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS toy_data (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        value INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info("Toy data table created or already exists")
                return True
        except Exception as e:
            logger.error(f"Error creating toy_data table: {e}")
            conn.rollback()
            return False

    def generate_toy_data(self) -> List[Tuple[str, int]]:
        """
        Generate toy dataset with repeated names and random values
        """
        dataset = []
        
        for i in range(self.num_entries):
            # Select a random base name
            
            # Repeat the name a random number of times (1-5)
            repetition = random.randint(1, 6)
            name = 'a' * repetition
            
            # Generate a random value between 1 and 1000
            value = random.randint(1, 10000)
            
            dataset.append((name, value))
            
        return dataset

    def populate_toy_data(self, conn) -> bool:
        """
        Populate the toy_data table with generated data
        """
        try:
            dataset = self.generate_toy_data()
            
            with conn.cursor() as cur:
                for name, value in dataset:
                    cur.execute("""
                        INSERT INTO toy_data (name, value)
                        VALUES (%s, %s)
                    """, (name, value))
                
                conn.commit()
                logger.info(f"Successfully populated toy_data table with {self.num_entries} entries")
                return True
                
        except Exception as e:
            logger.error(f"Database error while populating toy_data: {e}")
            conn.rollback()
            return False
    
    def print_dataset(self) -> None:
        """
        Print the generated dataset to console (for verification)
        """
        dataset = self.generate_toy_data()
        print("\nGenerated Toy Dataset:")
        print("-" * 30)
        print(f"{'Name':<20} {'Value':<10}")
        print("-" * 30)
        for name, value in dataset:
            print(f"{name:<20} {value:<10}")
        print("-" * 30)
    
def main():
    breakpoint()
    creator = ToyDatasetCreator(num_entries=20)
    
    # Print sample dataset to console (even if DB connection fails)
    creator.print_dataset()
    
    try:
        with DatabaseConnection() as conn:
            # Create table
            if not creator.create_toy_table(conn):
                logger.error("Failed to create table. Exiting.")
                return
            
            # Populate data
            success = creator.populate_toy_data(conn)
            if success:
                logger.info("Toy dataset created successfully")
            else:
                logger.error("Failed to create toy dataset")

    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        logger.info("Generated dataset was printed to console for reference")
        
if __name__ == "__main__":
    main()
