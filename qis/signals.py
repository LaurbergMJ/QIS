import pandas as pd 
import numpy as np 

def momentum(price: pd.Series, lookback: int, mode: str = "long_flat") -> pd.Series:
    mom = price / price.shift(lookback) - 1.0

    if mode == "long_flat":
        return (mom > 0).astype(float)
    if mode == "long_short":
        return np.sign(mom).replace(0, 0.0).astype(float)
    raise ValueError(f"Unknown mode: {mode}")

def momentum_ensemble(price: pd.Series, lookbacks: list[int], mode: str) -> pd.Series:
    sigs = [momentum(price, lb, mode=mode) for lb in lookbacks]
    s = pd.concat(sigs, axis=1).mean(axis=1)

    if mode == "long_flat":
        return (s > 0.5).astype(float)
    return s.clip(-1.0, 1.0)

    