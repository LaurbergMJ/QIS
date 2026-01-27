from pathlib import Path 
import matplotlib.pyplot as plt 

def plot_series(s, title: str, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.plot(s.index, s.values)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()

def make_basic_plots(df, out_dir: str | Path) -> None:
    out_dir = Path(out_dir)
    plot_series(df["index"], "QIS Index Level", out_dir / "index_level.png")
    plot_series(df["w_exec"], "Equity Weight (executed)", out_dir/ "weights_executed.png")
    plot_series(df["vol_a"], "Annualized Vol Estimate", out_dir / "vol_est.png")
    plot_series(df["turnover"], "turnover.png")
    