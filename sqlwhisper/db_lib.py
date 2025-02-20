from sqlalchemy import create_engine
from dotenv import load_dotenv

import os

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")

# TODO: hardcoded variables!
engine = create_engine(f"postgresql://{user}:{password}@localhost/stock_data")

FUTURES_TABLE = "futures_data"
ARTIST_TABLE = "artist_data"
TOY_TABLE = "toy_data"
