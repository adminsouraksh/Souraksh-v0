<template>
  <div>
    <Navbar />
    <div class="min-h-[90vh] bg-light-gray">
        <!-- Header -->
        <div class="bg-white border-b border-gray-200 py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center gap-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-soft-blue">
              <path d="M3 3v18h18" /><path d="M18 17V9" /><path d="M13 17V5" /><path d="M8 17v-3" />
            </svg>
            <div>
              <h1 class="text-2xl font-bold text-dark-gray">
                AI Sales Forecasting
              </h1>
              <p class="text-dark-slate-gray mt-1 text-sm">
                Upload data → Configure → Generate forecast with AI adjustment
              </p>
            </div>
          </div>
        </div>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <SimpleUploadArea 
            v-if="currentStep === 'upload'" 
            :upload-state="uploadState" 
            @update:upload-state="Object.assign(uploadState, $event)" 
            @file-processed="handleFileProcessed" 
          />

          <div v-if="currentStep === 'configure' && uploadState.preview">
            <ConfigForm 
              :preview="uploadState.preview" 
              :detected-columns="uploadState.detectedColumns"
              :is-loading="isGeneratingForecast" 
              @submit="handleConfigSubmit" 
            />

            <div v-if="forecastError" class="mt-4 bg-orange-100 border border-muted-orange text-muted-orange rounded-md p-3">
              <div class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2">
                  <circle cx="12" cy="12" r="10" /><line x1="12" x2="12" y1="8" y2="12" /><line x1="12" x2="12.01" y1="16" y2="16" />
                </svg>
                <span class="text-sm">
                  {{ forecastError }}
                </span>
              </div>
            </div>
          </div>

          <ResultsPanel 
            v-if="currentStep === 'results' && forecastResult && configData" 
            :data="forecastResult" 
            :config="configData" 
            @reset="resetApp"
            @go-back="goBackToConfig"
          />
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import Navbar from '../components/Navbar.vue';
import SimpleUploadArea from '../components/forecast/SimpleUploadArea.vue';
import ConfigForm from '../components/forecast/ConfigForm.vue';
import ResultsPanel from '../components/forecast/ResultsPanel.vue';
import { generateForecast } from '../services/forecastService';
import { formatApiError } from '../lib/forecastUtils';

const currentStep = ref('upload');

const uploadState = reactive({
  file: null,
  preview: null,
  detectedColumns: { date: null, target: null },
  isProcessing: false,
  error: null,
});

const isGeneratingForecast = ref(false);
const forecastResult = ref(null);
const forecastError = ref(null);
const configData = ref(null);

const resetApp = () => {
  currentStep.value = 'upload';
  Object.assign(uploadState, {
    file: null,
    preview: null,
    detectedColumns: { date: null, target: null },
    isProcessing: false,
    error: null,
  });
  forecastResult.value = null;
  forecastError.value = null;
  isGeneratingForecast.value = false;
  configData.value = null;
};

const goBackToConfig = () => {
  currentStep.value = 'configure';
  forecastResult.value = null;
};
const handleFileProcessed = (file, preview, detectedColumns) => {
  uploadState.file = file;
  uploadState.preview = preview;
  uploadState.detectedColumns = detectedColumns;
  currentStep.value = 'configure';
};

const handleConfigSubmit = async (formData) => {
  if (!uploadState.file) return;

  configData.value = formData;
  isGeneratingForecast.value = true;
  forecastError.value = null;

  try {
    const result = await generateForecast({
      file: uploadState.file,
      ...formData
    });
    forecastResult.value = result;
    currentStep.value = 'results';
  } catch (error) {
    console.error('Forecast generation failed:', error);
    forecastError.value = formatApiError(error);
    // Go back to config on error to allow user to fix settings
    currentStep.value = 'configure'; 
  } finally {
    isGeneratingForecast.value = false;
  }
};
</script>

<style>
/* Global styles can be added here if needed, but prefer Tailwind classes. */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>