from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routers import forecast, ai_adjust, geo_data
from models.schemas import ErrorResponse

load_dotenv()

app = FastAPI(
    title="AI Forecasting API",
    description="B2B Sales Forecasting with Prophet and AI Adjustment",
    version="1.0.0"
)

# Changed: Define the specific frontend origins that are allowed to connect
origins = [
    "http://localhost:5173",  # Default Vite dev server port
    "http://localhost:8080",  # Common alternative
    # Add any other frontend URLs you use
]

# Changed: Replace the custom middleware with the official one
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(forecast.router, prefix="/api", tags=["forecast"])
app.include_router(ai_adjust.router, prefix="/api", tags=["ai-adjustment"])
app.include_router(geo_data.router, prefix="/api", tags=["geo-data"])


@app.get("/")
async def root():
    return {"message": "AI Forecasting API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/cors-test")
async def cors_test():
    return {"message": "CORS test successful", "status": "ok"}

@app.options("/{full_path:path}")
async def options_handler(request: Request, full_path: str):
    """Handle all OPTIONS requests"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "86400",
        }
    )



@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
