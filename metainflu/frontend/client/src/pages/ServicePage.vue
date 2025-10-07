<template>
  <div class="min-h-screen font-sans bg-white text-gray-900">
    <!-- Navbar -->
    <Navbar />

    <!-- Hero -->
    <header class="pt-28 pb-16 bg-gradient-to-b from-white to-gray-50 text-center">
      <div class="max-w-3xl mx-auto px-6">
        <h1 class="text-4xl sm:text-5xl font-extrabold leading-tight mb-4">
          Our <span class="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">Services</span>
        </h1>
        <p class="text-gray-600 max-w-xl mx-auto">
          Explore interactive demos of our core services. See how Souraksh can empower your business with data-driven insights.
        </p>
      </div>
    </header>

    <!-- Interactive Demos Section -->
    <section class="py-16">
      <div class="max-w-7xl mx-auto px-6 space-y-12">

        <!-- 1. Demand Forecasting Demo -->
        <div class="p-8 bg-white border border-gray-200 rounded-2xl shadow-sm">
          <h2 class="text-2xl font-bold text-center mb-2">Demand Forecasting</h2>
          <p class="text-center text-gray-600 max-w-2xl mx-auto mb-8">Predict future demand with our AI-powered forecasting model. Click below to see a sample forecast visualization.</p>
          <div class="max-w-4xl mx-auto">
            <div ref="forecastChart" class="w-full h-96 bg-gray-50 rounded-lg p-4"></div>
            <div class="text-center mt-6">
              <button @click="generateForecast" class="px-6 py-3 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition">
                Generate Sample Forecast
              </button>
            </div>
          </div>
        </div>

        <!-- 2. Revenue Estimation Demo -->
        <div class="p-8 bg-white border border-gray-200 rounded-2xl shadow-sm">
          <h2 class="text-2xl font-bold text-center mb-2">Revenue Estimation</h2>
          <p class="text-center text-gray-600 max-w-2xl mx-auto mb-8">Adjust the sliders to see how changes in sales volume and price can impact your revenue.</p>
          <div class="max-w-2xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div class="space-y-6">
              <div>
                <label class="block font-medium">Forecasted Units Sold: <span class="font-bold text-indigo-600">{{ revenueInputs.units.toLocaleString() }}</span></label>
                <input type="range" min="1000" max="100000" step="100" v-model.number="revenueInputs.units" class="w-full mt-2">
              </div>
              <div>
                <label class="block font-medium">Average Price per Unit: <span class="font-bold text-indigo-600">${{ revenueInputs.price.toFixed(2) }}</span></label>
                <input type="range" min="5" max="500" step="0.5" v-model.number="revenueInputs.price" class="w-full mt-2">
              </div>
            </div>
            <div class="text-center bg-indigo-50 p-8 rounded-lg">
              <h3 class="text-gray-600">Estimated Revenue</h3>
              <p class="text-4xl font-extrabold text-indigo-700 mt-2">
                ${{ estimatedRevenue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
              </p>
            </div>
          </div>
        </div>

        <!-- 3. Profitability Analysis Demo -->
        <div class="p-8 bg-white border border-gray-200 rounded-2xl shadow-sm">
          <h2 class="text-2xl font-bold text-center mb-2">Profitability Analysis</h2>
          <p class="text-center text-gray-600 max-w-2xl mx-auto mb-8">Enter your financials to see a breakdown of your profit margins.</p>
          <div class="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
            <div class="space-y-4">
              <div>
                <label class="block font-medium text-sm">Total Revenue ($)</label>
                <input type="number" v-model.number="profitInputs.revenue" placeholder="e.g., 500000" class="mt-1 w-full px-4 py-2 rounded-lg border border-gray-300">
              </div>
              <div>
                <label class="block font-medium text-sm">Cost of Goods Sold (COGS) ($)</label>
                <input type="number" v-model.number="profitInputs.cogs" placeholder="e.g., 200000" class="mt-1 w-full px-4 py-2 rounded-lg border border-gray-300">
              </div>
              <div>
                <label class="block font-medium text-sm">Operating Expenses ($)</label>
                <input type="number" v-model.number="profitInputs.expenses" placeholder="e.g., 150000" class="mt-1 w-full px-4 py-2 rounded-lg border border-gray-300">
              </div>
            </div>
            <div class="space-y-4">
              <div class="bg-green-50 p-4 rounded-lg text-center">
                <h3 class="text-green-800 font-semibold">Gross Profit</h3>
                <p class="text-2xl font-bold text-green-700 mt-1">${{ profitAnalysis.grossProfit.toLocaleString() }}</p>
                <p class="text-sm text-green-600">({{ profitAnalysis.grossMargin }}% Margin)</p>
              </div>
              <div class="bg-blue-50 p-4 rounded-lg text-center">
                <h3 class="text-blue-800 font-semibold">Net Profit</h3>
                <p class="text-2xl font-bold text-blue-700 mt-1">${{ profitAnalysis.netProfit.toLocaleString() }}</p>
                 <p class="text-sm text-blue-600">({{ profitAnalysis.netMargin }}% Margin)</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue';
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';

// For ECharts
let echarts;
const forecastChart = ref(null);
let myChart = null;

// Demo 1: Demand Forecasting
const generateForecast = () => {
  if (!myChart) return;
  
  const baseData = Array.from({ length: 12 }, (_, i) => 1000 + (i * 50) + (Math.random() * 300));
  const forecastData = Array.from({ length: 6 }, (_, i) => 1600 + (i * 60) + (Math.random() * 400));
  
  myChart.setOption({
    series: [
      { data: baseData },
      { data: Array(11).fill(null).concat([baseData[11]]).concat(forecastData) }
    ]
  });
};

const initChart = () => {
    if (forecastChart.value && !myChart) {
      myChart = echarts.init(forecastChart.value);
      myChart.setOption({
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'] },
        yAxis: { type: 'value', name: 'Units Sold' },
        series: [
          { name: 'Historical', type: 'line', data: [], smooth: true },
          { name: 'Forecast', type: 'line', smooth: true, lineStyle: { type: 'dashed' }, data: [] }
        ],
        grid: { left: '10%', right: '5%', bottom: '10%' },
        legend: { data: ['Historical', 'Forecast'], top: 10 }
      });
    }
}

// Demo 2: Revenue Estimation
const revenueInputs = reactive({
  units: 50000,
  price: 120.50
});
const estimatedRevenue = computed(() => revenueInputs.units * revenueInputs.price);

// Demo 3: Profitability Analysis
const profitInputs = reactive({
  revenue: 500000,
  cogs: 200000,
  expenses: 150000
});
const profitAnalysis = computed(() => {
  const grossProfit = profitInputs.revenue - profitInputs.cogs;
  const netProfit = grossProfit - profitInputs.expenses;
  const grossMargin = profitInputs.revenue > 0 ? ((grossProfit / profitInputs.revenue) * 100).toFixed(1) : 0;
  const netMargin = profitInputs.revenue > 0 ? ((netProfit / profitInputs.revenue) * 100).toFixed(1) : 0;
  return { grossProfit, netProfit, grossMargin, netMargin };
});


onMounted(() => {
  // Check if ECharts is available on the window object from the CDN script
  if (typeof window.echarts !== 'undefined') {
    echarts = window.echarts;
    nextTick(() => {
      initChart();
    });
  } else {
    console.error('ECharts library not found. Please ensure the CDN script in index.html is loaded.');
  }
});

</script>

<style scoped>
/* Basic styling for range inputs */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 5px;
  outline: none;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #4f46e5;
  cursor: pointer;
  border-radius: 50%;
}
input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #4f46e5;
  cursor: pointer;
  border-radius: 50%;
}
</style>

