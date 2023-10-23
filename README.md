Replaced pandas-ta calls with numpy/numba functions to speed up the calculation of EMA, TEMA, RSI, MFI, Plus_DI, Minus_DI, ADX, DPO indicators.

Improved with ChatGPT 4 (free from Bing) and ChatGPT 3.5.

Removed pd.series from the MFI function code, using numba for speedup in TEMA calculation.

Implemented a check to quickly determine if the dataframe read from the CSV file is empty or not.

The ADX code was inspired by https://medium.com/codex/does-combining-adx-and-rsi-create-a-better-profitable-trading-strategy-125a90c36ac. The ADX code was optimized for speed using numba with the assistance of ChatGPT. Some parts were adapted from https://www.quora.com/How-do-we-calculate-ADX-in-Python-for-backtesting and https://stackoverflow.com/questions/63020750/how-to-find-average-directional-movement-for-stocks-using-pandas. RSI, TEMA, MFI, DPO, Plus_DI, Minus_DI, and ADX outputs precisely match those calculated on investing.com. I am proud of the improvements made to the existing code with ChatGPT.

The RSI numba code was copied from https://github.com/boonteck/tech_inds.

Why did I make these changes? I work with 376 instruments from the XU100 market. I calculate indicators in 15m, 30m, 1h, 2h, 3h, 4h, 1day, 1week, and 1month periods in each run. When I upgraded the pandas library to version 2.1.1 to speed up the process, pandas_ta's MFI function caused an error, which I couldn't resolve. So, I decided to convert pandas_ta calls to numpy functions and, if faster, to numba calls. Interestingly, not all numpy subroutines became faster with numba, but I achieved significant improvement. The entire program now finishes in 45 seconds instead of 117 seconds on an Intel E7500 Windows PC, and in 12.7 seconds instead of 33 seconds on an AMD 5700X Windows PC. This represents a 2,5x improvement in the complete Python program.

I attempted, used, and ultimately abandoned the idea of installing the executable TA-Lib on my machines: https://github.com/TA-Lib/ta-lib-python and https://ta-lib.org/install/.

I'm happy to report that all of my code consists of 486 lines. It has minimal dependencies on pandas. I prefer to copy pandas series from data frames to numpy arrays, which results in faster calculations. If you have only a few symbols to calculate, you may not expect significant improvement. On the contrary, execution time may increase, for example, from 2 seconds to 4 seconds.
