import psycopg2
from dotenv import load_dotenv
import os
import logging
from typing import List, Dict, Tuple

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

class ArtistDataPopulator:
    def __init__(self):
        self.artist_data = {
            "Tupac": {
                "aliases": ["Tupac", "2Pac", "Makaveli", "Tupac Shakur", "Pac"],
                "albums": [
                    ("All Eyez on Me", 9800000),
                    ("Me Against the World", 5400000),
                    ("The Don Killuminati: The 7 Day Theory", 4000000),
                    ("R U Still Down?", 3500000),
                    ("Until the End of Time", 2900000)
                ]
            },
            "Kendrick": {
                "aliases": ["Kendrick", "Kendrick Lamar", "K-Dot", "Kung Fu Kenny", "King Kendrick"],
                "albums": [
                    ("DAMN.", 3500000),
                    ("good kid, m.A.A.d city", 3200000),
                    ("To Pimp a Butterfly", 2700000),
                    ("Section.80", 1800000),
                    ("Mr. Morale & the Big Steppers", 1200000)
                ]
            }
        }

    def create_artist_table(self, conn) -> bool:
        """
        Create the artist_data table if it doesn't exist
        """
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS artist_data (
                        id SERIAL PRIMARY KEY,
                        album VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        downloads INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info("Artist data table created or already exists")
                return True
        except Exception as e:
            logger.error(f"Error creating artist_data table: {e}")
            conn.rollback()
            return False

    def populate_artist_data(self, conn) -> Dict[str, bool]:
        """
        Populate the artist_data table with one album per artist alias
        """
        results = {}
        
        try:
            with conn.cursor() as cur:
                for artist, data in self.artist_data.items():
                    aliases = data["aliases"]
                    albums = data["albums"]
                    
                    # Match each alias with one album
                    # If we have more aliases than albums, some albums will be reused
                    for i, alias in enumerate(aliases):
                        album_idx = i % len(albums)
                        album_name, downloads = albums[album_idx]
                        
                        try:
                            cur.execute("""
                                INSERT INTO artist_data (album, name, downloads)
                                VALUES (%s, %s, %s)
                            """, (album_name, alias, downloads))
                            
                        except Exception as e:
                            logger.error(f"Error inserting data for {alias}, album {album_name}: {e}")
                            conn.rollback()
                            results[f"{alias}:{album_name}"] = False
                            continue
                    
                    results[artist] = True
                
                conn.commit()
                logger.info("Successfully populated artist_data table")
                
        except Exception as e:
            logger.error(f"Database error while populating artist_data: {e}")
            conn.rollback()
            return {artist: False for artist in self.artist_data.keys()}
            
        return results
    
def main():
    populator = ArtistDataPopulator()
    
    with DatabaseConnection() as conn:
        # Create table
        if not populator.create_artist_table(conn):
            logger.error("Failed to create table. Exiting.")
            return
        
        # Populate data
        results = populator.populate_artist_data(conn)
        for artist, success in results.items():
            status = "Successfully processed" if success else "Failed to process"
            logger.info(f"{status}: {artist}")
        
if __name__ == "__main__":
    main()
