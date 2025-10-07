import Papa from 'papaparse';
import * as XLSX from 'xlsx';

// --- File Parsing ---

const parseCsv = (file) => {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      preview: 100, // Parse only the first 100 rows for preview
      complete: (results) => {
        if (results.errors.length) {
          reject(new Error(`CSV parsing error: ${results.errors[0].message}`));
        } else {
          resolve({
            columns: results.meta.fields,
            rows: results.data,
          });
        }
      },
      error: (error) => {
        reject(new Error(`CSV parsing failed: ${error.message}`));
      },
    });
  });
};

const parseXlsx = async (file) => {
    const data = await file.arrayBuffer();
    const workbook = XLSX.read(data, { type: 'array' });
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '', raw: false });

    if (rows.length === 0) {
        return { columns: [], rows: [] };
    }

    const header = rows[0];
    const body = rows.slice(1, 101); // Preview first 100 rows

    const formattedRows = body.map(row => {
        const rowObject = {};
        header.forEach((col, index) => {
            rowObject[col] = row[index];
        });
        return rowObject;
    });

    return {
        columns: header,
        rows: formattedRows,
    };
};


export const fileUtils = {
    parseFile: async (file) => {
        const extension = file.name.split('.').pop().toLowerCase();
        let result;

        if (extension === 'csv') {
            result = await parseCsv(file);
        } else if (['xlsx', 'xls'].includes(extension)) {
            result = await parseXlsx(file);
        } else {
            throw new Error('Unsupported file type. Please upload a CSV or Excel file.');
        }
        
        // For simplicity, we are not getting total_rows anymore.
        // This can be added later if needed by parsing the whole file.
        return { ...result, total_rows: '100+' };
    },
    validateFileName: (name) => /\.(csv|xlsx|xls)$/i.test(name),
    formatFileSize: (bytes) => `${(bytes / 1024).toFixed(2)} KB`,
};


// --- Column Detection ---

const DATE_COLUMN_KEYWORDS = ['date', 'day', 'time', 'period', 'dt', 'ds'];
const NUMERIC_TARGET_KEYWORDS = ['sale', 'revenue', 'total', 'value', 'units', 'quantity', 'amount', 'price'];

// Basic check if a value could be a date
const isDate = (s) => {
    if (!s) return false;
    // Attempt to parse the string as a date. This is a simple check.
    // For more robust validation, a library like moment.js or date-fns could be used.
    const date = new Date(s);
    return !isNaN(date.getTime());
};

// Basic check if a value is numeric
const isNumeric = (s) => {
    if (s === null || s === '') return false;
    return !isNaN(Number(s));
}

export const columnDetection = {
    analyzeColumns: (rows) => {
        if (!rows || rows.length === 0) return [];
        const columns = Object.keys(rows[0]);
        const analysis = {};

        columns.forEach(col => {
            analysis[col] = {
                numericCount: 0,
                dateCount: 0,
            };
        });

        rows.forEach(row => {
            for (const col of columns) {
                const value = row[col];
                if (isNumeric(value)) {
                    analysis[col].numericCount++;
                }
                if (isDate(value)) {
                    analysis[col].dateCount++;
                }
            }
        });

        return Object.entries(analysis).map(([name, counts]) => ({
            name,
            isNumeric: counts.numericCount / rows.length > 0.8,
            isDate: counts.dateCount / rows.length > 0.8,
        }));
    },

    detectDateColumn: (columnInfo) => {
        let bestGuess = null;
        let maxScore = -1;

        columnInfo.forEach(col => {
            let score = 0;
            const lowerCaseName = col.name.toLowerCase();

            // Score based on name
            if (DATE_COLUMN_KEYWORDS.some(kw => lowerCaseName.includes(kw))) {
                score += 0.5;
            }

            // Score based on data type
            if (col.isDate) {
                score += 0.5;
            }

            if (score > maxScore) {
                maxScore = score;
                bestGuess = col;
            }
        });
        
        return bestGuess ? { name: bestGuess.name, confidence: maxScore } : null;
    },

    detectTargetColumn: (columnInfo) => {
        let bestGuess = null;
        let maxScore = -1;

        columnInfo.forEach(col => {
            // Exclude date columns from being target columns
            if (col.isDate) return;

            let score = 0;
            const lowerCaseName = col.name.toLowerCase();

            // Score based on name
            if (NUMERIC_TARGET_KEYWORDS.some(kw => lowerCaseName.includes(kw))) {
                score += 0.5;
            }

            // Score based on data type
            if (col.isNumeric) {
                score += 0.5;
            }

            if (score > maxScore) {
                maxScore = score;
                bestGuess = col;
            }
        });

        return bestGuess ? { name: bestGuess.name, confidence: maxScore } : null;
    },
};

export function formatApiError(error) {
    if (error.response && error.response.data && error.response.data.detail) {
        return `Error: ${error.response.data.detail}`;
    }
    return error instanceof Error ? error.message : 'An unknown error occurred.';
}