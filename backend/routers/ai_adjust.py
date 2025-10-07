from fastapi import APIRouter, HTTPException
from models.schemas import AIAdjustmentRequest, AIAdjustmentResponse, ErrorResponse
from services.perplexity_client import PerplexityClient
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/ai-adjust", response_model=AIAdjustmentResponse)
async def get_ai_adjustment(request: AIAdjustmentRequest):
    """
    Get AI-powered forecast adjustment based on macro factors.
    
    This endpoint takes anonymized metadata about a forecast and returns
    a bounded adjustment percentage with rationale.
    """
    try:
        logger.info(f"AI adjustment request for {request.industry} in {request.country}")
        
        # Validate inputs
        if request.horizon <= 0:
            raise HTTPException(status_code=400, detail="Horizon must be positive")
        
        if request.freq not in ["D", "W", "M"]:
            raise HTTPException(status_code=400, detail="Frequency must be D, W, or M")
        
        # Call Perplexity service
        client = PerplexityClient()
        adjustment = await client.get_adjustment(request)
        
        logger.info(f"AI adjustment: {adjustment.adjustment_pct}% - {adjustment.rationale}")
        return adjustment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI adjustment failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI adjustment service failed: {str(e)}"
        )