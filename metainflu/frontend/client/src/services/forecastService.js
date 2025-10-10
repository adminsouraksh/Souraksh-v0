// File: frontend/client/src/services/forecastService.js
import axios from 'axios';

// Changed: Removed the trailing slash from the API_URL
const API_URL = 'https://souraksh-v0po.onrender.com/api';

const getAuthToken = () => {
  const user = JSON.parse(localStorage.getItem('user'));
  return user ? user.token : null;
};

// This will now correctly form the URL as http://localhost:8000/api/countries
export async function getCountries() {
  try {
    const response = await axios.get(`${API_URL}/countries`);
    return response.data.countries;
  } catch (error) {
    console.error("Error fetching countries:", error);
    return [];
  }
}

// This will now correctly form the URL as http://localhost:8000/api/subdivisions/{country}
export async function getSubdivisions(country) {
  if (!country) return [];
  try {
    const response = await axios.get(`${API_URL}/subdivisions/${country}`);
    return response.data.subdivisions;
  } catch (error) {
    console.error(`Error fetching subdivisions for ${country}:`, error);
    return [];
  }
}

export async function generateForecast(params) {
    const token = getAuthToken();
    if (!token) {
        throw new Error('Authentication token not found.');
    }

    const formData = new FormData();
    formData.append('file', params.file);
    formData.append('industry', params.industry);
    formData.append('country', params.country);
    formData.append('freq', params.freq);
    formData.append('horizon', params.horizon);
    formData.append('date_col', params.date_col);
    formData.append('target_col', params.target_col);
    if (params.state) {
        formData.append('state', params.state);
    }
    if (params.city) {
        formData.append('city', params.city);
    }
    formData.append('apply_holidays', params.apply_holidays);
    formData.append('apply_ai_adjustment', params.apply_ai_adjustment);

    try {
        // This will now correctly form the URL as http://localhost:8000/api/forecast
        const response = await axios.post(`${API_URL}/forecast`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        if (error.response && error.response.data) {
            throw new Error(error.response.data.message || 'An error occurred during forecast generation.');
        } else {
            throw new Error('An error occurred during forecast generation.');
        }
    }
}
