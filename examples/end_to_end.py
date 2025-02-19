from stockwhisper.actors import stock_actor

def happy_path():
    print('Running AIAIAIAI')

    query_str = "Give me the last week of data for gold"
    validator = stock_actor.validate_user_query(query_str)

    print(f"Prompt valid = {validator.contains_valid_query}")
    if not validator.contains_valid_query:
        return

    print("generating SQL query")
    sql_str = stock_actor.generate_sql_query_with_context(query_str)

    print(f"executing SQL query\n{sql_str}")
    df = stock_actor.execute_sql_query(sql_str)
    print(df)


if __name__ == '__main__':
    happy_path()

