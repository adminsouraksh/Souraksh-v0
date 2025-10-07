import holidays
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class HolidaysService:
    """Service for handling country and state-specific holidays."""
    
    def __init__(self):
        self.supported_countries = {
            'US': 'United States',
            'IN': 'India', 
            'GB': 'United Kingdom',
            'CA': 'Canada',
            'AU': 'Australia',
            'DE': 'Germany',
            'FR': 'France',
            'JP': 'Japan',
            'BR': 'Brazil',
            'MX': 'Mexico'
        }
    
    def get_country_code(self, country_input: str) -> Optional[str]:
        """Convert country name/code to ISO code."""
        country_upper = country_input.upper()
        
        # If it's already a 2-letter country code and supported, return it
        if len(country_upper) == 2 and country_upper in self.supported_countries:
            return country_upper
        
        # Otherwise try to map from name to code
        country_lower = country_input.lower()
        name_to_code = {
            'united states': 'US',
            'usa': 'US',
            'america': 'US',
            'india': 'IN',
            'united kingdom': 'GB',
            'uk': 'GB',
            'britain': 'GB',
            'canada': 'CA',
            'australia': 'AU',
            'germany': 'DE',
            'france': 'FR',
            'japan': 'JP',
            'brazil': 'BR',
            'mexico': 'MX'
        }
        
        return name_to_code.get(country_lower)
    
    def get_holidays_dataframe(self, country: str, state: Optional[str] = None, 
                             start_date: datetime = None, end_date: datetime = None) -> pd.DataFrame:
        """
        Get holidays as a pandas DataFrame for Prophet.
        
        Args:
            country: Country name or ISO code
            state: State/province name (if supported)
            start_date: Start date for holiday range
            end_date: End date for holiday range
            
        Returns:
            DataFrame with 'ds' and 'holiday' columns
        """
        try:
            # Default date range if not provided
            if start_date is None:
                start_date = datetime.now() - timedelta(days=365*2)
            if end_date is None:
                end_date = datetime.now() + timedelta(days=365*2)
                
            country_code = self.get_country_code(country)
            if not country_code:
                logger.warning(f"Country '{country}' not supported for holidays")
                return pd.DataFrame(columns=['ds', 'holiday'])
            
            years = list(range(start_date.year, end_date.year + 1))
            
            # Get holidays based on country and state
            holiday_dict = self._get_holidays_dict(country_code, state, years)
            
            if not holiday_dict:
                logger.warning(f"No holidays found for {country_code}")
                return pd.DataFrame(columns=['ds', 'holiday'])
            
            # Convert to DataFrame
            holiday_data = []
            for date, name in holiday_dict.items():
                if start_date.date() <= date <= end_date.date():
                    holiday_data.append({
                        'ds': date,
                        'holiday': name
                    })
            
            df = pd.DataFrame(holiday_data)
            logger.warning(f"HOLIDAYS DEBUG: Found {len(df)} holidays for {country_code}" + 
                       (f"/{state}" if state else ""))
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting holidays: {e}")
            return pd.DataFrame(columns=['ds', 'holiday'])
    
    def _get_holidays_dict(self, country_code: str, state: Optional[str], years: List[int]) -> dict:
        """Get holidays dictionary from holidays library."""
        try:
            if country_code == 'US' and state:
                # US supports state-level holidays
                return holidays.US(state=state, years=years)
            elif country_code == 'IN' and state:
                # India supports some state-level holidays
                state_mapping = {
                    'maharashtra': 'MH',
                    'karnataka': 'KA', 
                    'tamil nadu': 'TN',
                    'gujarat': 'GJ',
                    'west bengal': 'WB',
                    'rajasthan': 'RJ',
                    'uttar pradesh': 'UP',
                    'madhya pradesh': 'MP',
                    'bihar': 'BR',
                    'odisha': 'OR'
                }
                state_code = state_mapping.get(state.lower())
                if state_code:
                    return holidays.India(state=state_code, years=years)
                else:
                    return holidays.India(years=years)
            elif country_code == 'CA' and state:
                # Canada supports province-level holidays
                province_mapping = {
                    'ontario': 'ON',
                    'quebec': 'QC',
                    'british columbia': 'BC',
                    'alberta': 'AB',
                    'manitoba': 'MB',
                    'saskatchewan': 'SK',
                    'nova scotia': 'NS',
                    'new brunswick': 'NB',
                    'newfoundland and labrador': 'NL',
                    'prince edward island': 'PE'
                }
                province_code = province_mapping.get(state.lower())
                if province_code:
                    return holidays.Canada(state=province_code, years=years)
                else:
                    return holidays.Canada(years=years)
            else:
                # Use national holidays
                country_classes = {
                    'US': holidays.US,
                    'IN': holidays.India,
                    'GB': holidays.UK,
                    'CA': holidays.Canada,
                    'AU': holidays.Australia,
                    'DE': holidays.Germany,
                    'FR': holidays.France,
                    'JP': holidays.Japan,
                    'BR': holidays.Brazil,
                    'MX': holidays.Mexico
                }
                
                holiday_class = country_classes.get(country_code)
                if holiday_class:
                    return holiday_class(years=years)
                
            return {}
            
        except Exception as e:
            logger.error(f"Error creating holidays object: {e}")
            return {}
    
    def get_upcoming_holidays(self, country: str, state: Optional[str] = None, 
                            weeks_ahead: int = 8) -> List[str]:
        """Get list of upcoming holiday names for AI context."""
        try:
            start_date = datetime.now()
            end_date = start_date + timedelta(weeks=weeks_ahead)
            
            holidays_df = self.get_holidays_dataframe(country, state, start_date, end_date)
            
            if holidays_df.empty:
                return []
            
            # Return unique holiday names
            return holidays_df['holiday'].unique().tolist()
            
        except Exception as e:
            logger.error(f"Error getting upcoming holidays: {e}")
            return []