from pathlib import Path 
import pandas as pd 

from qis.config import load_config, make_run_meta
from qis.io import run_dir, save_json, save_parquet
from qis.signals import momentum, momentum_ensemble
from qis.risk import ewma_vol, vol_target_leverage
from qis.costs import apply_rebalance_schedule, transaction_cost, slippage_cost
from qis.index_engine import compute_index
from qis.analytics import performance_stats
from qis.reporting import make_basic_plots

def load_csv(path: str, date_col: str, price_col: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=[date_col]).set_index(date_col).sort_index()
    df = df[[price_col]].rename(columns={price_col: "price"})
    return df 

def main():
    cfg = load_config("config.yaml")
    meta = make_run_meta(cfg)

    out = run_dir(cfg["paths"]["runs_dir"], meta.run_id)
    save_json(out / "run_meta.json", meta.__dict__)
    save_json(out / "config_snapshot.json", cfg)

    df = load_csv(cfg["data"]["csv_path"], cfg["data"]["date_col"], cfg["data"]["price_col"])
    df["ret"] = df["price"].pct_change()

    # signal 
    sig_cfg = cfg["signal"]

    if sig_cfg["type"] == "momentum":
        df["signal"] = momentum(df["price"], sig_cfg["lookback"], mode=sig_cfg["mode"])
    
    elif sig_cfg["type"] == "momentum_ensemble":
        df["signal"] = momentum_ensemble(df["price"], sig_cfg["lookbacks"], mode=sig_cfg["mode"])
    else:
        raise ValueError("Unknown signal type")
    
    # risk + leverage 
    df["vol_d"] = ewma_vol(df["ret"], lam=cfg["risk"]["ewma_lambda"])
    df["leverage"] = vol_target_leverage(df["vol_d"], cfg["risk"]["target_vol"], cfg["risk"]["max_leverage"])
    df["w_desired"] = (df["signal"] * df["leverage"]).fillna(0.0)

    # execution schedule
    df["w_exec"] = apply_rebalance_schedule(df["w_desired"], freq=cfg["execution"]["rebalance_freq"])

    # costs
    