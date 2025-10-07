<template>
  <div v-if="!forecastData || forecastData.length === 0" class="bg-white rounded-lg shadow-md p-8 text-center text-dark-slate-gray">
    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-4 text-muted-orange"><line x1="12" x2="12" y1="2" y2="22" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>
    <p>No forecast data available for financial projection</p>
  </div>

  <div v-else class="bg-white rounded-lg shadow-md p-6">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center gap-2 mb-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-soft-blue"><line x1="12" x2="12" y1="2" y2="22" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>
        <h3 class="text-xl font-bold text-dark-gray m-0">{{ title }}</h3>
      </div>
      <p class="text-dark-slate-gray text-sm">Calculate revenue and profitability based on forecast units</p>
    </div>

    <!-- Input Form -->
    <div class="bg-light-gray rounded-lg p-6 mb-8 border border-gray-200">
      <h4 class="text-lg font-medium text-dark-gray mb-4 flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2" /><line x1="8" x2="16" y1="6" y2="6" /><line x1="16" x2="16" y1="14" y2="18" /><line x1="8" x2="8" y1="10" y2="18" /><line x1="8" x2="16" y1="10" y2="10" /></svg>
        Financial Parameters
      </h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="form-label">Average Selling Price per Unit ({{ currency.symbol }})</label>
          <input type="number" :value="inputs.avgSellingPrice" @input="handleInputChange('avgSellingPrice', $event.target.value)" placeholder="e.g., 50.00" min="0" step="0.01" class="input-field" :class="{'border-red-500': errors.avgSellingPrice !== undefined}" />
          <p v-if="errors.avgSellingPrice !== undefined" class="error-text">Please enter a valid selling price greater than {{ currency.symbol }}0</p>
        </div>
        <div>
          <label class="form-label">Average Cost of Goods per Unit ({{ currency.symbol }})</label>
          <input type="number" :value="inputs.avgCostOfGoods" @input="handleInputChange('avgCostOfGoods', $event.target.value)" placeholder="e.g., 30.00" min="0" step="0.01" class="input-field" :class="{'border-red-500': errors.avgCostOfGoods !== undefined}" />
          <p v-if="errors.avgCostOfGoods !== undefined" class="error-text">Cost must be less than selling price and ≥ {{ currency.symbol }}0</p>
        </div>
      </div>
      <div v-if="isInputValid" class="mt-4 p-3 bg-green-100 rounded-md border border-vibrant-green">
        <p class="text-sm text-green-800">
          <strong>Gross Margin:</strong> {{ ((inputs.avgSellingPrice - inputs.avgCostOfGoods) / inputs.avgSellingPrice * 100).toFixed(2) }}%
          ({{ currency.symbol }}{{ (inputs.avgSellingPrice - inputs.avgCostOfGoods).toFixed(2) }} profit per unit)
        </p>
      </div>
    </div>

    <!-- Results -->
    <div v-if="financialMetrics.length > 0">
      <!-- Summary Cards -->
      <div v-if="isInputValid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div class="summary-card bg-light-blue border-soft-blue">
          <h4 class="summary-title text-soft-blue">Total Revenue</h4>
          <p class="summary-value text-soft-blue">{{ currency.symbol }}{{ summaryMetrics.totalRevenue.toLocaleString(undefined, { maximumFractionDigits: 0 }) }}</p>
        </div>
        <div class="summary-card bg-green-100 border-vibrant-green">
          <h4 class="summary-title text-vibrant-green">Total Gross Profit</h4>
          <p class="summary-value text-vibrant-green">{{ currency.symbol }}{{ summaryMetrics.totalProfit.toLocaleString(undefined, { maximumFractionDigits: 0 }) }}</p>
        </div>
        <div class="summary-card bg-orange-100 border-muted-orange">
          <h4 class="summary-title text-muted-orange">Total Units</h4>
          <p class="summary-value text-muted-orange">{{ summaryMetrics.totalUnits.toLocaleString() }}</p>
        </div>
        <div class="summary-card bg-purple-100 border-cool-purple">
          <h4 class="summary-title text-cool-purple">Average Margin</h4>
          <p class="summary-value text-cool-purple">{{ summaryMetrics.avgMargin.toFixed(1) }}%</p>
        </div>
      </div>

      <!-- Charts -->
      <div class="grid gap-8 mb-8">
        <div>
          <h4 class="section-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17" /><polyline points="16 7 22 7 22 13" /></svg>
            Revenue vs Profit by Period
          </h4>
          <div ref="financialChart" style="width: 100%; height: 400px;"></div>
        </div>

        <!-- Data Table Preview -->
        <div v-if="isInputValid">
          <div class="flex justify-between items-center mb-4">
            <h4 class="section-title m-0">Projection Preview</h4>
            <button @click="downloadFinancialProjection" class="btn-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" x2="12" y1="15" y2="3" /></svg>
              <span>Export CSV</span>
            </button>
          </div>
          <div class="bg-light-gray rounded-lg p-4 max-h-64 overflow-y-auto">
            <table class="min-w-full text-xs">
              <thead class="bg-gray-200">
                <tr>
                  <th class="table-header">Period</th>
                  <th class="table-header text-right">Units</th>
                  <th class="table-header text-right">Revenue</th>
                  <th class="table-header text-right">Profit</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="(item, idx) in financialMetrics.slice(0, 8)" :key="idx" class="hover:bg-gray-200">
                  <td class="table-cell">{{ item.period }}</td>
                  <td class="table-cell text-right">{{ item.salesUnits.toLocaleString() }}</td>
                  <td class="table-cell text-right">{{ currency.symbol }}{{ item.grossRevenue.toLocaleString(undefined, { maximumFractionDigits: 0 }) }}</td>
                  <td class="table-cell text-right text-vibrant-green font-medium">{{ currency.symbol }}{{ item.grossProfit.toLocaleString(undefined, { maximumFractionDigits: 0 }) }}</td>
                </tr>
              </tbody>
            </table>
            <p v-if="financialMetrics.length > 8" class="text-xs text-dark-slate-gray text-center mt-2">
              Showing first 8 of {{ financialMetrics.length }} periods
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, nextTick } from 'vue';

