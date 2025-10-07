# AI Demand Forecasting System

A comprehensive B2B sales forecasting solution combining Prophet time series modeling with AI-powered macro adjustments via Perplexity Sonar. Built with React + TypeScript frontend and FastAPI backend.

## 🚀 Features

### Core Functionality
- **File Upload**: Supports CSV and Excel files up to 10MB
- **Smart Column Detection**: Automatically identifies date and sales columns
- **Prophet Forecasting**: Industry-standard time series forecasting
- **AI Macro Adjustment**: Real-time economic context via Perplexity Sonar (±20% bounded)
- **Interactive Visualization**: Recharts-based charts with toggleable series
- **Data Export**: Download forecasts as CSV with multiple series

### Business Context
- **Industry Support**: Retail, E-commerce, CPG, Fashion, Electronics, etc.
- **Geographic Context**: Country/State/City for localized holidays and macro factors
- **Frequency Options**: Daily, Weekly, Monthly forecasting
- **Holiday Integration**: Automatic holiday detection for 10+ countries

### Privacy & Security
- Sales data never sent to external AI services
- Only anonymized metadata sent to Perplexity for macro insights
- Local processing with secure server-side modeling

## 🏗️ Architecture

### Frontend (React + TypeScript)
```
frontend/
├── src/
│   ├── components/
│   │   ├── UploadArea.tsx      # File upload with drag & drop
│   │   ├── ConfigForm.tsx      # Forecast configuration
│   │   ├── ForecastChart.tsx   # Interactive Recharts visualization
│   │   └── ResultsPanel.tsx    # KPIs, chart, and download
│   ├── lib/
│   │   ├── fileUtils.ts        # CSV/Excel parsing (PapaParse, SheetJS)
│   │   ├── detectColumns.ts    # Smart column detection heuristics
│   │   └── constants.ts        # Industries, frequencies, patterns
│   ├── api/
│   │   └── client.ts           # Axios API client with error handling
│   └── types/
│       └── index.ts            # TypeScript interfaces
```

### Backend (FastAPI + Python 3.11)
```
backend/
├── routers/
│   ├── forecast.py             # Main forecasting endpoint
│   └── ai_adjust.py            # AI adjustment service
├── services/
│   ├── prophet_service.py      # Prophet model training & prediction
│   ├── perplexity_client.py    # Perplexity Sonar integration
│   └── holidays_service.py     # Multi-country holiday support
├── models/
│   └── schemas.py              # Pydantic models
└── main.py                     # FastAPI app with CORS
```

## 🛠️ Setup & Installation

### Prerequisites
- Node.js 18+
- Python 3.11+
- Git

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**:
   ```bash
   cp .env.sample .env
   ```
   Edit `.env` and add:
   ```
   PERPLEXITY_API_KEY=your_perplexity_api_key_here
   PORT=8000
   ALLOWED_ORIGINS=http://localhost:5173
   ```

5. **Start the server**:
   ```bash
   python main.py
   ```
   Server runs at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Environment configuration**:
   ```bash
   cp .env.sample .env
   ```
   Edit `.env`:
   ```
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

4. **Start development server**:
   ```bash
   npm run dev
   ```
   App runs at `http://localhost:5173`

## 📊 Usage Workflow

### 1. Upload Data
- Drag & drop or browse for CSV/Excel files
- Automatic column detection for dates and sales
- Preview first 200 rows with data quality stats

### 2. Configure Forecast
- **Business Context**: Industry, Country, State, City
- **Forecast Settings**: Frequency (D/W/M), Horizon (1-365 periods)
- **Column Selection**: Override auto-detected columns if needed
- **Options**: Toggle holidays and AI adjustment

### 3. Generate & Analyze
- View interactive chart with historical data and forecasts
- Compare baseline vs AI-adjusted predictions
- Download CSV with all forecast series
- Review AI rationale and data quality metrics

## 🔧 API Endpoints

### `POST /api/forecast`
Generate sales forecast with optional AI adjustment.

