import pandas as pd 
import numpy as np 

TRADING_DAYS = 252 

def ewma_vol(ret: pd.Series, lam: float = 0.94) -> pd.Series:
    r = ret.fillna(0.0)
    var = np.zeros(len(r))
    var[0] = r.iloc[:20].var() if len(r) > 20 else r.var()
    for i in range(1, len(r)):
        var[i] = lam * var[i-1] + (1-lam) * (r.iloc[i-1] **2)
    return pd.Series(np.sqrt(var), index=r.index)

def vol_target_leverage(vol_d: pd.Series, target_vol: float, max_leverage: float) -> pd.Series:
    vol_a = vol_d * np.sqrt(TRADING_DAYS)
    lev = (target_vol / vol_a.replace(0, np.nan)).clip(0.0, max_leverage)
    return lev.fillna(0.0)

