<template>
  <div>
    <div ref="chart" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';

const props = defineProps({
  history: {
    type: Array,
    required: true,
  },
  forecastBase: {
    type: Array,
    required: true,
  },
  forecastFinal: {
    type: Array,
    required: true,
  },
  aiAdjustment: {
    type: Object,
    required: true,
  }
});

const chart = ref(null);
let chartInstance = null;

const initChart = () => {
  if (chart.value && window.echarts) {
    chartInstance = window.echarts.init(chart.value, 'light', { renderer: 'svg' });
    updateChart();
  }
};

const updateChart = () => {
  if (!chartInstance) return;

  const historyData = props.history.map(p => [p.ds, p.y]);
  const forecastBaseData = props.forecastBase.map(p => [p.ds, p.yhat]);
  
  const series = [
    {
      name: 'Historical Sales',
      type: 'line',
      data: historyData,
      itemStyle: { color: '#2F4F4F' }, // dark-slate-gray
      lineStyle: { width: 2 },
    },
    {
      name: 'Baseline Forecast',
      type: 'line',
      smooth: true,
      data: forecastBaseData,
      itemStyle: { color: '#FF9800' }, // muted-orange
      lineStyle: { type: 'dashed' },
    },
  ];

  if (props.aiAdjustment.applied && props.forecastFinal.length > 0) {
    const forecastFinalData = props.forecastFinal.map(p => [p.ds, p.yhat_final]);
    series.push({
      name: 'AI-Adjusted Forecast',
      type: 'line',
      smooth: true,
      data: forecastFinalData,
      itemStyle: { color: '#4C8BF5' }, // soft-blue
      lineStyle: { width: 3 },
      areaStyle: {
        color: new window.echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(76, 139, 245, 0.3)' }, // soft-blue with opacity
          { offset: 1, color: 'rgba(76, 139, 245, 0)' }
        ])
      }
    });
  }

  chartInstance.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      backgroundColor: '#FFFFFF',
      borderColor: '#E3F2FD',
      borderWidth: 1,
      textStyle: {
        color: '#333333'
      }
    },
    legend: {
      data: series.map(s => s.name),
      bottom: 0,
      textStyle: {
        color: '#2F4F4F'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'time',
      boundaryGap: false,
      axisLine: {
        lineStyle: {
          color: '#d1d5db'
        }
      },
      axisLabel: {
        color: '#2F4F4F'
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value}',
        color: '#2F4F4F'
      },
      splitLine: {
        lineStyle: {
          color: '#F2F2F2'
        }
      }
    },
    series: series
  });
};

onMounted(() => {
  nextTick(initChart);
});

watch(() => [props.history, props.forecastBase, props.forecastFinal], () => {
  nextTick(updateChart);
}, { deep: true });

</script>
