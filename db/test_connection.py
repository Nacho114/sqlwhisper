from dotenv import dotenv_values

config = dotenv_values(".env")

import psycopg2

conn = psycopg2.connect(dbname="stock_data", user=config.get("POSTGRES_USER"), password=config.get("POSTGRES_PASSWORD"), host="localhost", port="5432")
cur = conn.cursor()

print("Connected to PostgreSQL")

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
tables = cur.fetchall()

if tables:
    print("\nTables in 'public' schema:")
    for table in tables:
        print(f"- {table[0]}")
else:
    print("\nNo tables found.")

