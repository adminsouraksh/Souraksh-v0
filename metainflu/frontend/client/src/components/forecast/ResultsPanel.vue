<template>
    <div class="bg-white rounded-lg shadow-md">
        <!-- Header & Tabs -->
        <div class="border-b border-gray-200 px-6 py-4">
             <div class="flex justify-between items-start mb-4">
                <div>
                    <h3 class="text-xl font-bold text-dark-gray">Results Dashboard</h3>
                    <p class="text-dark-slate-gray text-sm">{{ data.meta.freq }}-frequency forecast for {{ data.meta.horizon }} periods</p>
                </div>
                <div class="flex gap-2">
                    <button class="btn-secondary" @click="$emit('go-back')">Reconfigure</button>
                    <button class="btn-secondary" @click="downloadCsv">Download CSV</button>
                    <button class="btn-purple" @click="$emit('reset')">Start Over</button>
                </div>
            </div>
            <!-- Tab Navigation -->
             <div class="flex gap-2 border-b border-gray-200 -mb-4">
                <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id" class="tab-button" :class="{ 'active-tab': activeTab === tab.id }">
                     <component :is="tab.icon" class="h-4 w-4"></component>
                    <span>{{ tab.name }}</span>
                </button>
            </div>
        </div>

        <!-- Tab Content -->
        <div class="p-6">
             <div v-if="activeTab === 'forecast'">
                
                <div class="mt-6" v-if="data.ai_adjustment.applied">
                    <h4 class="text-lg font-medium text-dark-gray mb-3">AI Macro Adjustment Applied</h4>
                    <div class="bg-light-blue border border-soft-blue rounded-lg p-4 text-sm">
                        <p class="text-dark-slate-gray mb-2"><strong>Adjustment:</strong> <span class="font-semibold">{{ data.ai_adjustment.adjustment_pct > 0 ? '+' : '' }}{{ data.ai_adjustment.adjustment_pct.toFixed(1) }}%</span></p>
                        <p class="text-dark-slate-gray mb-4"><strong>Business Insights:</strong><br>{{ data.ai_adjustment.rationale }}</p>
                        <div v-if="data.ai_adjustment.sources && data.ai_adjustment.sources.length > 0">
                            <p class="text-dark-slate-gray mb-2"><strong>Sources:</strong></p>
                            <ul class="list-disc list-inside space-y-1">
                                <li v-for="(source, index) in data.ai_adjustment.sources" :key="index">
                                    <a :href="source" target="_blank" rel="noopener noreferrer" class="text-soft-blue hover:underline">
                                        {{ source }}
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div class="mt-8">
                    <h4 class="text-lg font-medium text-dark-gray mb-3">Forecast Summary</h4>
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200 text-sm">
                            <thead class="bg-light-gray">
                                <tr>
                                    <th scope="col" class="px-6 py-3 text-left font-medium text-dark-slate-gray tracking-wider">Period</th>
                                    <th scope="col" class="px-6 py-3 text-left font-medium text-dark-slate-gray tracking-wider">Base Forecast</th>
                                    <th scope="col" class="px-6 py-3 text-left font-medium text-dark-slate-gray tracking-wider">AI Adjusted</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr v-for="item in summaryData" :key="item.ds" class="hover:bg-light-blue transition-colors duration-200">
                                    <td class="px-6 py-4 whitespace-nowrap text-dark-gray">{{ new Date(item.ds).toLocaleDateString() }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-dark-gray">{{ Math.round(item.yhat || 0).toLocaleString() }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-dark-gray font-semibold">{{ Math.round(item.yhat_final || item.yhat || 0).toLocaleString() }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Metadata -->
                <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div class="bg-white border border-gray-200 rounded-lg p-4">
                    <h3 class="text-sm font-semibold text-dark-gray mb-3">Forecast Details</h3>
                    <div class="space-y-2 text-xs">
                      <div class="flex justify-between">
                        <span class="font-medium text-dark-slate-gray">Frequency:</span>
                        <span class="text-dark-gray">{{ config.freq === 'D' ? 'Daily' : config.freq === 'W' ? 'Weekly' : 'Monthly' }}</span>
                      </div>
                      <div class="flex justify-between">
                          <span class="font-medium text-dark-slate-gray">Industry:</span>
                          <span class="text-dark-gray">{{ config.industry }}</span>
                      </div>
                      <div class="flex justify-between">
                          <span class="font-medium text-dark-slate-gray">Location:</span>
                          <span class="text-dark-gray text-right">{{ config.city ? `${config.city}, ` : '' }}{{ config.state ? `${config.state}, ` : '' }}{{ config.country }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="bg-white border border-gray-200 rounded-lg p-4">
                    <h3 class="text-sm font-semibold text-dark-gray mb-3">Data Quality</h3>
                    <div class="space-y-2 text-xs">
                      <div class="flex justify-between">
                        <span class="font-medium text-dark-slate-gray">Training Period:</span>
                        <span class="text-dark-gray">{{ new Date(data.meta.train_start).toLocaleDateString() }} to {{ new Date(data.meta.train_end).toLocaleDateString() }}</span>
                      </div>
                      <div v-if="data.meta.holidays_used && data.meta.holidays_used.length > 0" class="flex justify-between">
                        <span class="font-medium text-dark-slate-gray">Holidays:</span>
                        <span class="text-dark-gray">{{ data.meta.holidays_used.length }} included</span>
                      </div>
                    </div>
                  </div>
                </div>
             </div>
             <div v-if="activeTab === 'analysis'">
                 <AnalysisModule :data="data.history" title="Historical Data Analysis" />
             </div>
             <div v-if="activeTab === 'financial'">
                 <FinancialProjection :forecast-data="data.forecast_final.length > 0 ? data.forecast_final : data.forecast_base" :country="config.country" />
             </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineAsyncComponent, computed } from 'vue';
import AnalysisModule from './AnalysisModule.vue';
import FinancialProjection from './FinancialProjection.vue';

const props = defineProps({
    data: Object,
    config: Object,
});

defineEmits(['reset', 'go-back']);

const activeTab = ref('forecast');

const tabs = [
    { id: 'forecast', name: 'Forecast Details', icon: 'LineChartIcon' },
    { id: 'analysis', name: 'Data Analysis', icon: 'TrendingUpIcon' },
    { id: 'financial', name: 'Financial Projection', icon: 'DollarSignIcon' },
];

// Dummy components for icons
const LineChartIcon = defineAsyncComponent(async () => ({ template: '<div></div>' }));
const TrendingUpIcon = defineAsyncComponent(async () => ({ template: '<div></div>' }));
const DollarSignIcon = defineAsyncComponent(async () => ({ template: '<div></div>' }));

const summaryData = computed(() => {
    if (!props.data || !props.data.forecast_base) {
        return [];
    }
    const finalDataMap = new Map(
        (props.data.forecast_final || []).map(item => [item.ds, item])
    );
    return props.data.forecast_base.map(baseItem => {
        const finalItem = finalDataMap.get(baseItem.ds) || {};
        return {
            ds: baseItem.ds,
            yhat: baseItem.yhat,
            yhat_lower: finalItem.yhat_lower,
            yhat_upper: finalItem.yhat_upper,
            yhat_final: finalItem.yhat_final,
        };
    });
});

const downloadCsv = () => {
    const { history, forecast_base, forecast_final, ai_adjustment } = props.data;
    const dataMap = new Map();
    history.forEach(p => {
        dataMap.set(p.ds, { ds: p.ds, historical_sales: p.y });
    });
    forecast_base.forEach(p => {
        const entry = dataMap.get(p.ds) || { ds: p.ds };
        entry.baseline_forecast = p.yhat;
        dataMap.set(p.ds, entry);
    });
    if (ai_adjustment.applied) {
        forecast_final.forEach(p => {
            const entry = dataMap.get(p.ds) || { ds: p.ds };
            entry.ai_adjusted_forecast = p.yhat_final;
            dataMap.set(p.ds, entry);
        });
    }
    const sortedData = Array.from(dataMap.values()).sort((a, b) => new Date(a.ds) - new Date(b.ds));
    const headers = ['ds', 'historical_sales', 'baseline_forecast'];
    if (ai_adjustment.applied) {
        headers.push('ai_adjusted_forecast');
    }
    const csvRows = [headers.join(',')];
    sortedData.forEach(row => {
        const values = headers.map(header => row[header] || '');
        csvRows.push(values.join(','));
    });
    const csvContent = csvRows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', 'forecast_data.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};

</script>

<style scoped>
.tab-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  background-color: transparent;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #2F4F4F; /* dark-slate-gray */
  border-bottom: 2px solid transparent;
}
.tab-button.active-tab {
  color: #4C8BF5; /* soft-blue */
  font-weight: 600;
  border-bottom-color: #4C8BF5; /* soft-blue */
}
.tab-button:hover {
    background-color: #E3F2FD; /* light-blue */
}

.btn-secondary {
    padding: 0.5rem 1rem;
    background-color: #F2F2F2; /* light-gray */
    color: #333333; /* dark-gray */
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
}
.btn-secondary:hover {
    background-color: #e5e7eb;
}

.btn-purple {
    padding: 0.5rem 1rem;
    background-color: #9C27B0; /* cool-purple */
    color: white;
    border: none;
    border-radius: 0.375rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
}
.btn-purple:hover {
    background-color: #89229b;
}
</style>