// File: frontend/client/src/services/forecastService.js
import axios from 'axios';

const API_URL = 'https://souraksh-v0po.onrender.com/api/forecast';

// Function to get the auth token from localStorage
const getAuthToken = () => {
  const user = JSON.parse(localStorage.getItem('user'));
  return user ? user.token : null;
};

export async function getCountries() {
    // This can be replaced with an API call if needed
    await new Promise(res => setTimeout(res, 100));
    return [
        { value: 'US', label: 'United States' },
        { value: 'IN', label: 'India' },
        { value: 'CA', label: 'Canada' },
        { value: 'GB', label: 'United Kingdom' },
        { value: 'AU', label: 'Australia' },
        { value: 'DE', label: 'Germany' },
        { value: 'FR', label: 'France' },
        { value: 'JP', label: 'Japan' },
        { value: 'BR', label: 'Brazil' },
        { value: 'MX', label: 'Mexico' },
    ];
}

export async function getSubdivisions(country) {
    // This can be replaced with an API call if needed
    await new Promise(res => setTimeout(res, 100));
    if (country === 'US') return [{ value: 'CA', label: 'California' }, { value: 'NY', label: 'New York' }];
    if (country === 'IN') return [{ value: 'MH', label: 'Maharashtra' }, { value: 'DL', label: 'Delhi' }];
    return [];
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
        const response = await axios.post(API_URL, formData, {
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