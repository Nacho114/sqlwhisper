from collections.abc import Callable
from dataclasses import dataclass
from typing import List

from sqlwhisper.text_sql_pair_examples import TextSqlPair

@dataclass
class Evaluator:

    text_sql_pairs: List[TextSqlPair]
    text_to_sql: Callable[[str], str]

    def evaluate(self):
        for text_sql_pair in self.text_sql_pairs:
            sql_str = self.text_to_sql(text_sql_pair.text)
            print(f"User prompt\n{text_sql_pair.text}\n")
            print(f"Target\n{text_sql_pair.sql_str}\n")
            print(f"Prediced\n{sql_str}\n\n")

