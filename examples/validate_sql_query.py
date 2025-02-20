from sqlwhisper.actors import stock_actor

def correct_query():
    query_str = "Give me the last week of data for gold"
    validator = stock_actor.validate_user_query(query_str)
    print(validator.contains_valid_query)
    print(validator.reasoning)

def wrong_query():
    query_str = "Show me all stocks of pengiuns with 1 week price"
    validator = stock_actor.validate_user_query(query_str)
    print(validator.contains_valid_query)
    print(validator.reasoning)

def very_wrong_query():
    query_str = "Show me all the green bears!"
    validator = stock_actor.validate_user_query(query_str)
    print(validator.contains_valid_query)
    print(validator.reasoning)

if __name__ == '__main__':

    correct_query()
    wrong_query()

