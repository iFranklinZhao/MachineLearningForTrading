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

def run(i=0):
    sl = learnerstrat.StrategyLearner(impact=i)
    sl.addEvidence(symbol = "NFLX", sd=dt.datetime(2003,1,1), ed=dt.datetime(2004,12,31), sv = 100000) # training phase)
    sldf_trades = sl.testPolicy(symbol = "NFLX", sd=dt.datetime(2003,1,1), ed=dt.datetime(2004,12,31), sv = 100000)
    # print sldf_trades
    sldf_trades["Symbol"] = 'NFLX'
    sldf_trades["Count sell"] = 0
    sldf_trades["Count buy"] = 0
    sldf_trades.loc[sldf_trades["Shares"] < 0, "Order"] = 'SELL'
    sldf_trades.loc[sldf_trades["Shares"] > 0, "Order"] = 'BUY'
    sldf_trades.loc[sldf_trades["Order"] == "BUY", "Count buy"] = 1
    sldf_trades.loc[sldf_trades["Order"] == "SELL", "Count sell"] = 1
    countsell = sldf_trades.loc[:, "Count sell"].sum()
    countbuy = sldf_trades.loc[:, 'Count buy'].sum()
    count = countbuy + countsell

    # sldf_trades = sldf_trades[sldf_trades["Shares"] != 0]
    sldf_trades["Date"] = sldf_trades.index
    sldf_trades = sldf_trades[["Date","Symbol", "Order", "Shares"]]
    sldf_trades["Shares"] = sldf_trades["Shares"].abs()
    # print "Strat Learner Trades"
    # print sldf_trades
    portvalSL = compute_portvals(sldf_trades, start_val=100000, commission=0.0, impact=i)
    print "Number of sell trades = {}".format(countsell)
    print "Number of buy trades = {}".format(countbuy)
    print "Number of total trades = {}".format(count)

    port_val_stats(portvalSL)
    portvalSL = portvalSL/portvalSL.iloc[0]
    portvalSL = portvalSL.rename("Strategy Leaner")




    psv = portvalSL.plot(legend = True, y = "Cumulative Returns", x = "Dates", color = "black")


if __name__=="__main__":
   for n in np.arange(0, .25, .05):
       for i in range(0,7):
           print "Test {} with impact={}".format(i+1, n)
           run(i=n)
           print
