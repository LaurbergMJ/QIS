import pandas as pd 
import numpy as np 

def compute_index(ret: pd.Series, w_exec: pd.Series, total_cost: pd.Series, base: float = 100.0) -> pd.Series:
    r = ret.fillna(0.0).to_numpy()
    w_lag = w_exec.shift(1).fillna(0.0).to_numpy()
    c = total_cost.fillna(0.0).to_numpy()

    idx = np.zeros(len(ret))
    idx[0] = base
    for t in range(1, len(ret)):
        idx[t] = idx[t-1] * (1.0 + w_lag[t] * r[t] -c[t])

    return pd.Series(idx, index=ret, name="index")

    
 
