import yfinance as yf
import pandas as pd
from datetime import datetime

def run():

    df = yf.download("AAPL")

    if df is None:
        print('none')
    else:
        for idx, row in df.iterrows():
            # Convert index to string first, then to datetime
            trade_date = datetime.strptime(str(idx)[:10], '%Y-%m-%d')

            print(float(row['Open'].item()))

            return
   
run()
