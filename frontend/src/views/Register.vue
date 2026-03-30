<template>
  <div class="auth-page register-page">
    <div class="auth-container">
      <div class="auth-header">
        <h1>Create Account</h1>
        <p class="subtitle">Join us to optimize your resume</p>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label for="name">Full Name</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            placeholder="John Doe"
            required
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="you@example.com"
            required
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            placeholder="••••••••"
            required
            :disabled="isLoading"
          />
          <p class="password-hint">At least 8 characters recommended</p>
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="formData.confirmPassword"
            type="password"
            placeholder="••••••••"
            required
            :disabled="isLoading"
          />
        </div>

        <button
          type="submit"
          class="btn-submit"
          :disabled="
            isLoading || formData.password !== formData.confirmPassword
          "
        >
          {{ isLoading ? "Creating account..." : "Create Account" }}
        </button>

        <p v-if="error" class="error-message">{{ error }}</p>
      </form>

      <div class="auth-footer">
        <p>
          Already have an account?
          <router-link to="/login" class="link">Sign in here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const formData = ref({
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const isLoading = ref(false);
const error = ref("");

const handleRegister = async () => {
  if (formData.value.password !== formData.value.confirmPassword) {
    error.value = "Passwords do not match";
    return;
  }

  isLoading.value = true;
  error.value = "";

  try {
    await authStore.register(
      formData.value.email,
      formData.value.password,
      formData.value.name,
    );
    router.push("/");
  } catch (err: any) {
    error.value = err || "Registration failed. Please try again.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  padding: 2rem;
}

.register-page {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

.auth-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 3rem;
  width: 100%;
  max-width: 400px;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header h1 {
  font-size: 1.8rem;
  color: #1a202c;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.subtitle {
  color: #718096;
  font-size: 0.95rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: #2d3748;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
  font-family: inherit;
}

.form-group input:focus {
  outline: none;
  border-color: #764ba2;
  box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.1);
}

.form-group input:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
}

.password-hint {
  font-size: 0.75rem;
  color: #a0aec0;
  margin-top: -0.25rem;
}

.btn-submit {
  padding: 0.85rem;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 1rem;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(118, 75, 162, 0.3);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  color: #e53e3e;
  font-size: 0.85rem;
  margin-top: -0.5rem;
  background-color: #fff5f5;
  padding: 0.75rem;
  border-radius: 6px;
  border-left: 3px solid #e53e3e;
}

.auth-footer {
  margin-top: 2rem;
  text-align: center;
  border-top: 1px solid #e2e8f0;
  padding-top: 1.5rem;
}

.auth-footer p {
  color: #718096;
  font-size: 0.9rem;
}

.link {
  color: #764ba2;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.link:hover {
  color: #667eea;
  text-decoration: underline;
}

@media (max-width: 640px) {
  .auth-container {
    padding: 2rem 1.5rem;
  }

  .auth-header h1 {
    font-size: 1.5rem;
  }
}
</style>
