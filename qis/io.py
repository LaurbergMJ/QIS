from pathlib import Path 
import json 

def run_dir(base: str | Path, run_id: str) -> Path:
    p = Path(base) / run_id 
    p.mkdir(parents=True, exist_ok=True)
    return p 

def save_json(path: str | Path, obj: dict) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "W", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)

def save_parquet(df, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path)

    