from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from llama_index.core.retrievers import NLSQLRetriever
from llama_index.core.query_engine import NLSQLTableQueryEngine
from sqlalchemy import text
import pandas as pd

from stockwhisper.db_lib import engine

llm = OpenAI(temperature=0.1, model="gpt-4o-mini")
sql_database = SQLDatabase(engine, include_tables=["futures_data"])

def generate_sql_query(query_str: str) -> str:
    """
    Assume Query is reasonable
    """

    nl_sql_retriever = NLSQLRetriever(
        sql_database=sql_database, tables=["futures_data"], llm=llm, sql_only=True
    )

    results = nl_sql_retriever.retrieve(
        query_str
    )

    result = results[0]
    print(result)

    sql_str = result.text

    return sql_str


def execute_sql_query(sql_str: str) -> pd.DataFrame:
    with engine.connect() as con:
        query = text(sql_str)
        result = con.execute(query)
        df = pd.DataFrame(result)

        engine.dispose()
        return df


def evluate_result(query_str: str, df: pd.DataFrame):

    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database, tables=["futures_data"], llm=llm
    )
    # query_str = f"Based on this query: {query_str}, does this result make sense: {df}. If the df is empty, is this an expected result, if not, why not? Make sure that there is no issue with symbol names missmatch!"
    query_str = f"what types of different tickers are there? {query_str} was empty, what could be wrong with this query?"

    response = query_engine.query(query_str)

    print(response)