const props = defineProps({
  forecastData: { type: Array, default: () => [] },
  title: { type: String, default: 'Financial Projection' },
  country: { type: String, default: 'USA' }
});

const inputs = reactive({
  avgSellingPrice: null,
  avgCostOfGoods: null
});

const errors = reactive({
  avgSellingPrice: undefined,
  avgCostOfGoods: undefined
});

const financialChart = ref(null);
let chartInstance = null;

const currency = computed(() => {
  const currencySymbol = props.country === 'IN' ? '₹' : '$';
  const currencyName = props.country === 'IN' ? 'INR' : 'USD';
  return { symbol: currencySymbol, name: currencyName };
});

const validateInputs = (newInputs) => {
  const newErrors = {};
  if (!newInputs.avgSellingPrice || newInputs.avgSellingPrice <= 0) {
    newErrors.avgSellingPrice = true;
  } else {
    newErrors.avgSellingPrice = undefined;
  }

  if (newInputs.avgCostOfGoods < 0) {
    newErrors.avgCostOfGoods = true;
  } else if (newInputs.avgCostOfGoods >= newInputs.avgSellingPrice) {
    newErrors.avgCostOfGoods = true;
  } else {
     newErrors.avgCostOfGoods = undefined;
  }
  
  Object.assign(errors, newErrors);
};

const handleInputChange = (field, value) => {
  const numValue = parseFloat(value);
  inputs[field] = isNaN(numValue) ? null : numValue;
  validateInputs(inputs);
};

const isInputValid = computed(() => {
  return inputs.avgSellingPrice > 0 && inputs.avgCostOfGoods >= 0 && inputs.avgCostOfGoods < inputs.avgSellingPrice;
});

const financialMetrics = computed(() => {
  if (!isInputValid.value || !props.forecastData || props.forecastData.length === 0) {
    return [];
  }
  return props.forecastData.map(point => {
    const salesUnits = Math.round(point.yhat_final || point.yhat || 0);
    const grossRevenue = salesUnits * inputs.avgSellingPrice;
    const costOfGoods = salesUnits * inputs.avgCostOfGoods;
    const grossProfit = grossRevenue - costOfGoods;
    const grossMargin = grossRevenue > 0 ? (grossProfit / grossRevenue) * 100 : 0;
    return {
      period: new Date(point.ds).toLocaleDateString(),
      salesUnits,
      grossRevenue,
      costOfGoods,
      grossProfit,
      grossMargin
    };
  });
});

const summaryMetrics = computed(() => {
  if (financialMetrics.value.length === 0) {
    return { totalRevenue: 0, totalProfit: 0, totalUnits: 0, avgMargin: 0 };
  }
  const totalRevenue = financialMetrics.value.reduce((sum, item) => sum + item.grossRevenue, 0);
  const totalProfit = financialMetrics.value.reduce((sum, item) => sum + item.grossProfit, 0);
  const totalUnits = financialMetrics.value.reduce((sum, item) => sum + item.salesUnits, 0);
  const avgMargin = totalRevenue > 0 ? (totalProfit / totalRevenue) * 100 : 0;
  return { totalRevenue, totalProfit, totalUnits, avgMargin };
});

