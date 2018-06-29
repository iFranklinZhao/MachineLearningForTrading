import pandas as pd
import matplotlib as matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from util import get_data, plot_data



def getsma(data, n=5):
    sma = data.rolling(window = n, min_periods=0).mean()
    band = data.rolling(window = n).std()
    return sma, band

def getema(data, n=5):
    ema = data.ewm(span=n, min_periods=0, adjust=False).mean()
    return ema

def b_bands(data, n=5):
    prices = data/data.iloc[0]
    sma, band = getsma(prices,n)
    upper = sma + 2 * band
    lower = sma - 2 * band
    bband_df = pd.concat([prices, sma.rename("SMA"), upper.rename("UPPER"), lower.rename("LOWER")], axis = 1)
    # plot_data(bband_df, title="Bollinger Bands")
    return bband_df

def priceoversma(data, n=5):
    prices = data/data.iloc[0]
    sma, band = getsma(prices,n)
    pos = prices/sma
    pos = pos.rename("Price Over SMA")
    pos_df = pd.concat([prices, sma.rename("SMA"), pos.rename("PRICE/SMA")], axis =1)
    ax = pos.plot(title="Price Over SMA", fontsize=12, legend=True )
    ax.axhline(y=1, color="black", label="Signal")
    ax.legend()
    plt.draw()
    # plt.show()
    return pos_df

def macd(data):
    prices = data/data.iloc[0]
    ema26 = getema(prices, n=26)
    ema12 = getema(prices, n=12)
    macd = ema26 - ema12
    signal = getema(prices, n=9)
    macd = macd.rename("MACD")
    macd_df = pd.concat([macd.rename("MACD"), signal.rename("EMA9 Signal")], axis=1)
    ax = macd_df.plot(title="MACD", fontsize=12, legend=True)
    ax.set_ylabel("MACD")
    ax.axhline(y=0, color="black", label="Signal")
    ax.legend()
    plt.show()
    return macd

# def aroon(data, n=25):
#     prices = data/data.iloc[0]
#     max = prices.rolling(window = n, min_periods = 1).max()
#     min = prices.rolling(window = n).min()
#
#     print prices
#     print max
def tsi(data):
    prices = data/data.iloc[0]
    # sma, b = getsma(prices, 9)
    sma, b = getsma(data, 9)

    pc = prices.diff()
    fs = getema(pc, 25) #first smooth
    ss = getema(fs, 13) #second smooth


    abspc = prices.diff().abs()
    afs = getema(abspc, 25) #first smooth absolute value
    ass = getema(afs, 13) #second smooth absolute value

    TSI = (ss.div(ass) * 100).rename("TSI")


    # tsi = pd.concat([sma.rename("SMA Signal"), TSI.rename("TSI")], axis = 1)
    ax = TSI.plot(title="True Strength Index", fontsize=12, legend= True)
    ax.set_xlabel("Dates")
    ax.set_ylabel("TSI")
    ax.axhline(y=0, color="black", label="Zero Signal")
    ax.legend()
    plt.show()

    return TSI




def test_code():
    plt.ion()
    start_date = dt.datetime(2003,1,1)
    end_date = dt.datetime(2004,12, 31)
    stockDF = get_data(['NFLX'],pd.date_range(start_date, end_date))
    stockDF = stockDF['NFLX']
    b_bands(stockDF, 20)
    priceoversma(stockDF, 20)
    macd(stockDF)
    tsi(stockDF)


if __name__ == "__main__":
    test_code()
