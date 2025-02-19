from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")

from sqlalchemy import create_engine, text

engine = create_engine(f"postgresql://{user}:{password}@localhost/stock_data")

with engine.connect() as con:
    query = text('SELECT open_price FROM futures_data WHERE symbol = :symbol LIMIT 10')
    result = con.execute(query, {"symbol": "GC=F"})

    # Fetch and process the results
    for row in result:
        print(row)

engine.dispose()
