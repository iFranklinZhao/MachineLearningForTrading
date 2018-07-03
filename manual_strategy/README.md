# Manual Strategy

In this project, I developed a trading strategy based on technical analysis and compared it against the optimal strategy by running both through my market simulator and analyzing the outcomes.


|  File Name | Purpose |
|-----|-------------------|
| indicators.py | My code implementing indicators as functions that take in dataframes|
| marketsimcode.py | My code that improves on the last marketsim by accepting a trades data frame instead of a csv file |
| ManualStrategy.py | My code implementing my manual strategy based on my technical analysis as outlined in my report |
| BestPossibleStrategy.py| My code implementing the optimal policy by looking ahead each day and deciding on the position to take, as outlined in my report |

<br>

indicators.py: <br>
    by running "python indicators.py", you should be able to see the output for: <br>
        -Bollinger Bands (with SMA20) --> to change sma, pass in different number in b_bands(stockDF,n) <br>
        -Price SMA Ratio (SMA20) <br>
        -Moving Average Convergence Divergence <br>
        -True Strength Index <br>
The default is NFLX from 1/1/2003 to 12/31/2004. Dates can be changed in test_code() <br>


BestPossibleStrategy: <br>
    by running "python BestPossibleStrategy.py", you should be able to get: <br>
        -Cumulative returns chart for NFLX over in sample period for best possible strategy <br>
        -Benchmark for NFLX over in sample period <br>
        -Portfolio statistics (portfolio value, Sharpe Fund, Cumulative returns, standard deviation of fun, and average daily return of fund) for benchmark and best possible Strategy
   to run with different stock and dates, just call bps.testPolicy() with right parameters in the __main__ <br>

 ManualStrategy: <br>
    by running "python ManualStrategy.py" you should get: <br>
    -Cumulative returns chart for NFLX over in sample period for manual strategy <br>
    -Benchmark for NFLX over in sample period <br>
    -Cumulative returns chart for NFLX over out of sample period for manual strategy <br>
    -Benchmark for NFLX over out of sample period <br>
    -portfolio statistics for benchmark and manual strategy in and out of sample
    to run with different stock and dates, just call ms.testPolicy() with right parameters in the __main__ <br>
