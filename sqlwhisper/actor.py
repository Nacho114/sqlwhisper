from llama_index.core import SQLDatabase
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.llms.openai import OpenAI
from llama_index.core.retrievers import NLSQLRetriever
from sqlalchemy import text

"""
Main references

[Structured (Pydantic) llms](https://docs.llamaindex.ai/en/stable/understanding/extraction/structured_llms/)
[text-to-sql](https://docs.llamaindex.ai/en/stable/examples/index_structs/struct_indices/SQLIndexDemo/)

"""

import pandas as pd

from sqlwhisper.db_lib import engine

class UserQueryValidator(BaseModel):
    """
    This class gives information about the validity of a query
    """
    contains_valid_query: bool = Field(
        ...,
        description="True if the user query is a valid command"
    )
    reasoning: str = Field(
        ...,
        description="Contains the reasoning behind the decision"
    )

class Actor:

    def __init__(self, table_name: str, sql_validator_prompt: str = '', text_to_sql_prompt: str = ''):
        self.table_name = table_name
        self.sql_validator_prompt = sql_validator_prompt
        self.text_to_sql_prompt = text_to_sql_prompt
        self.llm = OpenAI(temperature=0.1, model="gpt-4o-mini")
        self.sql_database = SQLDatabase(engine, include_tables=[table_name])

    def validate_user_query(self, query_str: str) -> UserQueryValidator:
        eval_query_str = f"User query validator text:{self.sql_validator_prompt}\n User prompt: {query_str}"
        sllm = self.llm.as_structured_llm(UserQueryValidator)
        response = sllm.complete(eval_query_str)
        validator = response.raw

        assert isinstance(validator, UserQueryValidator)

        return validator

    def generate_sql_query(self, query_str: str) -> str:
        query_str = f"User query{query_str}\nExtra context: {self.text_to_sql_prompt}"

        nl_sql_retriever = NLSQLRetriever(
            sql_database=self.sql_database, tables=[self.table_name], llm=self.llm, sql_only=True
        )

        results = nl_sql_retriever.retrieve(
            query_str
        )

        sql_str = results[0].text

        return sql_str

    def execute_sql_query(self, sql_str: str) -> pd.DataFrame:
        with engine.connect() as con:
            query = text(sql_str)
            result = con.execute(query)
            df = pd.DataFrame(result)
            return df
