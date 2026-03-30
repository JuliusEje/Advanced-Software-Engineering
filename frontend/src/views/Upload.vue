<template>
  <div class="upload-page">
    <nav class="navbar">
      <div class="navbar-content">
        <router-link to="/" class="nav-back">← Back to Home</router-link>
        <button @click="handleLogout" class="btn-logout">Sign Out</button>
      </div>
    </nav>

    <div class="upload-container">
      <div class="upload-header">
        <h2>Upload Your Resume</h2>
        <p>We'll analyze it and provide detailed feedback</p>
      </div>

      <div class="upload-content">
        <div class="two-column-layout">
          <!-- Left Column: JD Section -->
          <div class="jd-section">
            <h3 class="section-title">Job Details (Optional)</h3>
            <p class="section-hint">
              Provide job details for targeted analysis
            </p>

            <div class="form-group">
              <label for="company">Company</label>
              <input
                id="company"
                v-model="company"
                type="text"
                placeholder="e.g., Google, Microsoft"
                class="text-input"
              />
            </div>

            <div class="form-group">
              <label for="jobDescription">Job Description</label>
              <textarea
                id="jobDescription"
                v-model="jobDescription"
                placeholder="Paste the job description here..."
                class="textarea-input"
                rows="10"
              ></textarea>
            </div>
          </div>

          <!-- Right Column: Resume Upload -->
          <div class="resume-section">
            <h3 class="section-title">Resume Upload</h3>
            <p class="section-hint">Upload your resume file</p>

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
                <div class="upload-icon">📄</div>
                <p class="primary-text">Drag and drop your resume here</p>
                <p class="secondary-text">or</p>
                <button @click="triggerFileInput" class="btn-select">
                  Choose File
                </button>
                <p class="file-hint">Supports PDF, DOC, DOCX (Max 10MB)</p>
              </div>

              <div v-else class="file-info">
                <div class="file-icon">✓</div>
                <p class="file-name">{{ selectedFile.name }}</p>
                <p class="file-size">{{ formatFileSize(selectedFile.size) }}</p>
                <button @click="clearFile" class="btn-clear">
                  Clear Selection
                </button>
              </div>
            </div>
          </div>
        </div>

        <button
          @click="handleUpload"
          :disabled="!selectedFile || isUploading"
          class="btn-upload"
        >
          <span v-if="!isUploading">Upload & Analyze</span>
          <span v-else>
            <span class="loading-spinner"></span>
            Analyzing...
          </span>
        </button>

        <p v-if="error" class="error-message">{{ error }}</p>

        <div v-if="isUploading" class="loading-bar">
          <div class="progress"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { uploadResume } from "@/api/resume";

const router = useRouter();
const authStore = useAuthStore();
const fileInput = ref<HTMLInputElement>();
const selectedFile = ref<File | null>(null);
const isDragging = ref(false);
const isUploading = ref(false);
const error = ref("");
const company = ref("");
const jobDescription = ref("");

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const file = target.files[0];
    if (file.size > 10 * 1024 * 1024) {
      error.value = "File is too large. Maximum size is 10MB.";
      return;
    }
    selectedFile.value = file;
    error.value = "";
  }
};

const handleDrop = (event: DragEvent) => {
  isDragging.value = false;
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    const file = event.dataTransfer.files[0];
    if (file.size > 10 * 1024 * 1024) {
      error.value = "File is too large. Maximum size is 10MB.";
      return;
    }
    selectedFile.value = file;
    error.value = "";
  }
};

const clearFile = () => {
  selectedFile.value = null;
  if (fileInput.value) {
    fileInput.value.value = "";
  }
};

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
};

const handleUpload = async () => {
  if (!selectedFile.value) return;

  isUploading.value = true;
  error.value = "";

  try {
    const response = await uploadResume(
      selectedFile.value,
      company.value.trim() || undefined,
      jobDescription.value.trim() || undefined
    );
    router.push(`/result/${response.id}`);
  } catch (err) {
    error.value = "Upload failed. Please try again.";
    console.error(err);
  } finally {
    isUploading.value = false;
  }
};

const handleLogout = async () => {
  await authStore.logout();
  router.push("/");
};
</script>

<style scoped>
/* Merged and Fixed Styles */
.upload-page {
  min-height: 100vh;
  background: #f8f9fa;
  display: flex;
  flex-direction: column;
}

.navbar {
  width: 100%;
  box-sizing: border-box;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.navbar-content {
  max-width: 100%;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-back {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
  width: auto;
}

.nav-back:hover {
  color: #764ba2;
}

.btn-logout {
  padding: 0.6rem 1.2rem;
  background: #e2e8f0;
  color: #2d3748;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  background: #cbd5e0;
}

.upload-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 1200px;
  width: 100%;
  margin: 2rem auto;
  padding: 3rem;
  box-sizing: border-box;
}

.upload-header {
  text-align: center;
  margin-bottom: 2rem;
}

.upload-header h2 {
  color: #1a202c;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.upload-header p {
  color: #718096;
  font-size: 1rem;
}

.upload-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.jd-section,
.resume-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-title {
  color: #2d3748;
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
}

.section-hint {
  color: #718096;
  font-size: 0.9rem;
  margin: 0 0 0.5rem 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: #4a5568;
  font-weight: 500;
  font-size: 0.95rem;
}

.text-input {
  padding: 0.75rem;
  border: 1px solid #cbd5e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.text-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.textarea-input {
  padding: 0.75rem;
  border: 1px solid #cbd5e0;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  resize: vertical;
  min-height: 150px;
  transition: border-color 0.2s;
}

.textarea-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.upload-area {
  border: 2px dashed #cbd5e0;
  border-radius: 12px;
  padding: 2rem 1.5rem;
  text-align: center;
  background: white;
  transition: all 0.3s;
  cursor: pointer;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area.drag-over {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
  transform: scale(1.02);
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.primary-text {
  color: #2d3748;
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.secondary-text {
  color: #a0aec0;
  margin: 1rem 0;
}

.btn-select {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-select:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.file-hint {
  color: #a0aec0;
  font-size: 0.85rem;
  margin-top: 1rem;
}

.file-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.file-icon {
  font-size: 2.5rem;
  color: #48bb78;
}

.file-name {
  color: #2d3748;
  font-weight: 600;
  word-break: break-word;
}

.file-size {
  color: #718096;
  font-size: 0.9rem;
}

.btn-clear {
  padding: 0.6rem 1.2rem;
  background: #fed7d7;
  color: #c53030;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-clear:hover {
  background: #fc8181;
}

.btn-upload {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-upload:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn-upload:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  color: #e53e3e;
  background-color: #fff5f5;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #e53e3e;
  margin-top: -1rem;
}

.loading-bar {
  height: 4px;
  background-color: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  animation: progress 1.5s ease-in-out infinite;
}

@keyframes progress {
  0% {
    width: 0;
  }
  50% {
    width: 100%;
  }
  100% {
    width: 0;
  }
}

@media (max-width: 768px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }

  .upload-container {
    padding: 2rem 1.5rem;
    margin: 1rem;
  }

  .upload-area {
    padding: 2rem 1rem;
    min-height: 150px;
  }

  .upload-header h2 {
    font-size: 1.5rem;
  }
}
</style>
