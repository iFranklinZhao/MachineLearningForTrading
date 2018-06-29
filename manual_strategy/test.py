from marketsimcode import compute_portvals
import pandas as pd
from util import get_data, plot_data
import matplotlib.pyplot as plt
import datetime as dt
import BestPossibleStrategy as bps

if __name__=="__main__":
    trades = bps.BestPossibleStrategy()
    df_trades = trades.testPolicy()
    # print df_trades
    # print "________________________________________________"
    # print compute_portvals(df_trades, start_val = 100000, commission = 0, impact = 0)
