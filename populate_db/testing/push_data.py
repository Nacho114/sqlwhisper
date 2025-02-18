from dotenv import dotenv_values

config = dotenv_values(".env")

import psycopg2

conn = psycopg2.connect(dbname="stock_data", user=config.get("POSTGRES_USER"), password=config.get("POSTGRES_PASSWORD"), host="localhost", port="5432")
cur = conn.cursor()

cur.execute("""
    INSERT INTO testing_data (symbol, price)
    VALUES (%s, %s)
    """,
    ('yes', -42.0))

conn.commit()

cur.execute("SELECT * FROM testing_data")
print(cur.fetchall())


conn.close()
