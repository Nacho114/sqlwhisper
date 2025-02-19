PROMPT_FOR_VALIDATING_QUERY_FOR_YFINANCE = (
    "We want to check if a user prompt can be converted by an llm into a sql query"
    "e.g. Give me all users older than 3, then the llm might return SELECT * from USER WHERE Age > 3;"
    "e.g. Give me blue trees, then this would not be possible"
    "The data in question the llm has access to is a financial data, hence the tickers are GC=F, SI=F, CL=F for gold, silder and copper"
    "It contains OHLC time series financial data"
    "So queries only related to this will work"
    #TODO: Very sensitive to this lower prompt, note, this is over fitting!
    "Be very relaxed, e.g. Show me the latest silver price, should be ok" 
)

PROMPT_FOR_GENERATING_SQL_QUERY = (
    "This is futures data db of financial data"
    "Hence the tickers are GC=F, SI=F, CL=F for gold, silder and copper"
)
