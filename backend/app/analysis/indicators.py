import numpy as np
def sma(s,n): return s.rolling(n,min_periods=n).mean()
def ema(s,n): return s.ewm(span=n,adjust=False,min_periods=n).mean()
def daily_returns(p): return p.pct_change().dropna()
def cumulative_returns(p): return (1+daily_returns(p)).cumprod()
def volatility(r,annualize=False,periods=252):
    v=float(r.std(ddof=1)); return v*np.sqrt(periods) if annualize else v
def sharpe_ratio(r,risk_free_rate=0,periods=252):
    if r.empty:return 0.0
    x=r-risk_free_rate/periods; sd=x.std(ddof=1)
    return 0.0 if sd==0 or np.isnan(sd) else float(x.mean()/sd*np.sqrt(periods))
def max_drawdown(e):
    return 0.0 if e.empty else float((e/e.cummax()-1).min())
def rolling_returns(p,w=21): return p.pct_change(w)
def rolling_volatility(r,w=21,periods=252): return r.rolling(w).std()*np.sqrt(periods)
def correlation_matrix(p): return p.pct_change().dropna().corr()
def rolling_correlation(a,b,w=30): return a.pct_change().rolling(w).corr(b.pct_change())
def classify_regime(p,sma_period=50,vol_window=21):
    r=daily_returns(p)
    if len(p)<max(sma_period,vol_window)+2:return "Insufficient Data"
    if volatility(r.tail(vol_window),True)>volatility(r,True)*1.5:return "High Volatility"
    return "Bull Market" if p.iloc[-1]>sma(p,sma_period).iloc[-1] else "Bear Market"
