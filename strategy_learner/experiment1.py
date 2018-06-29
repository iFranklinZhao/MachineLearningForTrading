import datetime as dt
import pandas as pd
import util as ut
import random
import numpy as np

import indicators
import QLearner as Q
from marketsimcode import compute_portvals, port_val_stats
import ManualStrategy as manstrat
import StrategyLearner as learnerstrat
import matplotlib.pyplot as plt
# Jaswanth Sai Pyneni
# jpyneni3
def run():
    # Strategy Learner trades dataframe
    sl = learnerstrat.StrategyLearner()
    sl.addEvidence(symbol = "NFLX", sd=dt.datetime(2003,1,1), ed=dt.datetime(2004,12,31), sv = 100000) # training phase)
    sldf_trades = sl.testPolicy(symbol = "NFLX", sd=dt.datetime(2003,1,1), ed=dt.datetime(2004,12,31), sv = 100000)
    sldf_trades["Symbol"] = 'NFLX'
    sldf_trades["ORDER"] = 'HOLD'
    sldf_trades.loc[sldf_trades["Shares"] < 0, "Order"] = 'SELL'
    sldf_trades.loc[sldf_trades["Shares"] > 0, "Order"] = 'BUY'
    # sldf_trades = sldf_trades[sldf_trades["Shares"] != 0]
    sldf_trades["Date"] = sldf_trades.index
    sldf_trades = sldf_trades[["Date","Symbol", "Order", "Shares"]]
    sldf_trades["Shares"] = sldf_trades["Shares"].abs()
    # print "Strat Learner Trades"
    # print sldf_trades
    portvalSL = compute_portvals(sldf_trades, start_val=100000, commission=0.0, impact=0.0)
    print "Strategy Learner----------------------"
    port_val_stats(portvalSL)
    portvalSL = portvalSL/portvalSL.iloc[0]
    portvalSL = portvalSL.rename("Strategy Leaner")
    print



    # Manual Strategy trades dataframe
    ms = manstrat.ManualStrategy()
    msdf_trades = ms.testPolicy("NFLX", dt.datetime(2003,1,1), dt.datetime(2004,12,31), 100000)
    # msdf_trades = msdf_trades[msdf_trades["Shares"] != 0]
    # print "Manual Strat Trades"
    # print msdf_trades
    portvalMS = compute_portvals(msdf_trades, start_val=100000, commission=0.0, impact=0.0)
    print "Manual Strategy-------------------------------------------------"
    port_val_stats(portvalMS)
    portvalMS = portvalMS/portvalMS.iloc[0]
    portvalMS = portvalMS.rename("Manual Strategy")
    print
    #
    #
    # Benchmark trades dataframe
    stockDF = ut.get_data(["NFLX"], pd.date_range(dt.datetime(2003,1,1), dt.datetime(2004,12,31)))
    stockDF = stockDF["NFLX"]
    stockDF = stockDF/stockDF.iloc[0]
    benchmark_trades = pd.DataFrame(np.nan, columns=['Date','Symbol', 'Order', 'Shares'], index=stockDF.index)
    benchmark_trades['Date'] = stockDF.index
    benchmark_trades['Symbol'] = "NFLX"
    benchmark_trades['Shares'] = 0
    benchmark_trades['Order'] = "HOLD"
    benchmark_trades.iloc[0,2] = "BUY"
    benchmark_trades.iloc[0,3] = 1000
    # print benchmark_trades
    portvalBM = compute_portvals(benchmark_trades, start_val=100000, commission=0.0, impact=0.0)
    print "Benchmark-------------------------------------------------"
    port_val_stats(portvalBM)
    portvalBM = portvalBM/portvalBM.iloc[0]
    portvalBM = portvalBM.rename("Benchmark")
    print

    # print portvalSL
    psv = portvalMS.plot(legend = True, y = "Cumulative Returns", x = "Dates", color = "black")
    bm = portvalBM.plot(ax=psv, title = "Cumulative Returns of NFLX", legend = True, color="blue")
    msv = portvalSL.plot(ax=psv, title = "Cumulative Returns of NFLX", legend = True, color="red")

    plt.ylabel("Cumulative Return")
    plt.xlabel("Dates")
    plt.show()


if __name__=="__main__":
    run()
