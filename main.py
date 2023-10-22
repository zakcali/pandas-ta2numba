import pandas as pd
import numpy as np
from numba import jit

TEMA_HIGH_PERIOD = 120
TEMA_LOW_PERIOD = 35
RSI_PERIOD = 14
ADX_PERIOD = 21
MFI_PERIOD = 14
DPO_PERIOD = 21

def calculate_true_range(high, low, close):
    high_low = high - low
    high_close_prev = np.abs(high - np.roll(close, 1))
    low_close_prev = np.abs(low - np.roll(close, 1))
    tr = np.maximum(high_low, high_close_prev)
    tr = np.maximum(tr, low_close_prev)
    return tr


@jit(nopython=True)
def calculate_ewma(data, period):
    ema = np.empty_like(data)
    ema[0] = data[0]
    alpha = 1.0 / (period)
    for i in range(1, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
    return ema


def calculate_adx(high, low, close, period=14):
    epsilon = 1e-10  # Small epsilon value to avoid division by zero
    tr = calculate_true_range(high, low, close)
    atr = calculate_ewma(tr, period) + epsilon

    move_up = high - np.roll(high, 1)
    move_down = np.roll(low, 1) - low

    pos_dm = np.where((move_up > move_down) & (move_up > 0), move_up, 0)
    neg_dm = np.where((move_down > move_up) & (move_down > 0), move_down, 0)

    plus_di = 100 * calculate_ewma(pos_dm, period) / atr
    minus_di = 100 * calculate_ewma(neg_dm, period) / atr

    #dx = (np.abs(plus_di - minus_di) / abs(plus_di + minus_di+ epsilon)) * 100
    ##adx = ((np.roll(dx, 1) * (period - 1)) + dx) / period # do not calculate adx to ensure getting same results as investing[dot]com
    #adx_smooth = calculate_ewma(dx, period) #use dx instead of adx to ensure getting same results as investing[dot]com, alternate is: calculate_ewma(adx, period)
    #return plus_di, minus_di, adx_smooth # I don't use adx_smooth, if you need it remove 5 lines of # from beginnig here and up 

    return plus_di, minus_di # if you need adx smooth, replace: return plus_di, minus_di, adx_smooth


@jit(nopython=True)
def calculate_ema(data, period):
    ema = np.empty_like(data)
    ema[0] = data[0]
    alpha = 2.0 / (period + 1)
    for i in range(1, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
    return ema


def calculate_tema(data, period):
    ema1 = calculate_ema(data, period)
    ema2 = calculate_ema(ema1, period)
    ema3 = calculate_ema(ema2, period)
    tema = 3 * ema1 - 3 * ema2 + ema3
    return tema


# Calculate money flow index
def calculate_mfi(high, low, close, volume, period):
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    mf_sign = np.where(typical_price > np.roll(typical_price, shift=1), 1, -1)
    signed_mf = money_flow * mf_sign

    # Calculate gain and loss using vectorized operations
    positive_mf = np.maximum(signed_mf, 0)
    negative_mf = np.maximum(-signed_mf, 0)

    mf_avg_gain = np.convolve(positive_mf, np.ones(period), mode='full')[:len(positive_mf)] / period
    mf_avg_loss = np.convolve(negative_mf, np.ones(period), mode='full')[:len(negative_mf)] / period

    epsilon = 1e-10  # Small epsilon value to avoid division by zero
    mfi = 100 - 100 / (1 + mf_avg_gain / (mf_avg_loss + epsilon))
    return mfi


# Exponential Moving Average
@jit(nopython=True)
def rsi_ema(arr, period, alpha=None):
    if alpha is None:
        alpha = 2 / (period + 1)

    exp_weights = np.zeros(len(arr))
    exp_weights[period - 1] = np.mean(arr[:period])
    for i in range(period, len(exp_weights)):
        exp_weights[i] = exp_weights[i - 1] * (1 - alpha) + alpha * arr[i]
    exp_weights[:period - 1] = np.nan
    return exp_weights

# Relative Strength Index
@jit(nopython=True)
def calculate_rsi(arr, period=21):
    delta = np.diff(arr)
    up, down = np.copy(delta), np.copy(delta)
    up[up < 0] = 0
    down[down > 0] = 0

    # Exponential Weighted windows mean with centre of mass = period - 1 -> alpha = 1 / (period)
    alpha = 1 / period
    rUp = rsi_ema(up, period, alpha=alpha)
    rDown = np.abs(rsi_ema(down, period, alpha=alpha))
    result = 100 - (100 / (1 + rUp / rDown))

    # append nan that was lost in np.diff
    result = np.concatenate((np.array([np.nan]), result))
    return result

def calculate_dpo(close, length, centered=False):
    half_length = length // 2
    shifted_close = np.roll(close, half_length + 1)
    convolved = np.convolve(shifted_close, np.ones(length) / length, mode='full')[:len(shifted_close)]
    dpo_values = close[:(len(convolved))] - convolved
    if centered:
        dpo_values = np.roll(dpo_values, -half_length)
    return dpo_values
        
def calculate_indicator(file_name):
    df = pd.read_csv(file_name)
    len_dfx_index = len(df.index)
    if len_dfx_index == 0:  # faster than if df.empty:
        df_is_empty = True
    else:
        df_is_empty = False
    if df_is_empty:  
        df["MFI"] = np.nan
        df["RSI"] = np.nan
        df["DPO"] = np.nan
    else:
        df["MFI"] = calculate_mfi(high=df["High"].values, low=df["Low"].values, close=df["Close"].values, volume=df["Volume"].values, period=MFI_PERIOD)
        df["RSI"] = calculate_rsi(df["Close"].values, RSI_PERIOD)
        df["DPO"] = calculate_dpo(close=df["Close"].values, length=DPO_PERIOD, centered=False)  # dpo 21
    if len_dfx_index > TEMA_HIGH_PERIOD:  # prevents all NaN error
        df["TEMA_HIGH"] = calculate_tema(df["Close"].values, TEMA_HIGH_PERIOD)
        df["TEMA_LOW"] = calculate_tema(df["Close"].values, TEMA_LOW_PERIOD)
    else:
        df["TEMA_HIGH"] = np.nan
        df["TEMA_LOW"] = np.nan
    if len_dfx_index > ADX_PERIOD:
        tempor = calculate_adx(df["High"].values, df["Low"].values, df["Close"].values, ADX_PERIOD)
        df["PLUS_DI"] = tempor[0]  # plus-di, 21
        df["MINUS_DI"] = tempor[1]  # minus-di, 21
        # df["ADX"] = tempor[2]
    else:
        df["PLUS_DI"] = np.nan
        df["MINUS_DI"] = np.nan
        # df["ADX"] = np.nan
    return df
