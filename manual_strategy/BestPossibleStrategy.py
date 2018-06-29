from marketsimcode import compute_portvals, port_val_stats
import datetime as dt
import pandas as pd
from util import get_data, plot_data
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')

class BestPossibleStrategy(object):
    def __init__(self):
        self
    def testPolicy(self, symbol = "AAPL", sd =dt.datetime(2010,1,1), ed =dt.datetime(2011,12,31), sv = 100000):
        stockDF = get_data([symbol], pd.date_range(sd, ed))
        stockDF = stockDF[symbol]
        stockDF = stockDF - stockDF.shift(-1)
        df_trades = pd.DataFrame(np.nan, columns=['Date','Symbol', 'Order', 'Shares'], index=stockDF.index)
        df_trades['Date'] = stockDF.index
        df_trades['Symbol'] = symbol
        df_trades['Shares'] = 0
        df_trades['Order'] = "HOLD"

        currholdings = 0
        for i in stockDF.index.values:
            date = pd.to_datetime(str(i))
            date = date.strftime('%Y-%m-%d')
            if stockDF[i] > 0:
                if currholdings == 1000:
                    df_trades.loc[date, 'Order'] = 'SELL'
                    df_trades.loc[date, "Shares"] = 2000
                if currholdings == 0:
                    df_trades.loc[date, 'Order'] = 'SELL'
                    df_trades.loc[date, "Shares"] = 1000
                currholdings = -1000
            if stockDF[i] < 0:
                if currholdings == -1000:
                    df_trades.loc[date, 'Order'] = 'BUY'
                    df_trades.loc[date, "Shares"] = 2000
                if currholdings == 0:
                    df_trades.loc[date, 'Order'] = 'BUY'
                    df_trades.loc[date, "Shares"] = 1000
                currholdings = 1000
        df_trades2 = df_trades.copy()
        df_trades2['Order'] = "HOLD"
        df_trades2.iloc[0,2] = "BUY"
        df_trades2.iloc[0,3] = 1000
        benchmark = compute_portvals(df_trades2, start_val = 100000, impact = 0, commission =0)
        port_val  = compute_portvals(df_trades, start_val = 100000, impact = 0, commission =0)
        port_val_stats(port_val)
        port_val_stats(benchmark)
        port_val = port_val/port_val.iloc[0]
        benchmark = benchmark/benchmark.iloc[0]
        port_val = port_val.rename("Best Strategy")
        benchmark = benchmark.rename("Benchmark")
        pv = port_val.plot(legend = True, y = "Cumulative Return", x = "Dates", color="black")
        benchmark.plot(ax=pv, title = "Daily Returns of " + str(symbol), legend = True, color="blue")
        plt.ylabel("Cumulative Return")
        plt.xlabel("Dates")
        plt.show()




        return df_trades

if __name__=="__main__":
    bps = BestPossibleStrategy()
    print "In Sample------------------"
    df_trades = bps.testPolicy("NFLX", dt.datetime(2003,1,1), dt.datetime(2004,12,31), 100000)
    # print "Out of Sample-------------"
    # df_trades = bps.testPolicy("NFLX", dt.datetime(2005, 1, 1), dt.datetime(2006, 12, 31), 100000)
