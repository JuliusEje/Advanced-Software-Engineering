<template>
  <div class="upload-page">
    <div class="upload-container">
      <h2>Upload Resume</h2>
      
      <div 
        class="upload-area"
        :class="{ 'drag-over': isDragging }"
        @drop.prevent="handleDrop"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
      >
        <input 
          type="file" 
          ref="fileInput"
          @change="handleFileSelect"
          accept=".pdf,.doc,.docx"
          style="display: none"
        />
        
        <div v-if="!selectedFile" class="upload-prompt">
          <p>Drag and drop your file here or</p>
          <button @click="triggerFileInput" class="btn-select">Choose File</button>
          <p class="file-hint">Supports PDF, DOC, DOCX formats</p>
        </div>
        
        <div v-else class="file-info">
          <p>Selected: {{ selectedFile.name }}</p>
          <button @click="clearFile" class="btn-clear">Clear</button>
        </div>
      </div>
      
      <button 
        @click="handleUpload" 
        :disabled="!selectedFile || isUploading"
        class="btn-upload"
      >
        {{ isUploading ? 'Uploading...' : 'Upload & Analyze' }}
      </button>
      
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { uploadResume } from '@/api/resume'

const router = useRouter()
const fileInput = ref<HTMLInputElement>()
const selectedFile = ref<File | null>(null)
const isDragging = ref(false)
const isUploading = ref(false)
const error = ref('')

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0]
    error.value = ''
  }
}

const handleDrop = (event: DragEvent) => {
  isDragging.value = false
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    selectedFile.value = event.dataTransfer.files[0]
    error.value = ''
  }
}

const clearFile = () => {
  selectedFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const handleUpload = async () => {
  if (!selectedFile.value) return
  
  isUploading.value = true
  error.value = ''
  
  try {
    const response = await uploadResume(selectedFile.value)
    router.push(`/result/${response.id}`)
  } catch (err) {
    error.value = 'Upload failed. Please try again.'
    console.error(err)
  } finally {
    isUploading.value = false
  }
}
</script>

<style scoped>
.upload-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.upload-container {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 3rem;
  text-align: center;
  margin-bottom: 1.5rem;
  transition: all 0.3s;
}

.upload-area.drag-over {
  border-color: #667eea;
  background-color: #f0f4ff;
}

.upload-prompt p {
  margin-bottom: 1rem;
  color: #666;
}

.btn-select {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
}

.file-hint {
  font-size: 0.875rem;
  color: #999;
  margin-top: 1rem;
}

.file-info {
  color: #333;
}

.btn-clear {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-upload {
  width: 100%;
  padding: 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-upload:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error {
  color: #f44336;
  text-align: center;
  margin-top: 1rem;
}
</style>
