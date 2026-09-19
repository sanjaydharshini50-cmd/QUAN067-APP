import numpy as np
from app.analysis.indicators import sharpe_ratio,max_drawdown
from app.strategy.signals import generate_signal
def run_backtest(p,strategy,fast,slow,capital,cost_pct,size=1):
    if fast>=slow and strategy in ("SMA Crossover","EMA Trend Strategy"): raise ValueError("Fast period must be lower than slow period.")
    r=p.pct_change().fillna(0); sig=generate_signal(p,strategy,fast,slow); pos=sig.clip(0,1)*size
    turnover=pos.diff().abs().fillna(pos.abs()); cost=turnover*cost_pct/100
    sr=pos*r-cost; eq=capital*(1+sr).cumprod(); bh=capital*(1+r).cumprod()
    return {"final_equity":float(eq.iloc[-1]),"total_return":float(eq.iloc[-1]/capital-1),
    "benchmark_final_equity":float(bh.iloc[-1]),"benchmark_return":float(bh.iloc[-1]/capital-1),
    "sharpe":sharpe_ratio(sr),"benchmark_sharpe":sharpe_ratio(r),
    "volatility":float(sr.std(ddof=1)*np.sqrt(252)),"benchmark_volatility":float(r.std(ddof=1)*np.sqrt(252)),
    "max_drawdown":max_drawdown(eq),"benchmark_max_drawdown":max_drawdown(bh),
    "trades":int((turnover>0).sum()),
    "equity_curve":[{"date":str(i.date()),"value":float(v)} for i,v in eq.items()],
    "benchmark_curve":[{"date":str(i.date()),"value":float(v)} for i,v in bh.items()],
    "signals":[{"date":str(i.date()),"signal":int(v)} for i,v in sig.items() if v!=0]}
