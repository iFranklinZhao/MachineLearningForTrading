# Strategy Learner

In this project I designed a Q-Learning trading agent that uses numerical/technical indicators of a stock on each day as the state, stock position change as the action, and stock performance as the reward. <br>


|  File Name | Purpose |
|-----|-------------------|
| StrategyLearner.py | My code implementing a learner that learns a trading policy using my Q-Learner|
| Qlearner.py | My code that has my QLearner from the previous project|
| ManualStrategy.py | My code with my manual strategy from earlier to compare with the QLearner Strategy as outlined in my report |
| marketsimcode.py| My marketsimcode from earlier to evaluate and compare how each of the strategies perform  |

The benchmark that both strategies had to beat was investing long on the first day of trades and holding until the last day. <br>



Experiment One: <br>
  Results outlined in my report. For experiment one I compared my manual strategy performance against the performance of the QLearner strategy. <br>

Experiment Two: <br>
  For experiment two I tested the affects of impact value on my Qlearner strategy <br>
