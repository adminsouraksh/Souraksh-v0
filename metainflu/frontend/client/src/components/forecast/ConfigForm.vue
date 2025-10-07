<template>
  <div class="bg-white rounded-lg shadow-md p-8">
    <form @submit.prevent="onFormSubmit">
      <!-- Business Context -->
      <div class="mb-8">
        <div class="flex items-center gap-2 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-soft-blue"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" /><circle cx="12" cy="10" r="3" /></svg>
            <h3 class="text-lg font-medium text-dark-gray m-0">Business Context</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div>
                <label class="form-label">Industry *</label>
                <select v-model="formData.industry" class="input-field" required>
                    <option value="" disabled>Select industry...</option>
                    <option v-for="industry in INDUSTRIES" :key="industry.value" :value="industry.value">{{ industry.label }}</option>
                </select>
            </div>
            <div>
                <label class="form-label">Country *</label>
                <select v-model="formData.country" class="input-field" required :disabled="loadingCountries">
                    <option value="" disabled>{{ loadingCountries ? 'Loading...' : 'Select country...' }}</option>
                    <option v-for="country in countries" :key="country.value" :value="country.value">{{ country.label }}</option>
                </select>
            </div>
             <div>
                <label class="form-label">State/Province</label>
                <select v-model="formData.state" class="input-field" :disabled="!formData.country || loadingSubdivisions">
                     <option value="">{{ stateSelectText }}</option>
                     <option v-for="sub in subdivisions" :key="sub.value" :value="sub.value">{{ sub.label }}</option>
                </select>
            </div>
            <div>
              <label class="form-label">City</label>
              <input type="text" v-model="formData.city" class="input-field" placeholder="e.g., San Francisco" />
            </div>
        </div>
        <div class="mt-4 p-3 bg-light-blue rounded-md text-sm">
            <p class="text-dark-slate-gray font-medium mb-2">Supported Countries for Holiday Analysis:</p>
            <p class="text-dark-slate-gray leading-relaxed">
                United States, India, Canada, United Kingdom, Australia, Germany, France, Japan, Brazil, Mexico.
            </p>
        </div>
      </div>

      <!-- Forecast Settings -->
      <div class="mb-8">
        <div class="flex items-center gap-2 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-soft-blue"><rect width="18" height="18" x="3" y="4" rx="2" ry="2" /><line x1="16" x2="16" y1="2" y2="6" /><line x1="8" x2="8" y1="2" y2="6" /><line x1="3" x2="21" y1="10" y2="10" /></svg>
            <h3 class="text-lg font-medium text-dark-gray m-0">Forecast Settings</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <label class="form-label">Forecast Frequency *</label>
                <select v-model="formData.freq" class="input-field">
                    <option v-for="freq in FREQUENCIES" :key="freq.value" :value="freq.value">{{ freq.label }}</option>
                </select>
                <p class="form-hint">{{ selectedFreqDescription }}</p>
            </div>
            <div>
                <label class="form-label">Forecast Horizon *</label>
                <input type="number" v-model="formData.horizon" class="input-field" min="1" max="365" required />
                 <p class="form-hint">Number of {{ horizonUnit }} to forecast</p>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <div class="flex items-center">
                <input type="checkbox" id="apply_holidays" v-model="formData.apply_holidays" class="h-4 w-4 rounded border-gray-300 text-soft-blue focus:ring-soft-blue">
                <label for="apply_holidays" class="ml-2 form-label mb-0">Apply Country Holidays</label>
            </div>
            <div class="flex items-center">
                <input type="checkbox" id="apply_ai_adjustment" v-model="formData.apply_ai_adjustment" class="h-4 w-4 rounded border-gray-300 text-soft-blue focus:ring-soft-blue">
                <label for="apply_ai_adjustment" class="ml-2 form-label mb-0">Enable AI Adjustment</label>
            </div>
        </div>
      </div>
      
       <!-- Data Columns -->
      <div class="mb-8">
           <div class="flex items-center gap-2 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-soft-blue"><line x1="12" x2="12" y1="20" y2="10" /><line x1="18" x2="18" y1="20" y2="4" /><line x1="6" x2="6" y1="20" y2="16" /></svg>
                <h3 class="text-lg font-medium text-dark-gray m-0">Data Columns</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="form-label">Date Column *</label>
                    <select v-model="formData.date_col" class="input-field" required>
                        <option value="" disabled>Select date column...</option>
                        <option v-for="col in preview.columns" :key="col" :value="col">{{ col }} {{ detectedColumns.date?.name === col ? '(auto-detected)' : '' }}</option>
                    </select>
                </div>
                 <div>
                    <label class="form-label">Sales/Target Column *</label>
                    <select v-model="formData.target_col" class="input-field" required>
                        <option value="" disabled>Select target column...</option>
                        <option v-for="col in preview.columns" :key="col" :value="col">{{ col }} {{ detectedColumns.target?.name === col ? '(auto-detected)' : '' }}</option>
                    </select>
                </div>
            </div>
      </div>

      <!-- Submit -->
      <div class="flex justify-end">
          <button type="submit" :disabled="isLoading" class="btn-primary flex items-center gap-2" :class="{'opacity-50 cursor-not-allowed': isLoading}">
              <div v-if="isLoading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>{{ isLoading ? 'Generating Forecast...' : 'Generate Forecast' }}</span>
          </button>
      </div>

      <!-- Privacy Notice -->
      <div class="mt-6 p-4 bg-light-blue rounded-md text-center">
          <p class="text-sm text-dark-slate-gray">
              <strong>Privacy Notice:</strong> Your sales data is processed only on our server for modeling and never sent to external AI models. Only anonymous context (industry/location/horizon) is sent to AI models for macro adjustment.
          </p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue';
