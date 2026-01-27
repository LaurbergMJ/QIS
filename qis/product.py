import pandas as pd 
import numpy as np 

def capital_protected_participation(index: pd.Series, protection: float = 1.0, participation: float=1.0) -> dict:
    """
    Toy: payoff at maturity = protection + participation * max(0, I_T / I_0 -1)
    Return: payoff multiple (e.g. 1.15 = +15%)
    """
    i0 = float(index.iloc[0])
    iT = float(index.iloc[-1])
    performance = iT /i0 - 1.0 
    payoff = protection + participation * max(0.0, performance)
    return {"i0": i0, "iT": iT, "performance": float(performance), "payoff_multiple": float(payoff)}

