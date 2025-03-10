from sqlwhisper.actors import stock_actor, stock_actor_without_context

def sql_vanilla():
    query_str = "Give me the last week of data for gold"

    sql_str = stock_actor_without_context.generate_sql_query(query_str)
    print(sql_str)

def sql_with_context():
    query_str = "Give me the last week of data for gold"
    sql_str = stock_actor.generate_sql_query(query_str)
    print(sql_str)

def sql_giberish():
    query_str = "I'm hungry"

    sql_str = stock_actor.generate_sql_query(query_str)
    print(sql_str)

if __name__ == '__main__':

    # sql_vanilla()
    sql_vanilla()
    # sql_giberish()