**Request**: Multipart form with file + JSON fields
```json
{
  "industry": "retail",
  "country": "United States",
  "state": "California",
  "city": "San Francisco",
  "freq": "W",
  "horizon": 8,
  "date_col": "date",
  "target_col": "sales",
  "apply_holidays": true,
  "apply_ai_adjustment": true
}
```

**Response**:
```json
{
  "meta": {
    "freq": "W",
    "train_start": "2023-01-02",
    "train_end": "2024-12-30",
    "horizon": 8,
    "holidays_used": ["New Year's Day", "Christmas Day"]
  },
  "history": [{"ds": "2024-01-01", "y": 1234.5}],
  "forecast_base": [{"ds": "2025-01-06", "yhat": 1400.2}],
  "forecast_final": [{"ds": "2025-01-06", "yhat_final": 1295.2}],
  "ai_adjustment": {
    "applied": true,
    "adjustment_pct": -7.5,
    "rationale": "Consumer sentiment declining, inflation concerns"
  }
}
```

### `POST /api/ai-adjust`
Get AI-powered macro adjustment (internal service).

## 🌍 Supported Countries & Holidays

- **United States**: State-level holidays (all 50 states)
- **India**: National + state holidays (major states)
- **Canada**: Provincial holidays
- **United Kingdom**: National holidays
- **Australia**: National holidays
- **Germany, France, Japan, Brazil, Mexico**: National holidays

## 📋 Data Requirements

### File Formats
- **CSV**: UTF-8 or Latin-1 encoding
- **Excel**: .xlsx or .xls (first worksheet only)
- **Size Limit**: 10MB maximum

### Data Structure
- **Minimum**: 12 historical periods
- **Date Column**: Any recognizable date format
- **Sales Column**: Numeric values (sales, revenue, quantity)
- **Missing Data**: Automatically handled via interpolation

### Column Detection Patterns
**Date Columns**:
- date, ds, order_date, invoice_date, day, week, month, period, timestamp

**Sales Columns**:
- sales, revenue, qty, quantity, y, amount, gmv, value, total, price

## 🔒 Privacy & Security

### Data Protection
- Sales data processed server-side only for modeling
- No sales values sent to external AI services
- Only anonymized metadata sent to Perplexity:
  - Industry, location, forecast frequency, horizon
  - High-level trend patterns (growth %, volatility)
  - Upcoming holiday names

### Security Features
- CORS protection
- File type validation
- Input sanitization
- Error handling with no data leakage

## 🚀 Deployment

### Replit Deployment
1. **Backend**: Create Python Replit, upload backend files
2. **Frontend**: Create React Replit, upload frontend files
3. **Environment**: Set environment variables in Replit secrets
4. **Run**: Use provided run commands

### Production Considerations
- Set up proper environment variables
- Configure CORS for production domains
- Monitor API usage for Perplexity costs
- Consider adding authentication for sensitive data

## 🧪 Development

### Backend Testing
```bash
cd backend
python -m pytest tests/  # Add tests as needed
```

### Frontend Testing
```bash
cd frontend
npm run test
```

### Code Quality
```bash
# Backend
cd backend
black . && flake8 .

# Frontend
cd frontend
npm run lint && npm run type-check
```

## 📈 Performance & Limits

### File Processing
- **CSV**: ~50,000 rows in <5 seconds
- **Excel**: ~30,000 rows in <10 seconds
- **Prophet Training**: ~5,000 points in <30 seconds

### API Rate Limits
- **Perplexity**: Based on API key tier
- **Forecast Endpoint**: No built-in limits (add Redis for production)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open pull request


## 🆘 Troubleshooting

### Common Issues

**"Prophet training failed"**
- Ensure minimum 12 data points
- Check date column format
- Verify numeric target values

**"Perplexity API error"**
- Check API key validity
- Verify internet connection
- Review usage limits

**"Column detection failed"**
- Manually select date/sales columns
- Check data format consistency
- Ensure proper encoding (UTF-8)

**"File too large"**
- Compress data or filter to recent periods
- Use CSV instead of Excel for better performance
- Sample data if historical depth not critical

For additional support, please check the issues section or create a new issue with detailed error information.

---

**Built with ❤️ for better business forecasting**
