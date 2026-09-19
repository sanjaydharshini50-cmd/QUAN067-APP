import pandas as pd
from app.analysis.indicators import sma,ema
SUPPORTED=["SMA Crossover","EMA Trend Strategy","Momentum Strategy","Mean Reversion"]
def generate_signal(p,strategy,fast,slow):
    if strategy not in SUPPORTED: raise ValueError(f"Unsupported strategy: {strategy}")
    s=pd.Series(0.0,index=p.index)
    if strategy=="SMA Crossover": s[sma(p,fast)>sma(p,slow)]=1
    elif strategy=="EMA Trend Strategy": s[ema(p,fast)>ema(p,slow)]=1
    elif strategy=="Momentum Strategy": s[p>p.shift(1)]=1
    else: s[p<sma(p,fast)]=1
    return s.shift(1).fillna(0)