import { getCountries, getSubdivisions } from '../../services/forecastService';

const props = defineProps({
    preview: Object,
    detectedColumns: Object,
    isLoading: Boolean
});

const emit = defineEmits(['submit']);

const formData = reactive({
  industry: '',
  country: '',
  state: '',
  city: '',
  freq: 'W',
  horizon: 8,
  date_col: props.detectedColumns.date?.name || '',
  target_col: props.detectedColumns.target?.name || '',
  apply_holidays: true,
  apply_ai_adjustment: true,
});

const countries = ref([]);
const subdivisions = ref([]);
const loadingCountries = ref(false);
const loadingSubdivisions = ref(false);

const INDUSTRIES = [ { value: 'retail', label: 'Retail' }, { value: 'ecommerce', label: 'E-commerce' } /* ... other industries */ ];
const FREQUENCIES = [ { value: 'D', label: 'Daily', description: 'Best for short-term planning' }, { value: 'W', label: 'Weekly', description: 'Recommended for most businesses' }, { value: 'M', label: 'Monthly', description: 'Good for long-term planning' } ];

onMounted(async () => {
    loadingCountries.value = true;
    try {
        countries.value = await getCountries();
    } finally {
        loadingCountries.value = false;
    }
});

watch(() => formData.country, async (newCountry) => {
    if (newCountry) {
        loadingSubdivisions.value = true;
        formData.state = '';
        try {
            subdivisions.value = await getSubdivisions(newCountry);
        } finally {
            loadingSubdivisions.value = false;
        }
    } else {
        subdivisions.value = [];
        formData.state = '';
    }
});

const stateSelectText = computed(() => {
    if (!formData.country) return 'Select country first';
    if (loadingSubdivisions.value) return 'Loading...';
    if (subdivisions.value.length > 0) return 'Select state/province...';
    return 'No states available';
});

const selectedFreqDescription = computed(() => FREQUENCIES.find(f => f.value === formData.freq)?.description);
const horizonUnit = computed(() => formData.freq === 'D' ? 'days' : formData.freq === 'W' ? 'weeks' : 'months');

const onFormSubmit = () => {
    emit('submit', { ...formData });
};
</script>

<style scoped>
.form-label {
    display: block;
    font-size: 0.875rem;
    font-weight: 500;
    color: #2F4F4F; /* dark-slate-gray */
    margin-bottom: 0.5rem;
}
.form-hint {
    margin-top: 0.25rem;
    font-size: 0.75rem;
    color: #6b7280;
}
.input-field {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    box-sizing: border-box;
    background-color: #F2F2F2; /* light-gray */
    color: #333333; /* dark-gray */
    transition: border-color 0.2s;
}
.input-field:focus {
    outline: none;
    border-color: #4C8BF5; /* soft-blue */
    box-shadow: 0 0 0 2px rgba(76, 139, 245, 0.2);
}
.btn-primary {
  padding: 0.75rem 1.25rem;
  background-color: #4C8BF5; /* soft-blue */
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}
.btn-primary:hover {
  background-color: #3a7bd5;
}
</style>