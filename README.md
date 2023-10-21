# pandas-ta-2-numba
replaced pandas-ta calls with numpy/numba functions to speed up calculating ema, tema, rsi, mfi, plus_di, minus_di, adx, dpo indicators

improved with ChatGPT 4 (free from Bing) and ChatGPT 3.5

mfi function->removed pd.series from code, 

using numba for speedup: tema, check if dataframe read from csv is empty fast

adx code inspired by: https://medium.com/codex/does-combining-adx-and-rsi-create-a-better-profitable-trading-strategy-125a90c36ac
adx code speed up by numba with the help of chatGPT, parts are copied from: https://www.quora.com/How-do-we-calculate-ADX-in-Python-for-backtesting and from https://stackoverflow.com/questions/63020750/how-to-find-average-directional-movement-for-stocks-using-pandas
outputs precisely same results as investing.com, so I'm very proud of impreving existing code with ChatGPT

rsi numba code copied and used from: https://github.com/boonteck/tech_inds

why?
I have 376 instruments from xu100 market. I calculate indicators for my strategy in 15m, 30m, 1h, 2h, 4h, 3h, 4h, 1day, 1week, 1month intervals.
When I upgraded pandas library to 2.1.1 for speeding up things a little, pandas_ta's mfi function raised error, and I couln't fix the error. So I decided to convert pandas_ta calls to numpy functions, and if runs better to numba calls.
I got significant improvement. whole program finishes in 39 secons instead of 117 secons on an intel e7500 windows pc, and 12,75 seconds instead od 33 seconds on an amd 5700x windows pc.
3x improvement on a complete python program

I tried, used, and gave up installing executable ta lib on my machines:
https://github.com/TA-Lib/ta-lib-python and
https://ta-lib.org/install/

All of my code resides in 486 lines, I'm happy.
It's minimally dependent upon pandas. I prefer to copy pandas series of data frame to numpy arrays, and calculations run faster.
If you have few sybols to calculate, you may not expect a significant improvement. on the contrary execution time may increase, for example from 2 seconds to 4 seconds.
