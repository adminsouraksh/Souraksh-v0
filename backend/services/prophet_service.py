import pandas as pd
import numpy as np
from prophet import Prophet
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any, List, Optional
import logging
import io

from services.holidays_service import HolidaysService
from services.perplexity_client import PerplexityClient
from models.schemas import (
    ForecastRequest, ForecastResponse, ForecastMeta, DataPoint, 
    AIAdjustmentRequest, RecentSummary
)

logger = logging.getLogger(__name__)

class ProphetService:
    """Service for Prophet-based forecasting with AI adjustment."""
    
    def __init__(self):
        self.holidays_service = HolidaysService()
        self.ai_client = PerplexityClient()
    
    def read_file(self, file_content: bytes, filename: str) -> pd.DataFrame:
        """Read CSV or Excel file content into DataFrame."""
        try:
            if filename.lower().endswith('.csv'):
                # Try different encodings for CSV
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        df = pd.read_csv(io.BytesIO(file_content), encoding=encoding)
                        logger.info(f"Successfully read CSV with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise ValueError("Could not decode CSV file with any supported encoding")
            
            elif filename.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(io.BytesIO(file_content))
                logger.info("Successfully read Excel file")
            
            else:
                raise ValueError("File must be CSV (.csv) or Excel (.xlsx, .xls)")
            
            logger.info(f"File loaded: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            raise ValueError(f"Failed to read file: {str(e)}")
    
    def validate_and_process_data(self, df: pd.DataFrame, 
                                request: ForecastRequest) -> Tuple[pd.DataFrame, ForecastMeta]:
        """Validate and process the input data for forecasting."""
        try:
            original_rows = len(df)
            
            # Check if columns exist
            if request.date_col not in df.columns:
                raise ValueError(f"Date column '{request.date_col}' not found in data")
            if request.target_col not in df.columns:
                raise ValueError(f"Target column '{request.target_col}' not found in data")
            
            # Convert date column
            df_clean = df[[request.date_col, request.target_col]].copy()
            df_clean.columns = ['ds', 'y']
            
            # Parse dates
            df_clean['ds'] = pd.to_datetime(df_clean['ds'], errors='coerce')
            null_dates = df_clean['ds'].isnull().sum()
            
            if null_dates > 0:
                logger.warning(f"Found {null_dates} invalid dates, removing them")
                df_clean = df_clean.dropna(subset=['ds'])
            
            # Convert target to numeric
            df_clean['y'] = pd.to_numeric(df_clean['y'], errors='coerce')
            null_targets = df_clean['y'].isnull().sum()
            
            if null_targets > 0:
                logger.warning(f"Found {null_targets} invalid target values, removing them")
                df_clean = df_clean.dropna(subset=['y'])
            
            if len(df_clean) == 0:
                raise ValueError("No valid data remaining after cleaning")
            
            # Sort by date
            df_clean = df_clean.sort_values('ds').reset_index(drop=True)
            
            # Check minimum data requirements
            if len(df_clean) < 12:
                raise ValueError(f"Insufficient data: need at least 12 periods, got {len(df_clean)}")
            
            # Aggregate to requested frequency if needed
            df_clean = self._aggregate_to_frequency(df_clean, request.freq)
            
            processed_rows = len(df_clean)
            train_start = df_clean['ds'].min().strftime('%Y-%m-%d')
            train_end = df_clean['ds'].max().strftime('%Y-%m-%d')
            
            meta = ForecastMeta(
                freq=request.freq,
                train_start=train_start,
                train_end=train_end,
                horizon=request.horizon,
                holidays_used=[],
                original_rows=original_rows,
                processed_rows=processed_rows,
                null_dates=null_dates,
                null_targets=null_targets
            )
            
            return df_clean, meta
            
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            raise ValueError(f"Data validation failed: {str(e)}")
    
    def _aggregate_to_frequency(self, df: pd.DataFrame, freq: str) -> pd.DataFrame:
        """Aggregate data to the requested frequency."""
        try:
            if freq == 'D':
                # Daily - group by date
                df_agg = df.groupby('ds').agg({'y': 'sum'}).reset_index()
            elif freq == 'W':
                # Weekly - group by Monday-based weeks
                df['week'] = df['ds'].dt.to_period('W-MON')
                df_agg = df.groupby('week').agg({'y': 'sum'}).reset_index()
                df_agg['ds'] = df_agg['week'].dt.start_time
                df_agg = df_agg[['ds', 'y']]
            elif freq == 'M':
                # Monthly - group by month start
                df['month'] = df['ds'].dt.to_period('M')
                df_agg = df.groupby('month').agg({'y': 'sum'}).reset_index()
                df_agg['ds'] = df_agg['month'].dt.start_time
                df_agg = df_agg[['ds', 'y']]
            else:
                return df
            
            return df_agg.sort_values('ds').reset_index(drop=True)
            
        except Exception as e:
            logger.error(f"Frequency aggregation failed: {e}")
            return df
    
    def _get_recent_summary(self, df: pd.DataFrame, freq: str) -> RecentSummary:
        """Calculate recent performance summary for AI adjustment."""
        try:
            # Calculate last 4 periods growth
            if len(df) >= 8:
                last_4 = df.tail(4)['y'].mean()
                prev_4 = df.iloc[-8:-4]['y'].mean()
                last4_growth_pct = ((last_4 - prev_4) / prev_4 * 100) if prev_4 > 0 else 0
            else:
                last4_growth_pct = 0
            
            # Calculate YoY growth (approximate)
            periods_per_year = {'D': 365, 'W': 52, 'M': 12}
            periods_back = periods_per_year.get(freq, 52)
            
            if len(df) > periods_back:
                current_period = df.iloc[-1]['y']
                year_ago_period = df.iloc[-periods_back-1]['y']
                yoy_last_period_pct = ((current_period - year_ago_period) / year_ago_period * 100) if year_ago_period > 0 else 0
            else:
                yoy_last_period_pct = 0
            
            # Calculate volatility (coefficient of variation of last 12 periods)
            recent_values = df.tail(12)['y']
            volatility_index = recent_values.std() / recent_values.mean() if recent_values.mean() > 0 else 0
            volatility_index = min(1.0, max(0.0, volatility_index))  # Clamp to [0, 1]
            
            return RecentSummary(
                last4_growth_pct=round(last4_growth_pct, 2),
                yoy_last_period_pct=round(yoy_last_period_pct, 2),
                volatility_index=round(volatility_index, 3)
            )
            
        except Exception as e:
            logger.error(f"Error calculating recent summary: {e}")
            return RecentSummary(
                last4_growth_pct=0.0,
                yoy_last_period_pct=0.0,
                volatility_index=0.5
            )
    
    async def generate_forecast(self, file_content: bytes, filename: str, 
                              request: ForecastRequest) -> ForecastResponse:
        """Generate complete forecast with Prophet and AI adjustment."""
        try:
            # Read and validate data
            df = self.read_file(file_content, filename)
            df_clean, meta = self.validate_and_process_data(df, request)
            
            # Get holidays if requested
            holidays_df = None
            if request.apply_holidays:
                holidays_df = self.holidays_service.get_holidays_dataframe(
                    request.country, request.state,
                    df_clean['ds'].min(), 
                    df_clean['ds'].max() + timedelta(days=request.horizon*30)
                )
                meta.holidays_used = holidays_df['holiday'].unique().tolist() if not holidays_df.empty else []
            
            # Train Prophet model
            model = self._train_prophet_model(df_clean, holidays_df, request.freq)
            
            # Generate base forecast
            future_df = model.make_future_dataframe(periods=request.horizon, 
                                                  freq=self._get_freq_alias(request.freq))
            forecast = model.predict(future_df)
            
            # Split history and forecast
            split_idx = len(df_clean)
            history_data = df_clean.to_dict('records')
            forecast_base_data = forecast[split_idx:][['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records')
            
            # Apply AI adjustment if requested
            ai_adjustment_info = None
            forecast_final_data = forecast_base_data.copy()
            
            if request.apply_ai_adjustment:
                try:
                    # Get recent summary and upcoming holidays
                    recent_summary = self._get_recent_summary(df_clean, request.freq)
                    upcoming_holidays = self.holidays_service.get_upcoming_holidays(
                        request.country, request.state, request.horizon
                    )
                    
                    # Call AI adjustment service
                    ai_request = AIAdjustmentRequest(
                        industry=request.industry,
                        country=request.country,
                        state=request.state,
                        city=request.city,
                        freq=request.freq,
                        horizon=request.horizon,
                        recent_summary=recent_summary,
                        holidays_window=upcoming_holidays[:5]  # Limit to top 5 holidays
                    )
                    
                    adjustment = await self.ai_client.get_adjustment(ai_request)
                    
                    ai_adjustment_info = {
                        "applied": True,
                        "adjustment_pct": adjustment.adjustment_pct,
                        "rationale": adjustment.rationale,
                        "sources": adjustment.sources or []
                    }
                    
                    # Apply adjustment to forecast
                    adjustment_factor = 1 + (adjustment.adjustment_pct / 100)
                    for i, point in enumerate(forecast_final_data):
                        point['yhat_final'] = point['yhat'] * adjustment_factor
                        
                except Exception as e:
                    logger.error(f"AI adjustment failed: {e}")
                    ai_adjustment_info = {
                        "applied": False,
                        "adjustment_pct": 0.0,
                        "rationale": f"AI adjustment failed: {str(e)}",
                        "sources": []
                    }
                    # Use base forecast as final
                    for point in forecast_final_data:
                        point['yhat_final'] = point['yhat']
            else:
                # No AI adjustment requested
                for point in forecast_final_data:
                    point['yhat_final'] = point['yhat']
            
            # Convert to response format
            history = [DataPoint(ds=str(point['ds'].date()), y=point['y']) for point in history_data]
            
            forecast_base = [
                DataPoint(
                    ds=str(point['ds'].date()) if hasattr(point['ds'], 'date') else str(point['ds'])[:10],
                    yhat=round(point['yhat'], 2),
                    yhat_lower=round(point['yhat_lower'], 2),
                    yhat_upper=round(point['yhat_upper'], 2)
                ) for point in forecast_base_data
            ]
            
            forecast_final = [
                DataPoint(
                    ds=str(point['ds'].date()) if hasattr(point['ds'], 'date') else str(point['ds'])[:10],
                    yhat_final=round(point['yhat_final'], 2)
                ) for point in forecast_final_data
            ]
            
            return ForecastResponse(
                meta=meta,
                ai_adjustment=ai_adjustment_info,
                history=history,
                forecast_base=forecast_base,
                forecast_final=forecast_final
            )
            
        except Exception as e:
            logger.error(f"Forecast generation failed: {e}")
            raise ValueError(f"Forecast generation failed: {str(e)}")
    
    def _train_prophet_model(self, df: pd.DataFrame, holidays_df: Optional[pd.DataFrame], 
                           freq: str) -> Prophet:
        """Train Prophet model with appropriate settings."""
        try:
            # Configure seasonality based on frequency
            daily_seasonality = freq == 'D'
            weekly_seasonality = freq in ['D', 'W']
            yearly_seasonality = True
            
            # Check if we should use multiplicative seasonality
            cv = df['y'].std() / df['y'].mean() if df['y'].mean() > 0 else 0
            seasonality_mode = 'multiplicative' if cv > 0.5 else 'additive'
            
            # Create Prophet model
            model = Prophet(
                daily_seasonality=daily_seasonality,
                weekly_seasonality=weekly_seasonality,
                yearly_seasonality=yearly_seasonality,
                seasonality_mode=seasonality_mode,
                holidays=holidays_df,
                uncertainty_samples=100  # Reduce for faster execution
            )
            
            # Fit model
            model.fit(df)
            logger.info(f"Prophet model trained with {seasonality_mode} seasonality")
            
            return model
            
        except Exception as e:
            logger.error(f"Prophet training failed: {e}")
            raise ValueError(f"Prophet training failed: {str(e)}")
    
    def _get_freq_alias(self, freq: str) -> str:
        """Get pandas frequency alias for Prophet."""
        freq_map = {
            'D': 'D',
            'W': 'W-MON', 
            'M': 'MS'
        }
        return freq_map.get(freq, 'D')