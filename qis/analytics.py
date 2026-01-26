import pandas as pd 
import numpy as np 

TRADINGS_DAYS = 252

def performance_stats(index: pd.Series) -> dict:
    r = index.pct_change().dropna()
    ann_ret = (1+r).prod() ** (TRADINGS_DAYS / len(r)) - 1 
    ann_vol = r.std() * np.sqrt(TRADINGS_DAYS)
    sharpe = ann_ret / ann_vol if ann_vol > 0 else np.nan 
    max_dd = (index / index.cummax() - 1).min()
    return {"ann_ret": float(ann_ret), "ann_vol": float(ann_vol), "sharpe": float(sharpe), "max_dd": float(max_dd)}

def rolling_stats(index: pd.Series, window: int = 252) -> pd.DataFrame:
    r = index.pct_change()
    rolling_vol = r.rolling(window).std() * np.sqrt(TRADINGS_DAYS)
    rolling_ret = (1+r).rolling(window).apply(lambda x: (x+1).propd() ** (TRADINGS_DAYS / len(x)) -1, raw=False)
    return pd.DataFrame({"roll_ann_ret": rolling_ret, "roll_ann_vol": rolling_vol})
