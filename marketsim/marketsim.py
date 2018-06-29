"""MC2-P1: Market simulator.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved

Jaswanth Sai Pyneni
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    ordDF = pd.read_csv(orders_file)
    start_date = min(ordDF['Date'])
    end_date = max(ordDF['Date'])

    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    returnDF = get_data(['SPY'], pd.date_range(start_date, end_date))
    returnDF['Cash Value'] = 0
    cash_val = start_val

    for i in returnDF.index.values:
        date = pd.to_datetime(str(i))
        date = date.strftime('%Y-%m-%d')

        if date in ordDF['Date'].values:

            for j in ordDF[ordDF['Date'] == date].index.values:

                curStock = ordDF.iloc[j]['Symbol']
                if curStock not in returnDF:
                    returnDF[curStock] = get_data([curStock], pd.date_range(start_date, end_date))[curStock]
                    returnDF['# of ' +str(curStock)] = 0
                numShares = ordDF.iloc[j]['Shares']
                price = returnDF.loc[date, curStock]
                valToday = price * numShares
                impact_penalty = impact * valToday
                order = ordDF.iloc[j]['Order']
                if order == 'BUY':
                    cash_val = cash_val - valToday - impact_penalty - commission
                    returnDF.loc[date:,'# of ' +str(curStock)] += numShares

                if order == 'SELL':
                    cash_val = cash_val + valToday - impact_penalty - commission
                    returnDF.loc[date:,'# of ' +str(curStock)] -= numShares



        #print cash_val
        returnDF.loc[date, 'Cash Value'] = cash_val
    indices = []
    for x in range(2, returnDF.shape[1] -1, 2):
        indices.append(x)
    scol = returnDF.ix[:, indices]
    print scol.shape
    ncol = returnDF.ix[:, [x+1 for x in indices]]
    print ncol.shape
    sxncol = pd.DataFrame(scol.values*ncol.values, columns =scol.columns, index = scol.index)
    returnDF['Portfolio Value'] = sxncol.sum(axis=1) + returnDF['Cash Value']



    return returnDF['Portfolio Value']

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-05.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
