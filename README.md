# pandas-ta-2-numba
replaced pandas-ta calls with numpy/numba functions to speed up calculating ema, tema, rsi, mfi, adx indicators

improved with chatgpt 4 (in bing chat) and ChatGPT 3.5

mfi function->removed pd.series from code, 

using numba for speedup: tema, check if df red from csv is empty

adx code inspired by: https://medium.com/codex/does-combining-adx-and-rsi-create-a-better-profitable-trading-strategy-125a90c36ac
adx code speed up by numba with the help of chatGPT, parts are copied from: https://www.quora.com/How-do-we-calculate-ADX-in-Python-for-backtesting and from https://stackoverflow.com/questions/63020750/how-to-find-average-directional-movement-for-stocks-using-pandas
outputs precisely same results as investing.com, so I'm very proud of impreving existing code with ChatGPT

rsi numba code copied and used from: https://github.com/boonteck/tech_inds

why?
I have 376 instruments from xu100 market. I calculate indicators for my strategy in 15m, 30m, 1h, 2h, 4h, 3h, 4h, 1day, 1week, 1month intervals.
When I upgraded panda to 2.1.1 to speed things a little, pandas_ta's mfi function raised error, and I couln't fix the error. So I decided to convert pandas_ta calls to numpy functions, and if runs better to numba calls.
I got significant improvement. whole program finishes in 42 secons instead of 117 secons on an intel e7500 windows pc, and 13,5 seconds instead od 40 seconds on an amd 5700x windows pc.
3x improvement on 475 lines of complete python program

I tried, used, and gave up installing executable ta lib on my machines:
https://github.com/TA-Lib/ta-lib-python
https://ta-lib.org/install/

All of my code resides in 475 lines, I'm happy.
It's minimally dependent upon pandas. if possible, copies pandas series of data frame to numpy arrays, and calculates faster.
If you have few stocks to calculate, you may not expect a significant improvement. on the contrary execution time may increase, for example from 2 seconds to 4 seconds.
