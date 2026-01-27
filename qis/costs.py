import pandas as pd 
import numpy as np 

def apply_rebalance_schedule(w_desired: pd.Series, freq: str = "D") -> pd.Series:
    """
    freq: 'D': daily, 'W-FRI': weekly, 'M': month end 
    """

    if freq == "D":
        return w_desired.fillna(0.0)
    
    w = w_desired.copy().fillna(0.0)
    rebalance = w.resample(freq).last()
    w_exec = rebalance.reindex(w.index).ffill().fillna(0.0)
    return w_exec

def transaction_cost(turnover: pd.Series, tc_bps: float) -> pd.Series:
    return (tc_bps / 1e4) * turnover.fillna(0.0)

def slippage_cost(turnover: pd.Series, vol_d: pd.Series, k: float = 0.0) -> pd.Series:
    """
    Simple add-on: slippage increases with volatility regime
    k = tuning parameter (start with 0 and later calibrate)
    """
    return (k * turnover.fillna(0.0) * vol_d.fillna(0.0)).fillna(0.0)