const downloadFinancialProjection = () => {
  if (financialMetrics.value.length === 0) return;

  const exportData = financialMetrics.value.map(item => ({
    'Period': item.period,
    'Sales Units': item.salesUnits,
    'Gross Revenue': item.grossRevenue.toFixed(2),
    'Cost of Goods Sold': item.costOfGoods.toFixed(2),
    'Gross Profit': item.grossProfit.toFixed(2),
    'Gross Margin %': item.grossMargin.toFixed(2)
  }));

  exportData.push({
    'Period': 'TOTAL',
    'Sales Units': summaryMetrics.value.totalUnits,
    'Gross Revenue': summaryMetrics.value.totalRevenue.toFixed(2),
    'Cost of Goods Sold': (summaryMetrics.value.totalRevenue - summaryMetrics.value.totalProfit).toFixed(2),
    'Gross Profit': summaryMetrics.value.totalProfit.toFixed(2),
    'Gross Margin %': summaryMetrics.value.avgMargin.toFixed(2)
  });

  const headers = Object.keys(exportData[0]);
  const csvContent = [
    headers.join(','),
    ...exportData.map(row => Object.values(row).join(','))
  ].join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.setAttribute('download', `financial_projection_${new Date().toISOString().split('T')[0]}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const updateChart = () => {
  if (!financialChart.value) {
    if (chartInstance && !chartInstance.isDisposed()) {
      chartInstance.dispose();
    }
    chartInstance = null;
    return;
  }

  if ((!chartInstance || chartInstance.isDisposed()) && window.echarts) {
    chartInstance = window.echarts.init(financialChart.value, 'light', { renderer: 'svg' });
  }

  if (!chartInstance) return;

  const metrics = financialMetrics.value;
  const showData = isInputValid.value && metrics.length > 0;

  chartInstance.setOption({
    tooltip: { 
      trigger: 'axis',
      formatter: (params) => {
        if (!params || params.length === 0) return '';
        let tooltip = `${params[0].axisValue}<br/>`;
        params.forEach(param => {
          tooltip += `${param.marker} ${param.seriesName}: ${currency.value.symbol}${(param.value || 0).toLocaleString(undefined, {maximumFractionDigits: 0})}<br/>`;
        });
        return tooltip;
      },
      backgroundColor: '#FFFFFF',
      borderColor: '#E3F2FD',
      borderWidth: 1,
      textStyle: { color: '#333333' }
    },
    legend: { data: ['Gross Revenue', 'Gross Profit'], bottom: 0, textStyle: { color: '#2F4F4F' } },
    grid: { top: '10%', left: '3%', right: '4%', bottom: '10%', containLabel: true },
    xAxis: { 
      type: 'category', 
      data: showData ? metrics.map(d => d.period) : [],
      axisLine: { lineStyle: { color: '#d1d5db' } },
      axisLabel: { color: '#2F4F4F' }
    },
    yAxis: { 
      type: 'value', 
      axisLabel: { 
        formatter: (value) => `${currency.value.symbol}${(value / 1000).toFixed(0)}K`,
        color: '#2F4F4F'
      },
      splitLine: { lineStyle: { color: '#F2F2F2' } }
    },
    series: [
      { 
        name: 'Gross Revenue', 
        type: 'bar', 
        data: showData ? metrics.map(d => d.grossRevenue) : [], 
        itemStyle: { color: '#4C8BF5', borderRadius: [4, 4, 0, 0] } 
      },
      { 
        name: 'Gross Profit', 
        type: 'bar', 
        data: showData ? metrics.map(d => d.grossProfit) : [], 
        itemStyle: { color: '#4CAF50', borderRadius: [4, 4, 0, 0] } 
      }
    ]
  }, true);
};

onMounted(() => {
  nextTick(updateChart);
});

watch(inputs, () => {
  nextTick(updateChart);
});

watch(financialMetrics, () => {
  nextTick(updateChart);
});

watch(() => props.forecastData, () => {
  nextTick(updateChart);
});
</script>

<style scoped>
.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #2F4F4F;
  margin-bottom: 0.5rem;
}
.input-field {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background-color: #F2F2F2;
  color: #333333;
  transition: border-color 0.2s;
}
.input-field:focus {
  outline: none;
  border-color: #4C8BF5;
  box-shadow: 0 0 0 2px rgba(76, 139, 245, 0.2);
}
.error-text {
  font-size: 0.75rem;
  color: #dc2626;
  margin-top: 0.25rem;
}
.summary-card {
  padding: 1rem;
  border-radius: 0.5rem;
  border-width: 1px;
}
.summary-title {
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}
.summary-value {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
}
.section-title {
  color: #333333;
  font-size: 1.125rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #4C8BF5;
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.btn-primary:hover {
  background-color: #3a7bd5;
}
.table-header {
  padding: 0.5rem;
  text-align: left;
  font-weight: 500;
  color: #2F4F4F;
}
.table-cell {
  padding: 0.5rem;
  color: #333333;
}
</style>