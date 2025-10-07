from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime


class RecentSummary(BaseModel):
    last4_growth_pct: float
    yoy_last_period_pct: float
    volatility_index: float


class AIAdjustmentRequest(BaseModel):
    industry: str
    country: str
    state: Optional[str] = None
    city: Optional[str] = None
    freq: Literal["D", "W", "M"]
    horizon: int
    recent_summary: RecentSummary
    holidays_window: List[str]


class AIAdjustmentResponse(BaseModel):
    adjustment_pct: float = Field(..., ge=-20, le=20)
    rationale: str
    sources: Optional[List[str]] = None


class ForecastRequest(BaseModel):
    industry: str
    country: str
    state: Optional[str] = None
    city: Optional[str] = None
    freq: Literal["D", "W", "M"]
    horizon: int
    date_col: str
    target_col: str
    apply_holidays: bool = True
    apply_ai_adjustment: bool = True


class DataPoint(BaseModel):
    ds: str
    y: Optional[float] = None
    yhat: Optional[float] = None
    yhat_lower: Optional[float] = None
    yhat_upper: Optional[float] = None
    yhat_final: Optional[float] = None


class ForecastMeta(BaseModel):
    freq: str
    train_start: str
    train_end: str
    horizon: int
    holidays_used: List[str]
    original_rows: int
    processed_rows: int
    null_dates: int
    null_targets: int


class ForecastResponse(BaseModel):
    meta: ForecastMeta
    ai_adjustment: Optional[Dict[str, Any]] = None
    history: List[DataPoint]
    forecast_base: List[DataPoint]
    forecast_final: List[DataPoint]


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None