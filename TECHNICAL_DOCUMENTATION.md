# AI Demand Forecasting System - Technical Documentation

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Backend Components](#backend-components)
3. [Frontend Components](#frontend-components)
4. [Data Flow & API Endpoints](#data-flow--api-endpoints)
5. [Component Logic Explanation](#component-logic-explanation)
6. [AI Integration & Privacy](#ai-integration--privacy)
7. [Local Development Setup](#local-development-setup)
8. [Testing & Deployment](#testing--deployment)

---

## 🏗️ System Architecture

The AI Demand Forecasting System is a full-stack application with a clear separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│                  Frontend (React)                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │
│  │   Upload    │ │   Config    │ │   Results   │    │
│  │   Module    │ │   Module    │ │   Module    │    │
│  └─────────────┘ └─────────────┘ └─────────────┘    │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP/JSON API
┌─────────────────────┴───────────────────────────────┐
│               Backend (FastAPI)                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │
│  │   Prophet   │ │ Perplexity  │ │  Holidays   │    │
│  │   Service   │ │   Client    │ │   Service   │    │
│  └─────────────┘ └─────────────┘ └─────────────┘    │
└─────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- **FastAPI**: High-performance async web framework
- **Prophet**: Facebook's time series forecasting library
- **Perplexity Sonar**: AI-powered macro adjustments
- **Holidays**: Multi-country holiday detection
- **Pandas**: Data manipulation and analysis
- **Pydantic**: Data validation and serialization

**Frontend:**
- **React 18**: Component-based UI framework
- **TypeScript**: Type-safe JavaScript development
- **React Query**: Server state management
- **Recharts**: Data visualization library
- **Lucide React**: Modern icon library
- **React Hook Form**: Form state management

---

## 🔧 Backend Components

### 1. Main Application (`main.py`)

**Purpose**: FastAPI application entry point with middleware and routing setup.

**Key Features:**
- **CORS Middleware**: Custom implementation for cross-origin requests
- **Error Handling**: Global exception handler for consistent error responses
- **Router Integration**: Modular endpoint organization
- **Health Checks**: Basic application health monitoring

```python
# Custom CORS middleware handles preflight and regular requests
class SimpleCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Handle OPTIONS preflight requests
        if request.method == "OPTIONS":
            response = Response()
            # Set CORS headers
        # Process regular requests and add CORS headers
```

### 2. Data Models (`models/schemas.py`)

**Purpose**: Pydantic models for request/response validation and serialization.

**Key Models:**

- **`ForecastRequest`**: Validates forecast generation parameters
- **`ForecastResponse`**: Structured forecast results with metadata
- **`AIAdjustmentRequest/Response`**: AI macro adjustment data structures
- **`DataPoint`**: Individual time series data point
- **`ForecastMeta`**: Metadata about training period and data quality

**Validation Features:**
- Type safety with Pydantic
- Field constraints (e.g., adjustment_pct bounded to ±20%)
- Optional fields with defaults

### 3. Forecast Router (`routers/forecast.py`)

**Purpose**: Main endpoint for forecast generation with comprehensive validation.

**Endpoint**: `POST /api/forecast`

**Input Validation:**
- File size limit (10MB)
- File format validation (.csv, .xlsx, .xls)
- Parameter bounds checking
- Required field validation

**Processing Flow:**
```python
async def generate_forecast():
    1. Validate file and parameters
    2. Create ForecastRequest object
    3. Delegate to ProphetService
    4. Return structured response
```

### 4. Prophet Service (`services/prophet_service.py`)

**Purpose**: Core forecasting logic using Facebook Prophet.

**Key Methods:**

#### `read_file(file_content, filename)`
- **Input**: Raw file bytes and filename
- **Process**: Multi-encoding CSV support, Excel file handling
- **Output**: Pandas DataFrame
- **Error Handling**: Graceful encoding fallback

#### `validate_and_process_data(df, request)`
- **Input**: Raw DataFrame and forecast parameters
- **Process**:
  - Column validation and mapping
  - Date parsing with error handling
  - Numeric conversion for target values
  - Data quality assessment
  - Frequency aggregation
- **Output**: Clean DataFrame + metadata
- **Validation**: Minimum 12 data points requirement

#### `_aggregate_to_frequency(df, freq)`
- **Daily ('D')**: Group by date, sum values
- **Weekly ('W')**: Group by Monday-based weeks
- **Monthly ('M')**: Group by month start, sum values

#### `generate_forecast(file_content, filename, request)`
**Main orchestration method:**

```python
async def generate_forecast():
    1. Read and validate input data
    2. Get holidays (if requested)
    3. Train Prophet model with appropriate seasonality
    4. Generate base forecast
    5. Apply AI adjustment (if requested)
    6. Format and return results
```

#### `_train_prophet_model(df, holidays_df, freq)`
**Prophet Configuration:**
- **Seasonality Settings**:
  - Daily: Only for 'D' frequency
  - Weekly: For 'D' and 'W' frequencies
  - Yearly: Always enabled
- **Seasonality Mode**: Automatic selection based on coefficient of variation
- **Holidays Integration**: Country/state-specific holidays
- **Performance Optimization**: Reduced uncertainty samples (100)

#### `_get_recent_summary(df, freq)`
**Business Intelligence Calculation:**
- **Last 4 Periods Growth**: Recent trend analysis
- **Year-over-Year Growth**: Seasonal comparison
- **Volatility Index**: Coefficient of variation (clamped 0-1)

### 5. Perplexity Client (`services/perplexity_client.py`)

**Purpose**: AI-powered macro economic adjustments via Perplexity Sonar.

**Privacy-First Design:**
- **No Raw Data**: Only anonymized metadata sent to AI
- **Bounded Adjustments**: ±20% maximum change
- **Fallback Handling**: Graceful degradation when AI unavailable

#### `_build_prompt(request)`
**Dynamic Prompt Construction:**
```python
def _build_prompt():
    # Constructs context-aware prompt with:
    # - Industry and location context
    # - Recent performance summary (anonymized)
    # - Upcoming holidays
    # - Strict JSON response format
```

#### `get_adjustment(request)`
**AI Processing Pipeline:**
```python
async def get_adjustment():
    1. Build contextual prompt
    2. Call Perplexity Sonar API
    3. Parse and validate JSON response
    4. Apply bounds checking (±20%)
    5. Return structured adjustment
```

**Error Handling:**
- API key validation
- Network timeout handling
- JSON parsing with fallback
- Response format validation

### 6. Holidays Service (`services/holidays_service.py`)

**Purpose**: Multi-country holiday detection for forecast accuracy.

**Supported Regions:**
- **USA**: All 50 states
- **India**: National + major states (Maharashtra, Karnataka, etc.)
- **Canada**: All provinces
- **UK, Australia, Germany, France, Japan, Brazil, Mexico**: National holidays

#### `get_holidays_dataframe(country, state, start_date, end_date)`
**Holiday Processing:**
```python
def get_holidays_dataframe():
    1. Map country names to ISO codes
    2. Create holidays object with state/province support
    3. Filter by date range
    4. Return Prophet-compatible DataFrame
```

#### `get_upcoming_holidays(country, state, weeks_ahead)`
**AI Context Helper:**
- Returns holiday names for AI prompt context
- Configurable look-ahead window
- Used for macro adjustment insights

---

## 🎨 Frontend Components

### 1. Main Application (`App.tsx`)

**Purpose**: Root component orchestrating the entire user flow.

**State Management:**
- **Current Step**: 'upload' → 'configure' → 'results'
- **Upload State**: File, preview, detected columns, processing status
- **Forecast State**: Results, errors, loading status
- **Tab State**: Results dashboard navigation

**Key Features:**
- **React Query Integration**: Server state management
- **Error Boundaries**: Graceful error handling
- **Step-based Navigation**: Guided user experience
- **Results Tabs**: Forecast, Analysis, Financial projections

### 2. Simple Upload Area (`components/SimpleUploadArea.tsx`)

**Purpose**: File upload with drag-and-drop, validation, and preview.

**Features:**

#### File Handling
```typescript
const handleFiles = useCallback(async (files: FileList) => {
    1. Validate file type and name
    2. Set processing state
    3. Parse file content
    4. Analyze columns for auto-detection
    5. Display preview and proceed to config
});
```

#### Column Detection Integration
- **Auto-detection**: Uses `detectColumns` utility
- **Confidence Display**: Shows detection confidence percentages
- **Manual Override**: User can override auto-detected columns

#### File Preview
- **Data Table**: First 5 rows, first 8 columns
- **File Metadata**: Size, row count, column count
- **Data Quality**: Shows truncated cell values

#### Drag & Drop UX
- **Visual Feedback**: Border color and background changes
- **Processing State**: Loading spinner during file processing
- **Error Display**: Clear error messages with actionable feedback

### 3. Configuration Form (`components/ConfigForm.tsx`)

**Purpose**: Comprehensive forecast configuration with dynamic geographic data.

**Form Sections:**

#### Business Context
```typescript
// Industry Selection
INDUSTRIES = [
    { value: 'retail', label: 'Retail' },
    { value: 'ecommerce', label: 'E-commerce' },
    // ... 9 industry options
];

// Geographic Hierarchy
Country → State/Province → City (optional)
```

#### Dynamic Geographic Loading
```typescript
// Country loading on mount
useEffect(() => {
    loadCountries(); // Fetch from /api/countries
}, []);

// State loading when country changes
useEffect(() => {
    if (selectedCountry) {
        loadSubdivisions(selectedCountry); // Fetch from /api/subdivisions/{country}
        setValue('state', ''); // Reset dependent field
    }
}, [selectedCountry]);
```

#### Forecast Settings
- **Frequency Options**: Daily, Weekly, Monthly with descriptions
- **Horizon Input**: 1-365 periods with dynamic unit display
- **Column Mapping**: Override auto-detected columns

#### Advanced Options
- **Holiday Integration**: Toggle country/state holidays
- **AI Adjustment**: Toggle macro economic adjustments
- **Privacy Notice**: Transparent data usage explanation

### 4. Analysis Module (`components/AnalysisModule.tsx`)

**Purpose**: Interactive historical data analysis with multi-year support.

**Data Processing Logic:**

#### Multi-Year Detection
```typescript
const processedData = useMemo(() => {
    const uniqueYears = [...new Set(parsedData.map(d => d.year))];
    const isMultiYear = uniqueYears.length > 1;

    if (isMultiYear) {
        // Multi-year aggregation and analysis
    } else {
        // Single-year detailed analysis
    }
});
```

#### Chart Configurations

**Multi-Year Mode:**
- **Yearly Bar Chart**: Annual sales comparison
- **Monthly Breakdown**: Filterable by year
- **Weekly Analysis**: Year-specific weekly patterns
- **Growth Trend**: Line chart showing year-over-year progression

**Single-Year Mode:**
- **Monthly Breakdown**: Detailed monthly analysis
- **Weekly Distribution**: All weeks of the year
- **Monthly Trend**: Line chart showing monthly progression

#### Interactive Features
- **Year Filter**: Dropdown for multi-year data
- **Responsive Charts**: Recharts with proper formatting
- **Tooltip Enhancement**: Localized number formatting

### 5. API Client (`api/client.ts`)

**Purpose**: Centralized API communication with comprehensive error handling.

**Configuration:**
```typescript
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 120000, // 2 minutes for forecast requests
});
```

**Request/Response Interceptors:**
- **Request Logging**: Debug API calls
- **Response Processing**: Structured error handling
- **HTTP Status Mapping**: User-friendly error messages

**Key Functions:**

#### `generateForecast(requestData)`
```typescript
async function generateForecast():
    1. Create FormData with file and parameters
    2. Send multipart/form-data request
    3. Handle long-running request (3-minute timeout)
    4. Return structured forecast response
```

#### Error Handling
- **413 (File Too Large)**: User-friendly file size message
- **422 (Validation Error)**: Data format guidance
- **500+ (Server Error)**: Generic retry message
- **Network Errors**: Connection-specific messaging

---

## 📊 Data Flow & API Endpoints

### Primary Data Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Upload    │───▶│   Config    │───▶│   Results   │
│   Module    │    │    Form     │    │  Dashboard  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│File Parsing │    │ API Request │    │Chart Render │
│& Validation │    │ Generation  │    │& Analysis   │
└─────────────┘    └─────────────┘    └─────────────┘
```

### API Endpoints

#### **POST /api/forecast**
**Main forecasting endpoint**

**Request Format:**
```typescript
Content-Type: multipart/form-data

// File
file: File (CSV/Excel, max 10MB)

// Form Fields
industry: string          // Industry category
country: string           // Country name or code
state?: string           // State/province (optional)
city?: string            // City name (optional)
freq: 'D' | 'W' | 'M'   // Forecast frequency
horizon: number          // Periods to forecast (1-365)
date_col: string         // Date column name
target_col: string       // Sales/target column name
apply_holidays: boolean  // Include holidays
apply_ai_adjustment: boolean // Apply AI adjustments
```

**Response Format:**
```typescript
{
    meta: {
        freq: string,
        train_start: string,        // Training period start
        train_end: string,          // Training period end
        horizon: number,
        holidays_used: string[],    // Applied holidays
        original_rows: number,      // Input data quality
        processed_rows: number,
        null_dates: number,
        null_targets: number
    },
    ai_adjustment?: {
        applied: boolean,
        adjustment_pct: number,     // ±20% bounded
        rationale: string,          // Business explanation
        sources: string[]           // Reference URLs
    },
    history: DataPoint[],           // Historical data
    forecast_base: DataPoint[],     // Prophet baseline
    forecast_final: DataPoint[]     // AI-adjusted forecast
}
```

#### **GET /api/countries**
**Geographic data for country selection**

**Response:**
```typescript
{
    countries: [
        { value: "US", label: "United States", code: "US" },
        { value: "IN", label: "India", code: "IN" },
        // ... more countries
    ]
}
```

#### **GET /api/subdivisions/{country_code}**
**State/province data for selected country**

**Response:**
```typescript
{
    subdivisions: [
        { value: "CA", label: "California", code: "CA", type: "state" },
        { value: "NY", label: "New York", code: "NY", type: "state" },
        // ... more subdivisions
    ]
}
```

#### **GET /api/health**
**Application health check**

**Response:**
```typescript
{ status: "healthy" }
```

### Internal Processing Flow

```
1. File Upload & Validation
   ├── File size check (≤10MB)
   ├── Format validation (.csv, .xlsx, .xls)
   └── Content parsing with encoding detection

2. Data Processing
   ├── Column mapping and validation
   ├── Date parsing with error handling
   ├── Numeric conversion for target values
   ├── Frequency aggregation (D/W/M)
   └── Data quality assessment

3. Holiday Integration (Optional)
   ├── Country/state mapping
   ├── Date range expansion
   └── Prophet-compatible DataFrame creation

4. Prophet Model Training
   ├── Seasonality configuration by frequency
   ├── Holiday integration
   ├── Multiplicative vs additive seasonality
   └── Model fitting with performance optimization

5. Base Forecast Generation
   ├── Future DataFrame creation
   ├── Prophet prediction
   └── Confidence intervals

6. AI Adjustment (Optional)
   ├── Recent performance summary calculation
   ├── Contextual prompt building
   ├── Perplexity Sonar API call
   ├── Response parsing and validation
   └── Bounded adjustment application (±20%)

7. Response Formatting
   ├── Data point conversion
   ├── Metadata compilation
   └── Structured JSON response
```

---

## 🧠 Component Logic Explanation

### Upload Flow Logic

**File Processing Pipeline:**
```typescript
// 1. File Validation
const validateFile = (file: File) => {
    // Check file extension
    // Validate file size
    // Return validation result
};

// 2. File Parsing
const parseFile = async (file: File) => {
    // Auto-detect encoding for CSV
    // Handle Excel files with SheetJS
    // Return structured preview
};

// 3. Column Detection
const detectColumns = (rows: any[]) => {
    // Analyze column names and values
    // Apply heuristic patterns
    // Calculate confidence scores
    // Return best matches
};
```

**Column Detection Heuristics:**

**Date Columns:**
```typescript
const DATE_PATTERNS = [
    /^date$/i, /^ds$/i, /order_date/i, /invoice_date/i,
    /day/i, /week/i, /month/i, /period/i, /timestamp/i
];

const isDateValue = (value: string) => {
    // Try parsing with various date formats
    // Check for ISO dates, US/EU formats
    // Return confidence score
};
```

**Sales/Target Columns:**
```typescript
const SALES_PATTERNS = [
    /^sales$/i, /^revenue$/i, /qty/i, /quantity/i,
    /amount/i, /gmv/i, /value/i, /total/i, /price/i
];

const isNumericValue = (value: string) => {
    // Check for numeric values
    // Handle currency symbols
    // Return confidence score
};
```

### Configuration Form Logic

**Dynamic Form Updates:**
```typescript
// Country change triggers state/province loading
useEffect(() => {
    if (selectedCountry) {
        loadSubdivisions(selectedCountry);
        setValue('state', ''); // Reset dependent field
    }
}, [selectedCountry]);

// Frequency change updates horizon description
const horizonDescription = useMemo(() => {
    const units = { D: 'days', W: 'weeks', M: 'months' };
    return `Number of ${units[selectedFreq]} to forecast`;
}, [selectedFreq]);
```

**Form Validation Rules:**
```typescript
const validationRules = {
    industry: { required: 'Industry is required' },
    country: { required: 'Country is required' },
    horizon: {
        required: 'Horizon is required',
        min: { value: 1, message: 'Must be at least 1' },
        max: { value: 365, message: 'Must be less than 365' }
    },
    date_col: { required: 'Date column is required' },
    target_col: { required: 'Target column is required' }
};
```

### Results Dashboard Logic

**Tab-based Navigation:**
```typescript
type ResultsTab = 'forecast' | 'analysis' | 'financial';

const TabContent = ({ activeTab, forecastResult }) => {
    switch (activeTab) {
        case 'forecast':
            return <ForecastDetails data={forecastResult} />;
        case 'analysis':
            return <AnalysisModule data={forecastResult.history} />;
        case 'financial':
            return <FinancialProjection data={forecastResult.forecast_final} />;
    }
};
```

**Data Export Logic:**
```typescript
const downloadExcel = () => {
    // Prepare forecast data with all series
    const forecastData = forecast_final.map((point, idx) => ({
        'Period': point.ds,
        'Baseline Forecast': basePoint.yhat,
        'Lower Bound': basePoint.yhat_lower,
        'Upper Bound': basePoint.yhat_upper,
        'AI Adjusted Forecast': point.yhat_final
    }));

    // Prepare AI insights as separate sheet
    const aiInsights = formatAIInsights(ai_adjustment);

    // Create multi-sheet Excel file
    downloadExcelMultiSheet([
        { data: forecastData, sheetName: 'Forecast Data' },
        { data: aiInsights, sheetName: 'AI Insights' }
    ]);
};
```

### Analysis Module Logic

**Multi-Year vs Single-Year Analysis:**
```typescript
const processData = useMemo(() => {
    const uniqueYears = [...new Set(data.map(d => new Date(d.ds).getFullYear()))];
    const isMultiYear = uniqueYears.length > 1;

    if (isMultiYear) {
        return {
            // Yearly aggregation for comparison
            yearlyData: aggregateByYear(data),
            // Monthly breakdown by year
            monthlyData: aggregateByMonth(data, true),
            // Growth trend analysis
            trendData: calculateYearOverYearTrend(data)
        };
    } else {
        return {
            // Detailed single-year analysis
            monthlyData: aggregateByMonth(data, false),
            weeklyData: aggregateByWeek(data),
            trendData: calculateMonthlyTrend(data)
        };
    }
}, [data]);
```

**Chart Configuration:**
```typescript
const ChartConfig = {
    responsive: true,
    tooltips: {
        formatter: (value) => value.toLocaleString(),
        labelStyle: { color: '#111827' }
    },
    axes: {
        x: { dataKey: 'period' },
        y: { tickFormatter: (value) => value.toLocaleString() }
    }
};
```

---

## 🔒 AI Integration & Privacy

### Privacy-First Design

**Data Protection Principles:**
1. **Local Processing**: All sales data processed server-side only
2. **No Raw Data to AI**: Only anonymized metadata sent to external AI
3. **Bounded Adjustments**: AI changes limited to ±20% maximum
4. **Transparent Usage**: Clear privacy notices in UI

### AI Adjustment Process

**Input to AI Model:**
```typescript
// Only these anonymized metrics are sent to AI
interface AIInput {
    industry: string;              // e.g., "retail"
    location: string;              // e.g., "California, United States"
    frequency: string;             // e.g., "weekly"
    horizon: number;               // e.g., 8
    recent_summary: {
        last4_growth_pct: number;      // Trend indicator
        yoy_last_period_pct: number;   // Seasonal comparison
        volatility_index: number;      // Risk indicator (0-1)
    };
    holidays_window: string[];     // e.g., ["Christmas", "New Year"]
}
```

**AI Processing:**
```typescript
const aiPrompt = `
You are a cautious forecaster. You never see raw sales data.
You only output a small adjustment percentage and a concise rationale.
Stay within ±20% total adjustment.

Context: ${industry} sector in ${location}
Recent pattern (anonymized): ${recent_summary}
Upcoming events: ${holidays}

Task: Provide bounded adjustment (-20 to +20) based on current macro signals.
`;
```

**Output Validation:**
```typescript
const validateAIResponse = (response: any) => {
    // Parse JSON response
    const adjustment = parseFloat(response.adjustment_pct);

    // Apply bounds checking
    const boundedAdjustment = Math.max(-20, Math.min(20, adjustment));

    // Validate rationale length
    const rationale = response.rationale?.substring(0, 200) || "Macro adjustment applied";

    return { adjustment_pct: boundedAdjustment, rationale, sources: response.sources || [] };
};
```

### Error Handling & Fallbacks

**AI Service Unavailable:**
```typescript
const handleAIFailure = (error: any) => {
    logger.error(`AI adjustment failed: ${error}`);

    return {
        applied: false,
        adjustment_pct: 0.0,
        rationale: `No reliable macro adjustment - ${error.message}`,
        sources: []
    };
};
```

**Graceful Degradation:**
- AI failure doesn't break forecast generation
- Users get base Prophet forecast even if AI fails
- Clear indication when AI adjustment wasn't applied

---

## 🚀 Local Development Setup

### Prerequisites

**System Requirements:**
- **Node.js**: Version 18 or higher
- **Python**: Version 3.11 or higher
- **Git**: For version control
- **Code Editor**: VS Code recommended

**Optional Tools:**
- **Docker**: For containerized development
- **Postman**: For API testing

### Backend Setup

#### 1. Environment Preparation

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 2. Dependencies Installation

```bash
# Install all required packages
pip install -r requirements.txt

# Key packages installed:
# - fastapi==0.104.1      # Web framework
# - uvicorn==0.24.0       # ASGI server
# - prophet==1.1.4        # Time series forecasting
# - pandas==2.1.3         # Data manipulation
# - numpy==1.24.3         # Numerical computing
# - httpx==0.25.2         # HTTP client for AI calls
# - python-multipart==0.0.6  # File upload support
# - holidays==0.36        # Holiday detection
# - python-dotenv==1.0.0  # Environment variables
```

#### 3. Environment Configuration

```bash
# Copy environment template
cp .env.sample .env

# Edit .env file with your settings
```

**Required Environment Variables:**
```env
# Perplexity AI API Key (required for AI adjustments)
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# Server Configuration
PORT=8000
HOST=0.0.0.0

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Logging Level
LOG_LEVEL=INFO
```

**Getting Perplexity API Key:**
1. Visit [Perplexity AI](https://www.perplexity.ai/)
2. Sign up/Login to your account
3. Navigate to API section
4. Generate new API key
5. Add to `.env` file

#### 4. Start Backend Server

```bash
# Development server with auto-reload
python main.py

# Alternative using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Backend Server Verification:**
- Health check: http://localhost:8000/health
- API documentation: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

### Frontend Setup

#### 1. Environment Preparation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Key packages installed:
# - react==18.2.0           # UI framework
# - typescript==5.2.2       # Type safety
# - @tanstack/react-query==5.8.4  # Server state
# - recharts==2.8.0         # Charts
# - react-hook-form==7.47.0 # Form management
# - axios==1.6.2            # HTTP client
# - lucide-react==0.294.0   # Icons
```

#### 2. Environment Configuration

```bash
# Copy environment template
cp .env.sample .env

# Edit .env file
```

**Required Environment Variables:**
```env
# Backend API URL
VITE_API_BASE_URL=http://localhost:8000/api

# Development settings
VITE_NODE_ENV=development
```

#### 3. Start Development Server

```bash
# Start Vite development server
npm run dev

# Alternative ports if 5173 is busy
npm run dev -- --port 3000

# Build for production
npm run build

# Preview production build
npm run preview
```

**Frontend Server Verification:**
- Application: http://localhost:5173
- Development tools: React Query DevTools accessible in browser

### Development Workflow

#### 1. Code Quality Setup

**Backend (Python):**
```bash
# Install development tools
pip install black flake8 isort mypy

# Format code
black .

# Lint code
flake8 .

# Sort imports
isort .

# Type checking
mypy .
```

**Frontend (TypeScript):**
```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Format with Prettier (if configured)
npm run format
```

#### 2. Testing Setup

**Backend Tests:**
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

**Frontend Tests:**
```bash
# Install test dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# Run tests
npm run test

# Run tests with coverage
npm run test:coverage
```

#### 3. API Testing

**Using cURL:**
```bash
# Health check
curl http://localhost:8000/health

# Countries endpoint
curl http://localhost:8000/api/countries

# Forecast endpoint (with file)
curl -X POST \
  -F "file=@sample-data.csv" \
  -F "industry=retail" \
  -F "country=United States" \
  -F "freq=W" \
  -F "horizon=8" \
  -F "date_col=date" \
  -F "target_col=sales" \
  -F "apply_holidays=true" \
  -F "apply_ai_adjustment=true" \
  http://localhost:8000/api/forecast
```

**Using Postman:**
1. Import API collection from `/docs` endpoint
2. Set up environment variables
3. Test individual endpoints
4. Save test scenarios

### Common Development Issues

#### Backend Issues

**Port Already in Use:**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
uvicorn main:app --port 8001
```

**Python Virtual Environment Issues:**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Missing Dependencies:**
```bash
# Update pip
pip install --upgrade pip

# Install specific package versions
pip install prophet==1.1.4 --no-cache-dir
```

#### Frontend Issues

**Node Modules Issues:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**TypeScript Errors:**
```bash
# Check TypeScript configuration
npx tsc --noEmit

# Update type definitions
npm install --save-dev @types/react @types/react-dom
```

**CORS Issues:**
```bash
# Verify backend CORS configuration
# Check ALLOWED_ORIGINS in backend .env
# Ensure frontend URL is included
```

### Development Best Practices

#### Code Organization
- **Backend**: Follow FastAPI project structure
- **Frontend**: Component-based architecture with TypeScript
- **Shared**: Consistent naming conventions

#### Version Control
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Commit with descriptive messages
git commit -m "feat: add AI adjustment bounds validation"

# Push and create pull request
git push origin feature/your-feature-name
```

#### Environment Management
- Never commit `.env` files
- Update `.env.sample` when adding new variables
- Document environment requirements

#### API Development
- Use Pydantic models for validation
- Include comprehensive error handling
- Document endpoints with docstrings
- Test with various input scenarios

#### Frontend Development
- Use TypeScript for type safety
- Implement error boundaries
- Follow accessibility guidelines
- Optimize for performance with React.memo

---

## 🧪 Testing & Deployment

### Testing Strategy

#### Backend Testing
```bash
# Unit tests for core functions
pytest tests/test_prophet_service.py -v

# Integration tests for API endpoints
pytest tests/test_forecast_api.py -v

# Load testing for file processing
pytest tests/test_performance.py -v
```

#### Frontend Testing
```bash
# Component unit tests
npm run test:unit

# Integration tests
npm run test:integration

# End-to-end tests
npm run test:e2e
```

### Production Deployment

#### Backend Deployment (Docker)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Deployment
```bash
# Build production bundle
npm run build

# Deploy to static hosting (Vercel, Netlify, etc.)
# Or serve with nginx
```

#### Environment Configuration
```env
# Production environment variables
PERPLEXITY_API_KEY=prod_key_here
ALLOWED_ORIGINS=https://yourdomain.com
LOG_LEVEL=WARNING
```

### Performance Considerations

#### Backend Optimization
- **Prophet Model Caching**: Cache trained models for similar datasets
- **File Processing**: Stream large files instead of loading entirely
- **Database Connection**: Use connection pooling for scalability
- **API Rate Limiting**: Implement rate limiting for production

#### Frontend Optimization
- **Code Splitting**: Lazy load components and routes
- **Bundle Analysis**: Monitor bundle size with webpack-bundle-analyzer
- **Caching**: Implement service worker for offline functionality
- **Performance Monitoring**: Use React DevTools Profiler

### Security Checklist

#### Backend Security
- ✅ **Input Validation**: Pydantic models validate all inputs
- ✅ **File Upload Security**: File type and size restrictions
- ✅ **CORS Configuration**: Restrictive CORS policy
- ✅ **Error Handling**: No sensitive data in error messages
- ✅ **Rate Limiting**: Implement in production
- ✅ **HTTPS**: Force HTTPS in production

#### Frontend Security
- ✅ **XSS Prevention**: React's built-in XSS protection
- ✅ **CSRF Protection**: Stateless API design
- ✅ **Content Security Policy**: Implement CSP headers
- ✅ **Dependency Scanning**: Regular security audits
- ✅ **Environment Variables**: Secure handling of API keys

### Monitoring & Logging

#### Backend Monitoring
```python
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Key metrics to monitor
# - Request latency
# - Error rates
# - Prophet model training time
# - AI API response times
```

#### Frontend Monitoring
- **Error Tracking**: Implement Sentry or similar
- **Performance Monitoring**: Core Web Vitals tracking
- **User Analytics**: Privacy-compliant usage tracking
- **Console Logging**: Structured logging for debugging

---

## 📝 Conclusion

This AI Demand Forecasting System provides a comprehensive, production-ready solution for business forecasting with the following key strengths:

### **Technical Excellence**
- **Scalable Architecture**: Modular design with clear separation of concerns
- **Type Safety**: Full TypeScript implementation with Pydantic validation
- **Performance Optimized**: Efficient data processing and responsive UI
- **Error Resilient**: Comprehensive error handling and graceful degradation

### **Business Value**
- **AI-Enhanced Accuracy**: Macro economic adjustments via Perplexity Sonar
- **Multi-Country Support**: Holidays and geographic context for 10+ countries
- **User-Friendly**: Intuitive step-by-step workflow with auto-detection
- **Privacy-First**: Local data processing with transparent AI usage

### **Developer Experience**
- **Well-Documented**: Comprehensive code documentation and setup guides
- **Testing Ready**: Test structure and validation examples
- **Deployment Ready**: Production configuration and security considerations
- **Extensible**: Modular design allows easy feature additions

The system is designed for collaboration, with clear component boundaries, consistent patterns, and extensive documentation to help new team members contribute effectively.

**Created by Sourabh**
*For questions or contributions, please refer to the project repository and documentation.*