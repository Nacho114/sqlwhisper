from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")

from sqlalchemy import create_engine

engine = create_engine(f"postgresql://{user}:{password}@localhost/stock_data")

from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI

llm = OpenAI(temperature=0.1, model="gpt-4o-mini")
sql_database = SQLDatabase(engine, include_tables=["futures_data"])

from llama_index.core.retrievers import NLSQLRetriever


nl_sql_retriever = NLSQLRetriever(
    sql_database=sql_database, tables=["futures_data"], llm=llm, sql_only=True
)

#query_str = "What different types of tickers are there?"
query_str = "Give me the last week of data for gold"
results = nl_sql_retriever.retrieve(
    query_str
)

print(results)

