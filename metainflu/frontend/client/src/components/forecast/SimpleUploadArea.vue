<template>
  <div class="bg-white rounded-lg shadow-md p-8">
    <div v-if="props.uploadState.file && props.uploadState.preview" class="p-6">
       <!-- File Loaded State -->
    </div>
    <div v-else>
      <div
        class="border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ease-in-out"
        :class="{
          'border-soft-blue bg-light-blue': dragActive,
          'border-gray-300': !dragActive
        }"
        @dragenter.prevent="dragActive = true"
        @dragover.prevent="dragActive = true"
        @dragleave.prevent="dragActive = false"
        @drop.prevent="handleDrop"
      >
        <input type="file" id="file-upload" class="hidden" accept=".csv,.xlsx,.xls" @change="handleInputChange" :disabled="props.uploadState.isProcessing" />
        <div class="flex flex-col items-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-4" :class="{'text-soft-blue': dragActive, 'text-gray-400': !dragActive}">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" x2="12" y1="3" y2="15" />
            </svg>
            <div v-if="props.uploadState.isProcessing" class="flex items-center gap-2">
                <div class="w-4 h-4 border-2 border-soft-blue border-t-transparent rounded-full animate-spin"></div>
                <span class="text-dark-slate-gray">Processing file...</span>
            </div>
            <div v-else>
                <h3 class="text-lg font-medium text-dark-gray mb-2">Upload your sales data</h3>
                <p class="text-dark-slate-gray mb-4">Drag and drop your CSV or Excel file here, or click to browse</p>
                <label for="file-upload" class="btn-primary cursor-pointer inline-block">Choose File</label>
                <p class="text-xs text-dark-slate-gray mt-2">Supports CSV, XLSX, and XLS files up to 10MB. Download a sample file <a href="/demo.csv" class="text-soft-blue hover:underline" download>here</a>.</p>
            </div>
        </div>
      </div>
      <div v-if="props.uploadState.error" class="mt-4 bg-orange-100 border border-muted-orange text-muted-orange rounded-md p-3">
          <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><circle cx="12" cy="12" r="10" /><line x1="12" x2="12" y1="8" y2="12" /><line x1="12" x2="12.01" y1="16" y2="16" /></svg>
              <span class="text-sm">{{ props.uploadState.error }}</span>
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  uploadState: Object,
});

const emit = defineEmits(['update:uploadState', 'file-processed']);

const dragActive = ref(false);

const handleFiles = async (files) => {
  if (!files || files.length === 0) return;
  const file = files[0];

  if (!fileUtils.validateFileName(file.name)) {
    emit('update:uploadState', { ...props.uploadState, error: 'Please upload a CSV, XLSX, or XLS file.' });
    return;
  }

  emit('update:uploadState', { ...props.uploadState, isProcessing: true, error: null, file });

  try {
    const preview = await fileUtils.parseFile(file);
    const columnInfo = columnDetection.analyzeColumns(preview.rows);
    const detectedDate = columnDetection.detectDateColumn(columnInfo);
    const detectedTarget = columnDetection.detectTargetColumn(columnInfo);
    const detectedColumns = { date: detectedDate, target: detectedTarget };

    emit('update:uploadState', { ...props.uploadState, preview, detectedColumns, isProcessing: false, file });
    emit('file-processed', file, preview, detectedColumns);
  } catch (error) {
    emit('update:uploadState', { ...props.uploadState, error: error.message || 'Failed to process file', isProcessing: false });
  }
};

const handleDrop = (e) => {
  dragActive.value = false;
  if (e.dataTransfer?.files) {
    handleFiles(e.dataTransfer.files);
  }
};

const handleInputChange = (e) => {
  const target = e.target;
  if (target.files) {
    handleFiles(target.files);
  }
};
</script>

<style scoped>
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
  background-color: #3a7bd5; /* A slightly darker shade of soft-blue */
}
</style>