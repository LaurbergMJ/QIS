from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path 
import hashlib, json, subprocess
import yaml 
from datetime import datetime, timezone

@dataclass(frozen=True)
class RunMeta:
    run_id: str
    timestamp_utc: str 
    git_commit: str 
    config_hash: str 

def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev_parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown error throwin in _git_commit method"
    
def _hash_dict(d: dict) -> str:
    s = json.dumps(d, sort_keys=True).encode("utf-8")
    return hashlib.sha256(s).hexdigest()[:12]

def load_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ValueError("Config must be a mapping")
    return cfg 

def make_run_meta(cfg: dict) -> RunMeta:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ch = _hash_dict(cfg)
    commit = _git_commit()
    run_id = f"{ts}_{ch}"
    return RunMeta(run_id=run_id, timestamp_utc=ts, git_commit=commit, config_hash=ch)


