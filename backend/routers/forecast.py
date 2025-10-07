from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import logging

from models.schemas import ForecastResponse, ForecastRequest, ErrorResponse
from services.prophet_service import ProphetService

logger = logging.getLogger(__name__)
router = APIRouter()

def get_prophet_service():
    return ProphetService()

@router.post("/forecast", response_model=ForecastResponse)
async def generate_forecast(
    file: UploadFile = File(...),
    industry: str = Form(...),
    country: str = Form(...),
    freq: str = Form(...),
    horizon: int = Form(...),
    date_col: str = Form(...),
    target_col: str = Form(...),
    state: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    apply_holidays: bool = Form(True),
    apply_ai_adjustment: bool = Form(True),
    service: ProphetService = Depends(get_prophet_service)
):
    """
    Generate sales forecast using Prophet with optional AI adjustment.
    
    Upload a CSV or Excel file with historical sales data and get back
    a forecast with baseline and AI-adjusted predictions.
    """
    try:
        # Validate file size (10MB limit)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        
        # Read file content
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds 10MB limit. Got {len(file_content) / 1024 / 1024:.1f}MB"
            )
        
        # Validate inputs
        if freq not in ["D", "W", "M"]:
            raise HTTPException(status_code=400, detail="Frequency must be 'D', 'W', or 'M'")
        
        if horizon <= 0 or horizon > 365:
            raise HTTPException(status_code=400, detail="Horizon must be between 1 and 365")
        
        if not industry or not country:
            raise HTTPException(status_code=400, detail="Industry and country are required")
        
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="File name is required")
        
        allowed_extensions = ['.csv', '.xlsx', '.xls']
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            raise HTTPException(
                status_code=400,
                detail=f"File must have one of these extensions: {', '.join(allowed_extensions)}"
            )
        
        # Create request object
        request = ForecastRequest(
            industry=industry,
            country=country,
            state=state,
            city=city,
            freq=freq,
            horizon=horizon,
            date_col=date_col,
            target_col=target_col,
            apply_holidays=apply_holidays,
            apply_ai_adjustment=apply_ai_adjustment
        )
        
        logger.warning(f"DEBUG: Forecast request: {industry} in {country} (state={state}, city={city}), {freq}-frequency, {horizon} periods, holidays={apply_holidays}, ai_adj={apply_ai_adjustment}")
        
        # Generate forecast
        result = await service.generate_forecast(file_content, file.filename, request)
        
        logger.info(f"Forecast generated successfully: {len(result.forecast_base)} periods")
        return result
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Forecast generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint for the forecast service."""
    return {"status": "healthy", "service": "forecast"}