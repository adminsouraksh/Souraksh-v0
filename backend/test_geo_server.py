#!/usr/bin/env python3

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pycountry

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/countries")
async def get_countries():
    """Get list of all countries"""
    countries = []
    for country in pycountry.countries:
        countries.append({
            "value": country.alpha_2,
            "label": country.name,
            "code": country.alpha_2
        })
    
    # Sort by name for better UX
    countries.sort(key=lambda x: x["label"])
    return {"countries": countries}

@app.get("/subdivisions/{country_code}")
async def get_subdivisions(country_code: str):
    """Get states/provinces for a specific country"""
    subdivisions = []
    
    try:
        for subdivision in pycountry.subdivisions:
            if subdivision.country_code == country_code.upper():
                subdivisions.append({
                    "value": subdivision.code,
                    "label": subdivision.name,
                    "code": subdivision.code,
                    "type": subdivision.type
                })
        
        # Sort by name
        subdivisions.sort(key=lambda x: x["label"])
        return {"subdivisions": subdivisions}
    
    except Exception as e:
        return {"subdivisions": [], "error": str(e)}

if __name__ == "__main__":
    uvicorn.run("test_geo_server:app", host="0.0.0.0", port=8001, reload=True)