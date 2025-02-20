from sqlwhisper.actor import Actor
from sqlwhisper.db_lib import FUTURES_TABLE
from sqlwhisper.evaluator import Evaluator
from sqlwhisper.text_sql_pair_examples import stock_text_sql_pairs

from sqlwhisper.actors import stock_actor

def actor_without_context(query_str: str):
    blind_actor = Actor(FUTURES_TABLE)
    sql_str = blind_actor.generate_sql_query(query_str)
    return sql_str


def actor_with_context(query_str: str):
    sql_str = stock_actor.generate_sql_query(query_str)
    return sql_str

def id(str):
    return str

if __name__ == '__main__':

    evaluator = Evaluator(stock_text_sql_pairs, actor_with_context)
    evaluator.evaluate()

    evaluator = Evaluator(stock_text_sql_pairs, actor_without_context)
    evaluator.evaluate()
