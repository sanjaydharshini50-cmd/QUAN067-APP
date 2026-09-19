import pandas as pd, yfinance as yf
from .assets import get_asset
def _clean(df):
    if df is None or df.empty: raise ValueError("No market data returned.")
    if isinstance(df.columns,pd.MultiIndex): df.columns=df.columns.get_level_values(0)
    df=df.rename(columns={c:str(c).title() for c in df.columns})
    for c in ["Open","High","Low","Close","Volume"]:
        if c not in df: df[c]=0.0
    df=df[["Open","High","Low","Close","Volume"]].copy()
    idx=pd.to_datetime(df.index)
    if getattr(idx,"tz",None) is not None: idx=idx.tz_localize(None)
    df.index=idx
    return df.dropna(subset=["Close"])
def fetch_history(asset,start=None,end=None,period="5y"):
    kw={"auto_adjust":True,"progress":False}
    if start:
        kw["start"]=str(start)
        if end: kw["end"]=str(end)
    else: kw["period"]=period
    return _clean(yf.download(get_asset(asset)["ticker"],**kw))
