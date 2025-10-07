<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="mb-8">
      <div class="flex items-center gap-2 mb-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-soft-blue"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>
        <h3 class="text-xl font-bold text-dark-gray m-0">{{ title }}</h3>
      </div>
      <p class="text-dark-slate-gray text-sm">
        {{ processedData.isMultiYear ? `Analysis for ${processedData.years.length} years of data` : `Analysis for single year of data` }}
      </p>
    </div>

    <div v-if="!data || data.length === 0" class="text-center text-dark-slate-gray py-8">
      <p>No data available for analysis</p>
    </div>

    <div v-else>
      <!-- Multi-year charts -->
      <div v-if="processedData.isMultiYear" class="grid gap-10">
        <div>
          <h4 class="text-lg font-medium text-dark-gray mb-4">Sales per Year</h4>
          <div ref="yearlyBarChart" style="width: 100%; height: 300px;"></div>
        </div>
        <div v-if="selectedYear">
          <div class="flex justify-between items-center mb-4">
            <h4 class="text-lg font-medium text-dark-gray m-0">Monthly Sales for {{ selectedYear }}</h4>
            <select v-model="selectedYear" class="input-field">
              <option v-for="year in processedData.years" :key="year" :value="year">{{ year }}</option>
            </select>
          </div>
          <div ref="monthlyBarChart" style="width: 100%; height: 300px;"></div>
        </div>
        <div>
          <h4 class="text-lg font-medium text-dark-gray mb-4">Monthly Sales Trend (All Years)</h4>
          <div ref="monthlyLineChart" style="width: 100%; height: 300px;"></div>
        </div>
      </div>

      <!-- Single-year charts -->
      <div v-else class="grid gap-10">
        <div>
          <h4 class="text-lg font-medium text-dark-gray mb-4">Monthly Sales</h4>
          <div ref="monthlyBarChart" style="width: 100%; height: 300px;"></div>
        </div>
        <div>
          <h4 class="text-lg font-medium text-dark-gray mb-4">Monthly Sales Trend</h4>
          <div ref="singleYearMonthlyLineChart" style="width: 100%; height: 300px;"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: 'Sales Analysis'
  }
});

const yearlyBarChart = ref(null);
const monthlyBarChart = ref(null);
const monthlyLineChart = ref(null);
const singleYearMonthlyLineChart = ref(null);

let yearlyBarChartInstance = null;
let monthlyBarChartInstance = null;
let monthlyLineChartInstance = null;
let singleYearMonthlyLineChartInstance = null;

const selectedYear = ref(null);

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const processedData = computed(() => {
  if (!props.data || props.data.length === 0) {
    return { isMultiYear: false, years: [], yearlyData: [], monthlyDataByYear: new Map() };
  }

  const parsedData = props.data.map(point => ({ ...point, date: new Date(point.ds) }));
  const years = [...new Set(parsedData.map(d => d.date.getFullYear()))].sort().map(String);
  const isMultiYear = years.length > 1;

  const yearlyData = years.map(year => {
      const totalSales = parsedData
          .filter(d => d.date.getFullYear() === parseInt(year))
          .reduce((sum, d) => sum + (d.y || 0), 0);
      return { year: year, sales: Math.round(totalSales) };
  });

  const monthlyDataByYear = new Map();
  years.forEach(year => {
      const yearData = parsedData.filter(d => d.date.getFullYear() === parseInt(year));
      const monthlyAgg = new Array(12).fill(0);
      yearData.forEach(point => {
          const month = point.date.getMonth();
          monthlyAgg[month] += (point.y || 0);
      });
      monthlyDataByYear.set(year, monthlyAgg.map(s => Math.round(s)));
  });

  return { isMultiYear, years, yearlyData, monthlyDataByYear };
});

const reinitCharts = () => {
    nextTick(() => {
        if (yearlyBarChartInstance) yearlyBarChartInstance.dispose();
        if (monthlyBarChartInstance) monthlyBarChartInstance.dispose();
        if (monthlyLineChartInstance) monthlyLineChartInstance.dispose();
        if (singleYearMonthlyLineChartInstance) singleYearMonthlyLineChartInstance.dispose();

        const echartOptions = { renderer: 'svg' };
        if (yearlyBarChart.value) yearlyBarChartInstance = window.echarts.init(yearlyBarChart.value, 'light', echartOptions);
        if (monthlyBarChart.value) monthlyBarChartInstance = window.echarts.init(monthlyBarChart.value, 'light', echartOptions);
        if (monthlyLineChart.value) monthlyLineChartInstance = window.echarts.init(monthlyLineChart.value, 'light', echartOptions);
        if (singleYearMonthlyLineChart.value) singleYearMonthlyLineChartInstance = window.echarts.init(singleYearMonthlyLineChart.value, 'light', echartOptions);
        
        if (yearlyBarChartInstance) {
            yearlyBarChartInstance.on('click', (params) => {
                if (params.name) {
                    selectedYear.value = params.name;
                }
            });
        }

        updateCharts();
    });
};

