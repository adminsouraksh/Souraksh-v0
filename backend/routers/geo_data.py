from fastapi import APIRouter
import pycountry

router = APIRouter()

@router.get("/countries")
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

@router.get("/subdivisions/{country_code}")
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

# For cities, we'll use a simple approach since pycountry doesn't have city data
# You could integrate with other APIs like GeoNames, but for now we'll keep it simple
@router.get("/cities/{subdivision_code}")
async def get_cities(subdivision_code: str):
    """Get cities for a specific subdivision (placeholder implementation)"""
    # This is a placeholder - in a real app you'd integrate with a proper city database
    # For now, we'll return an empty list and let users type city names
    return {"cities": [], "message": "City selection not implemented - please type city name"}