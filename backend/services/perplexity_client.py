import httpx
import json
import os
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv

from models.schemas import AIAdjustmentRequest, AIAdjustmentResponse

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class PerplexityClient:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            logger.warning("PERPLEXITY_API_KEY not found in environment variables")
        
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _build_prompt(self, request: AIAdjustmentRequest) -> str:
        """Build the dynamic prompt for Perplexity Sonar."""
        freq_units_map = {"D": "days", "W": "weeks", "M": "months"}
        freq_units = freq_units_map.get(request.freq, "periods")
        
        holidays_text = ", ".join(request.holidays_window) if request.holidays_window else "None"
        
        location = request.city or ""
        if request.state:
            location = f"{location}, {request.state}" if location else request.state
        location = f"{location}, {request.country}" if location else request.country
        
        system_prompt = """You are a cautious forecaster. You never see raw sales data. You only output a small adjustment percentage and a concise rationale. Stay within ±20% total adjustment."""
        
        user_prompt = f"""We have a short-term {request.freq}-level sales forecast for the {request.industry} sector in {location}.
Horizon: next {request.horizon} {freq_units}.
Recent pattern summary (approximate, anonymized):
- Last 4 {freq_units} growth: {request.recent_summary.last4_growth_pct}% 
- YoY last comparable period: {request.recent_summary.yoy_last_period_pct}%
- Volatility index (0–1): {request.recent_summary.volatility_index}

Upcoming holidays/events in scope: {holidays_text}

Task:
1) Search current macro signals that materially impact {request.industry} in {request.country}/{request.state or ''}/{request.city or ''}: inflation/CPI, consumer confidence, policy rates, FX, fuel, supply/logistics, major retail events (e.g., Diwali sale weeks), weather anomalies.
2) Propose one net bounded adjustment in percent (negative for down, positive for up) in the range -20 to +20 applied to the baseline.
3) Provide a concise rationale (≤ 60 words) with 2–4 bullet reasons.
4) Return STRICT JSON ONLY:

{{
  "adjustment_pct": <number between -20 and 20>,
  "rationale": "<one short paragraph>",
  "sources": ["<url1>", "<url2>"]
}}

Do not include any other text."""
        
        return system_prompt, user_prompt
    
    async def get_adjustment(self, request: AIAdjustmentRequest) -> AIAdjustmentResponse:
        """Get AI adjustment from Perplexity Sonar."""
        if not self.api_key:
            logger.warning("PERPLEXITY DEBUG: No Perplexity API key available, returning 0% adjustment")
            return AIAdjustmentResponse(
                adjustment_pct=0.0,
                rationale="No reliable macro adjustment - API key not configured",
                sources=[]
            )
        
        try:
            system_prompt, user_prompt = self._build_prompt(request)
            
            payload = {
                "model": "sonar",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 500
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    logger.error(f"Perplexity API error: {response.status_code} - {response.text}")
                    return self._fallback_response("API request failed")
                
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                if not content:
                    logger.error("Empty response from Perplexity API")
                    return self._fallback_response("Empty API response")
                
                # Parse JSON from content
                try:
                    # Sometimes the response might have extra text, try to extract JSON
                    content = content.strip()
                    if content.startswith("```json"):
                        content = content.replace("```json", "").replace("```", "").strip()
                    elif content.startswith("```"):
                        content = content.replace("```", "").strip()
                    
                    adjustment_data = json.loads(content)
                    
                    # Validate and clamp adjustment percentage
                    adj_pct = float(adjustment_data.get("adjustment_pct", 0))
                    adj_pct = max(-20, min(20, adj_pct))  # Clamp to [-20, 20]
                    
                    return AIAdjustmentResponse(
                        adjustment_pct=adj_pct,
                        rationale=adjustment_data.get("rationale", "Macro adjustment applied"),
                        sources=adjustment_data.get("sources", [])
                    )
                    
                except (json.JSONDecodeError, ValueError, KeyError) as e:
                    logger.error(f"Failed to parse Perplexity response: {e} - Content: {content}")
                    return self._fallback_response("Invalid API response format")
                
        except Exception as e:
            logger.error(f"Perplexity API call failed: {e}")
            return self._fallback_response("API service unavailable")
    
    def _fallback_response(self, reason: str) -> AIAdjustmentResponse:
        """Return fallback response with 0% adjustment."""
        return AIAdjustmentResponse(
            adjustment_pct=0.0,
            rationale=f"No reliable macro adjustment - {reason}",
            sources=[]
        )