watch(() => processedData.value.isMultiYear, (isMulti) => {
    if (isMulti && processedData.value.years.length > 0) {
        selectedYear.value = processedData.value.years[0];
    } else {
        selectedYear.value = null;
    }
    reinitCharts();
}, { immediate: true });

const chartBaseOptions = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, backgroundColor: '#FFFFFF', borderColor: '#E3F2FD', borderWidth: 1, textStyle: { color: '#333333' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', axisLine: { lineStyle: { color: '#d1d5db' } }, axisLabel: { color: '#2F4F4F' } },
    yAxis: { type: 'value', axisLabel: { color: '#2F4F4F' }, splitLine: { lineStyle: { color: '#F2F2F2' } } },
    textStyle: { fontFamily: 'inherit' }
};

const updateCharts = () => {
    if (!processedData.value) return;

    const { isMultiYear, years, yearlyData, monthlyDataByYear } = processedData.value;

    if (isMultiYear) {
        if (yearlyBarChartInstance) {
            yearlyBarChartInstance.setOption({
                ...chartBaseOptions,
                xAxis: { type: 'value', boundaryGap: [0, 0.01] },
                yAxis: { type: 'category', data: yearlyData.map(d => d.year) },
                series: [{ name: 'Sales', type: 'bar', data: yearlyData.map(d => d.sales), itemStyle: { color: '#4C8BF5' } }]
            });
        }

        if (monthlyBarChartInstance && selectedYear.value) {
            const monthlySales = monthlyDataByYear.get(selectedYear.value) || [];
            monthlyBarChartInstance.setOption({
                ...chartBaseOptions,
                xAxis: { ...chartBaseOptions.xAxis, data: MONTHS },
                series: [{ name: 'Sales', type: 'bar', data: monthlySales, itemStyle: { color: '#4CAF50' } }]
            });
        }

        if (monthlyLineChartInstance) {
            const series = years.map((year, index) => ({
                name: year.toString(),
                type: 'line',
                smooth: true,
                data: monthlyDataByYear.get(year.toString()) || [],
                itemStyle: { color: ['#4C8BF5', '#9C27B0', '#FF9800'][index % 3] }
            }));
            monthlyLineChartInstance.setOption({
                ...chartBaseOptions,
                tooltip: { ...chartBaseOptions.tooltip, trigger: 'axis' },
                legend: { data: years.map(y => y.toString()), textStyle: { color: '#2F4F4F' } },
                xAxis: { ...chartBaseOptions.xAxis, data: MONTHS },
                series: series
            });
        }

    } else {
        if (monthlyBarChartInstance && years.length > 0) {
            const year = years[0].toString();
            const monthlySales = monthlyDataByYear.get(year) || [];
            monthlyBarChartInstance.setOption({
                ...chartBaseOptions,
                xAxis: { ...chartBaseOptions.xAxis, data: MONTHS },
                series: [{ name: 'Sales', type: 'bar', data: monthlySales, itemStyle: { color: '#4C8BF5' } }]
            });
        }
        
        if (singleYearMonthlyLineChartInstance && years.length > 0) {
            const year = years[0].toString();
            const monthlySales = monthlyDataByYear.get(year) || [];
            singleYearMonthlyLineChartInstance.setOption({
                ...chartBaseOptions,
                tooltip: { ...chartBaseOptions.tooltip, trigger: 'axis' },
                xAxis: { ...chartBaseOptions.xAxis, data: MONTHS },
                series: [{ name: 'Sales', type: 'line', smooth: true, data: monthlySales, itemStyle: { color: '#4CAF50' } }]
            });
        }
    }
};

onMounted(reinitCharts);
watch(() => props.data, reinitCharts, { deep: true });
watch(selectedYear, updateCharts);

</script>

<style scoped>
.input-field {
    width: auto;
    padding: 0.5rem 1rem;
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
</style>
