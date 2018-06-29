from marketsimcode import compute_portvals, port_val_stats
import datetime as dt
import pandas as pd
from util import get_data, plot_data
import numpy as np
import matplotlib.pyplot as plt

import indicators
# Jaswanth Sai Pyneni
# jpyneni3

class ManualStrategy(object):
    def __init__(self):
        self
    def testPolicy(self, symbol = "AAPL", sd =dt.datetime(2010,1,1), ed =dt.datetime(2011,12,31), sv = 100000):
        stockDF = get_data([symbol], pd.date_range(sd, ed))
        stockDF = stockDF[symbol]
        stockDF = stockDF/stockDF.iloc[0]

        df_trades = pd.DataFrame(np.nan, columns=['Date','Symbol', 'Order', 'Shares'], index=stockDF.index)
        df_trades['Date'] = stockDF.index
        df_trades['Symbol'] = symbol
        df_trades['Shares'] = 0
        df_trades['Order'] = "HOLD"

        bbandDF = indicators.b_bands(stockDF, 20)
        macdDF = indicators.macd(stockDF)
        # posDF = indicators.priceoversma(stockDF, 20)
        exitflag = False
        enterflag = False
        # tsi = indicators.tsi(stockDF)




        currholdings = 0
        prev_date = sd
        prev_date = pd.to_datetime(str(prev_date))
        prev_date = prev_date.strftime('%Y-%m-%d')
        for i in stockDF.index.values:
            date = pd.to_datetime(str(i))
            date = date.strftime('%Y-%m-%d')
            price = stockDF.loc[date]
            upper =  bbandDF.loc[date, 'UPPER']
            lower =  bbandDF.loc[date, 'LOWER']
            macd = macdDF.loc[date]
        

            if price >= upper and exitflag == False and macdDF.loc[prev_date] > 0:
                exitflag = True
            elif price <= upper and exitflag == True and macd < 0 and macdDF.loc[prev_date] > 0:
                exitflag = False
                if currholdings == 1000:
                    df_trades.loc[date, 'Order'] = 'SELL'
                    df_trades.loc[date, "Shares"] = 2000
                if currholdings == 0:
                    df_trades.loc[date, 'Order'] = 'SELL'
                    df_trades.loc[date, "Shares"] = 1000
                currholdings = -1000
            elif price <= lower and enterflag == False:
                enterflag = True
            elif price >=lower and enterflag == True and macd > 0 and macdDF.loc[prev_date] < 0:
                enterflag = False
                if currholdings == -1000:
                    df_trades.loc[date, 'Order'] = 'BUY'
                    df_trades.loc[date, "Shares"] = 2000
                if currholdings == 0:
                    df_trades.loc[date, 'Order'] = 'BUY'
                    df_trades.loc[date, "Shares"] = 1000
                currholdings = 1000


            prev_date = date









        return df_trades

if __name__=="__main__":
    ms = ManualStrategy()
    print "In Sample"
    df_trades = ms.testPolicy("NFLX", dt.datetime(2003,1,1), dt.datetime(2004,12,31), 100000)
    print "Out of Sample"
    df_trades2 = ms.testPolicy("NFLX", dt.datetime(2005, 1, 1), dt.datetime(2006, 12, 31), 100000)
