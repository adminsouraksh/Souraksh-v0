# Project Documentation & Summary

This document provides a summary of the work completed today and an overview of the application's data flow for the forecasting feature.

## Summary of Work Completed

Today, we worked through several issues to connect the frontend and backend services and implement new features. Here is a summary of the key accomplishments:

1.  **Initial Setup & Cleanup:**
    *   Removed the old, unused React frontend from the `AI-Demand-Forecasting-System` project.

2.  **Backend Integration & CORS Fixes:**
    *   Connected the `metainflu` Vue.js frontend to the `AI-Demand-Forecasting-System` Python backend by creating a proxy endpoint in the `metainflu` Node.js backend.
    *   Resolved a `405 Method Not Allowed` error by correcting the API path to `/api/forecast`.
    *   Fixed a Cross-Origin Resource Sharing (CORS) issue by properly configuring the `cors` middleware in the Node.js backend to handle authenticated requests from the frontend.

3.  **Frontend File Parsing:**
    *   Diagnosed a `400 Bad Request` error caused by the frontend sending mocked data instead of parsing the uploaded file.
    *   Replaced the mock functions with real file-parsing logic by installing and implementing the `papaparse` (for CSV) and `xlsx` (for Excel) libraries.
    *   Implemented heuristic-based column detection to automatically identify and suggest the date and target columns.

4.  **New Feature: Advanced Charting:**
    *   Successfully implemented a major new feature in the "Data Analysis" tab.
    *   The UI now detects if the historical data spans a single year or multiple years.
    *   **For multi-year data**, it displays three charts: a bar chart for sales per year, a bar chart for monthly sales of a selected year, and a line chart comparing monthly sales across all years.
    *   **For single-year data**, it displays a simple bar chart of monthly sales.

5.  **Bug Fixing & Troubleshooting:**
    *   Resolved a dependency crisis with the Python backend by identifying incompatible library versions (`pandas`, `scikit-learn`) with Python 3.13 and updating the `requirements.txt` file.
    *   Fixed a critical rendering bug (`Cannot access 'reinitCharts' before initialization`) in the `AnalysisModule.vue` component by correcting the code order.
    *   Diagnosed a Google Sign-In error (`The given origin is not allowed`) and provided clear instructions on how to resolve it by configuring the Authorized JavaScript origins in the Google Cloud Console.

## Data Flow Diagram (DFD)

This diagram illustrates how data moves through the system when a user requests a forecast.

```mermaid
graph TD
    A[User's Browser <br> (Vue Frontend)] -- 1. Upload CSV/XLSX --> B[metainflu Backend <br> (Node.js/Express)];
    B -- 2. Auth Middleware Checks Token --> C{User Authenticated?};
    C -- No --> D[401 Unauthorized Response];
    C -- Yes --> E[Proxy to AI Backend];
    E -- 3. Forward File + Params --> F[AI-Demand-Forecasting Backend <br> (Python/FastAPI)];
    F -- 4. Generate Forecast --> F;
    F -- 5. Return Forecast JSON --> E;
    E -- 6. Return Forecast JSON --> B;
    B -- 7. Send JSON to Frontend --> A;
    A -- 8. Render Charts and Results --> A;
```

## Detailed Data Flow

Here is a step-by-step breakdown of the forecast generation process:

1.  **File Upload (Frontend):**
    *   The user selects a CSV or Excel file in the UI.
    *   The frontend parses the file in the browser to extract column names and a data preview.
    *   The user fills out the configuration form (selecting date/target columns, forecast horizon, etc.).
    *   Upon submission, the frontend sends the original file and configuration parameters to the `metainflu` backend, including the user's authentication token in the request header.

2.  **Authentication (metainflu Backend):**
    *   The Node.js server receives the request at the `/api/forecast` endpoint.
    *   The `protect` authentication middleware intercepts the request and validates the JWT token to ensure the user is logged in.
    *   If the token is invalid, it returns a `401 Unauthorized` error.

3.  **Proxy Request (metainflu Backend):**
    *   If authentication is successful, the backend constructs a new `multipart/form-data` request containing the file and all the parameters.
    *   It forwards this request to the `AI-Demand-Forecasting-System` backend at the `/api/forecast` endpoint.

4.  **Forecast Generation (AI Backend):**
    *   The Python/FastAPI server receives the request.
    *   It uses the `prophet` library and other services to perform the time-series forecast based on the provided data and parameters.

5.  **Response (AI Backend to metainflu Backend):**
    *   Once the forecast is complete, the AI backend sends the results (including historical data, baseline forecast, and AI adjustments) back to the `metainflu` backend as a JSON response.

6.  **Proxy Response (metainflu Backend to Frontend):**
    *   The `metainflu` backend receives the JSON response and forwards it directly to the user's browser.

7.  **Render Results (Frontend):**
    *   The Vue application receives the forecast data.
    *   It updates its state, causing the `ResultsPanel` to render.
    *   The `AnalysisModule` inside the results panel processes the historical data from the response and uses the `echarts` library to render the appropriate single-year or multi-year charts.
