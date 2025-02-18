from stockwhisper.actions import * 

#query_str = "What different types of tickers are there?"
query_str = "Give me the last week of data for gold"
# sql_str = generate_sql_query('hello world')
# sql_str = " SELECT symbol, trade_date, close_price FROM futures_data ORDER BY trade_date DESC LIMIT 5;"
# sql_str = "SELECT DISTINCT symbol FROM futures_data ORDER BY symbol;"
sql_str = "SELECT fd.trade_date, fd.open_price, fd.high_price, fd.low_price, fd.close_price, fd.volume \nFROM futures_data fd \nWHERE fd.symbol = 'GOLD' \nAND fd.trade_date >= NOW() - INTERVAL '7 days' \nORDER BY fd.trade_date DESC;"
# print('\n', sql_str)
df = execute_sql_query(sql_str)
evluate_result(sql_str, df)
