import pandas as pd
from fastapi import APIRouter,HTTPException,Query
from app.data.assets import ASSETS
from app.data.market_data import fetch_history
from app.analysis.indicators import *
from app.backtesting.engine import run_backtest
from app.models import *
router=APIRouter()
def rec(s): return [{"date":str(i.date()),"value":None if pd.isna(v) else float(v)} for i,v in s.items()]
@router.get("/assets")
def assets(): return {"assets":[{"name":k,**v} for k,v in ASSETS.items()]}
@router.get("/data/{asset}")
def data(asset,start=None,end=None):
    try:d=fetch_history(asset,start,end)
    except Exception as e:raise HTTPException(400,str(e))
    return {"asset":asset,"rows":[{"date":str(i.date()),"open":float(r.Open),"high":float(r.High),"low":float(r.Low),"close":float(r.Close),"volume":float(r.Volume)} for i,r in d.iterrows()]}
@router.post("/analysis")
def analysis(q:AnalysisRequest):
    try:
        p=fetch_history(q.asset,q.start_date,q.end_date)["Close"];r=daily_returns(p)
        return {"asset":q.asset,"current_price":float(p.iloc[-1]),"daily_change":float(r.iloc[-1]) if len(r) else 0,
        "sma":rec(sma(p,q.sma_period)),"ema":rec(ema(p,q.ema_period)),"returns":rec(r),
        "cumulative_returns":rec(cumulative_returns(p)),"rolling_returns":rec(rolling_returns(p)),
        "rolling_volatility":rec(rolling_volatility(r)),"annualized_volatility":volatility(r,True),
        "sharpe":sharpe_ratio(r),"max_drawdown":max_drawdown(p/p.iloc[0]),"regime":classify_regime(p,q.sma_period),"prices":rec(p)}
    except Exception as e:raise HTTPException(400,str(e))
@router.post("/correlation")
def correlation(q:CorrelationRequest):
    try:
        p=pd.concat([fetch_history(a,q.start_date,q.end_date)["Close"].rename(a) for a in q.assets],axis=1).dropna()
        m=correlation_matrix(p);roll={}
        if len(q.assets)>=2:roll[f"{q.assets[0]}:{q.assets[1]}"]=rec(rolling_correlation(p.iloc[:,0],p.iloc[:,1],q.rolling_window))
        return {"assets":q.assets,"matrix":m.round(6).to_dict(),"rolling":roll}
    except Exception as e:raise HTTPException(400,str(e))
@router.post("/backtest")
def backtest(q:BacktestRequest):
    try:
        p=fetch_history(q.asset,q.start_date,q.end_date)["Close"]
        return {"asset":q.asset,"strategy":q.strategy,"parameters":q.model_dump(),**run_backtest(p,q.strategy,q.fast_period,q.slow_period,q.initial_capital,q.transaction_cost_pct,q.position_size)}
    except Exception as e:raise HTTPException(400,str(e))
@router.get("/risk/{asset}")
def risk(asset,start=None,end=None):
    try:
        p=fetch_history(asset,start,end)["Close"];r=daily_returns(p);e=(1+r).cumprod()
        return {"asset":asset,"annualized_volatility":volatility(r,True),"sharpe":sharpe_ratio(r),"max_drawdown":max_drawdown(e),"drawdown_curve":rec(e/e.cummax()-1),"rolling_volatility":rec(rolling_volatility(r))}
    except Exception as e:raise HTTPException(400,str(e))
@router.get("/report")
def report(asset=Query("Gold"),strategy=Query("SMA Crossover")):
    return {"platform":"OMNICRYPTO","mode":"Historical Research / Simulation","tracked_assets":list(ASSETS),"asset":asset,"strategy":strategy,"components":["SMA / EMA","Daily Returns","Cumulative Returns","Annualized Volatility","Sharpe Ratio","Maximum Drawdown","Correlation Analysis","Strategy Backtesting","Market Regime Analysis"],"notice":"Historical simulation does not guarantee future returns."}
