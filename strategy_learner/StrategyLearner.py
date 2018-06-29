"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
# Jaswanth Sai Pyneni
# jpyneni3
"""
# Jaswanth Sai Pyneni
# jpyneni3

import datetime as dt
import pandas as pd
import util as ut
import random
import numpy as np

import indicators
import QLearner as Q
import warnings
warnings.filterwarnings("ignore")
# pd.options.display.max_rows = 999

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.QL = Q.QLearner(num_states=100, num_actions=3, alpha=0.2, gamma=0.9, rar=0.5, radr=0.99, dyna=0, verbose=False)

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):


        # add your code to do learning here
        stockDF = ut.get_data([symbol], pd.date_range(sd, ed))
        stockDF = stockDF[symbol]
        stockDF = stockDF/stockDF.iloc[0]
        PC = (stockDF/stockDF.shift(1)) - 1

        # print stockDF

        #print PC
        # example usage of the old backward compatible util function
        # syms=[symbol]
        # dates = pd.date_range(sd, ed)
        # prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        # prices = prices_all[syms]  # only portfolio symbols
        # prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        # if self.verbose: print prices
        #
        # # example use with new colname
        # volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        # volume = volume_all[syms]  # only portfolio symbols
        # volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        # if self.verbose: print volume

        bbandDF = indicators.b_bands(stockDF, 20) #test with min_periods = 0 in SMA
        bbandDF["BBP"] = ((bbandDF[symbol]-bbandDF["LOWER"])/(bbandDF["UPPER"]-bbandDF["LOWER"]))
        bbandDF = bbandDF["BBP"]
        macdDF = indicators.macd(stockDF)

        inds = pd.concat([bbandDF, macdDF], axis = 1)
        inds = inds.dropna()
        inds = self.discretize(inds)



        df_trades = pd.DataFrame(np.nan, columns=['Date','Symbol', 'Order', 'Shares'], index=stockDF.index)
        df_trades['Date'] = stockDF.index
        df_trades['Symbol'] = symbol
        df_trades['Shares'] = 0
        df_trades['Order'] = "HOLD"
        currholdings = 0
        reward = 0
        # print (int(float(inds.iloc[0])))
        # print "----------------------------"
        # print inds.max()
        # print inds.min()

        self.QL.querysetstate(int(float(inds.iloc[0])))

        dft_copy = df_trades.copy()
        converged = False
        epochCount = 0
        stockDF.dropna()
        # print inds
        while not converged:
            epochCount +=1
            currholdings = 0
            # reward = 0

            if(epochCount > 500):
                break

            dft_copy = df_trades.copy()

            for i in inds.index.values:
                # print "hit"
                date = pd.to_datetime(str(i))
                date = date.strftime('%Y-%m-%d')
                # print PC.loc[date].values

                reward = (currholdings * PC.loc[date]*(1-self.impact))
                # print (int(float(inds.loc[date])))
                action = self.QL.query((int(float(inds.loc[date]))), reward)
                # print action
                # print action
                if action == 2: #sell
                    if currholdings == 1000:
                        df_trades.loc[date, 'Order'] = 'SELL'
                        df_trades.loc[date, "Shares"] = -2000
                        currholdings = -1000
                    if currholdings == 0:
                        df_trades.loc[date, 'Order'] = 'SELL'
                        df_trades.loc[date, "Shares"] = -1000
                        currholdings = -1000
                elif action == 1: #buy
                    if currholdings == -1000:
                        df_trades.loc[date, 'Order'] = 'BUY'
                        df_trades.loc[date, "Shares"] = 2000
                        currholdings = 1000
                    if currholdings == 0:
                        df_trades.loc[date, 'Order'] = 'BUY'
                        df_trades.loc[date, "Shares"] = 1000
                        currholdings = 1000


            if(dft_copy.equals(df_trades) and epochCount > 10):
                converged = True

        df_trades = pd.DataFrame(np.nan, columns=['Date','Symbol', 'Order', 'Shares'], index=stockDF.index)
        df_trades['Date'] = stockDF.index
        df_trades['Symbol'] = symbol
        df_trades['Shares'] = 0
        df_trades['Order'] = "HOLD"


        # print self.QL.Q
        # print df_trades


    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        stockDF = ut.get_data([symbol], pd.date_range(sd, ed))
        stockDF = stockDF[symbol]
        stockDF = stockDF/stockDF.iloc[0]
        # print stockDF
        PC = (stockDF/stockDF.shift(1)) - 1
        # print PC

        bbandDF = indicators.b_bands(stockDF, 20) #test with min_periods = 0 in SMA
        bbandDF["BBP"] = ((bbandDF[symbol]-bbandDF["LOWER"])/(bbandDF["UPPER"]-bbandDF["LOWER"]))
        bbandDF = bbandDF["BBP"]
        macdDF = indicators.macd(stockDF)

        inds = pd.concat([bbandDF, macdDF], axis = 1)
        inds = inds.dropna()
        inds = self.discretize(inds)


        df_trades = pd.DataFrame(np.nan, columns=['Date','Symbol', 'Order', 'Shares'], index=stockDF.index)
        df_trades['Date'] = stockDF.index
        df_trades['Symbol'] = symbol
        df_trades['Shares'] = 0
        df_trades['Order'] = "HOLD"
        currholdings = 0



        self.QL.rar = 0
        for i in inds.index.values:
            # print "hit"
            date = pd.to_datetime(str(i))
            date = date.strftime('%Y-%m-%d')

            # print reward
            action = self.QL.querysetstate((int(float(inds.loc[date]))))
            # print action
            # print action
            if action == 2: #sell
                if currholdings == 1000:
                    df_trades.loc[date, 'Order'] = 'SELL'
                    df_trades.loc[date, "Shares"] = -2000
                    currholdings = -1000
                if currholdings == 0:
                    df_trades.loc[date, 'Order'] = 'SELL'
                    df_trades.loc[date, "Shares"] = -1000
                    currholdings = -1000
            elif action == 1: #buy
                if currholdings == -1000:
                    df_trades.loc[date, 'Order'] = 'BUY'
                    df_trades.loc[date, "Shares"] = 2000
                    currholdings = 1000
                if currholdings == 0:
                    df_trades.loc[date, 'Order'] = 'BUY'
                    df_trades.loc[date, "Shares"] = 1000
                    currholdings = 1000
        # print df_trades["Shares"]
        # print df_trades
        df_trades = df_trades.drop('Symbol', axis=1)
        df_trades = df_trades.drop('Order', axis=1)
        df_trades = df_trades.drop('Date', axis=1)
        # print df_trades
        return df_trades

    def discretize(self, inds):
        # print inds
        bbpmin = inds.iloc[:, 0].min()
        bbpmax = inds.iloc[:, 0].max()
        bbpbins = np.arange(bbpmin, bbpmax, ((bbpmax-bbpmin)/10)).tolist()
        bbpbins.append(bbpmax)
        groups = []
        for i in range(0, 10):
            groups.append(i)

        inds["BBState"] = pd.cut(inds["BBP"], bbpbins, labels=groups)
        inds["MACDState"] = inds["MACD"]
        inds.loc[inds["MACDState"] > 0, "MACDState"] = 1
        inds.loc[inds["MACDState"] < 0, "MACDState"] = -1
        # print inds['MACDState']
        inds["MACDState"] = inds["MACDState"] - inds["MACDState"].shift(1)
        inds["MACDState"] += 2
        # print inds["MACDState"]
        # print inds['MACDState']
        inds = inds.dropna()
        inds["state"] = inds["BBState"].astype(int).astype(str) + inds["MACDState"].astype(int).astype(str)
        inds = inds["state"]
        # print inds
        return inds




if __name__=="__main__":
    sl = StrategyLearner()
    sl.addEvidence()
    trades = sl.testPolicy()
    # trades2 = sl.testPolicy()
    # if (trades2.equals(trades)):
    #     print "pass"
    print "One does not simply think up a strategy"
