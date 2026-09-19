from datetime import date
from pydantic import BaseModel, Field
class BacktestRequest(BaseModel):
    asset:str="Gold"; strategy:str="SMA Crossover"
    fast_period:int=Field(20,ge=2,le=500); slow_period:int=Field(50,ge=3,le=1000)
    initial_capital:float=Field(100000,gt=0); transaction_cost_pct:float=Field(.10,ge=0,le=10)
    start_date:date|None=None; end_date:date|None=None; position_size:float=Field(1,gt=0,le=1)
class AnalysisRequest(BaseModel):
    asset:str="Gold"; start_date:date|None=None; end_date:date|None=None
    sma_period:int=Field(20,ge=2,le=500); ema_period:int=Field(21,ge=2,le=500)
class CorrelationRequest(BaseModel):
    assets:list[str]=Field(default_factory=lambda:["Gold","Bitcoin","NVIDIA"])
    start_date:date|None=None; end_date:date|None=None
    rolling_window:int=Field(30,ge=2,le=500)
