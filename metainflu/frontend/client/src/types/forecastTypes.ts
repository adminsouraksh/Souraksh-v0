// File: frontend/client/src/types/forecastTypes.ts
export interface UploadState {
  file: File | null;
  preview: FilePreview | null;
  detectedColumns: { 
    date: ColumnDetection | null; 
    target: ColumnDetection | null 
  };
  isProcessing: boolean;
  error: string | null;
}

export interface ConfigFormData {
  industry: string;
  country: string;
  state?: string;
  city?: string;
  freq: 'D' | 'W' | 'M';
  horizon: number;
  date_col: string;
  target_col: string;
  apply_holidays: boolean;
  apply_ai_adjustment: boolean;
}

export interface Country {
    value: string;
    label: string;
}

export interface Subdivision {
    value: string;
    label: string;
}

export interface ForecastDataPoint {
    ds: string;
    y?: number;
    yhat?: number;
    yhat_lower?: number;
    yhat_upper?: number;
    yhat_final?: number;
}

export interface ForecastResponse {
    meta: {
        freq: string;
        train_start: string;
        train_end: string;
        horizon: number;
        holidays_used: string[];
        original_rows: number;
        processed_rows: number;
        null_dates: number;
        null_targets: number;
    };
    ai_adjustment: {
        applied: boolean;
        adjustment_pct?: number;
        rationale?: string;
        sources?: string[];
    };
    history: ForecastDataPoint[];
    forecast_base: ForecastDataPoint[];
    forecast_final: ForecastDataPoint[];
}

export interface FilePreview {
  columns: string[];
  rows: Record<string, any>[];
  total_rows: number;
}

export interface ColumnDetection {
  name: string;
  confidence: number;
}
