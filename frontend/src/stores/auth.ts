import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { User } from "@/types";
import apiClient from "@/api/client";

export const useAuthStore = defineStore("auth", () => {
  // --- State ---
  const user = ref<User | null>(null);
  const token = ref<string | null>(localStorage.getItem("auth_token"));
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // --- Getters ---
  const isAuthenticated = computed(() => !!token.value && !!user.value);
  const isLoggedIn = computed(() => !!token.value);

  // --- Actions ---
  const setToken = (newToken: string) => {
    token.value = newToken;
    localStorage.setItem("auth_token", newToken);
  };

  const register = async (email: string, password: string, name: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post("/auth/register", {
        email,
        password,
        name,
      });
      setToken(response.data.token);
      user.value = response.data.user;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.error || "Registration failed";
      throw error.value;
    } finally {
      isLoading.value = false;
    }
  };

  const login = async (email: string, password: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post("/auth/login", { email, password });
      setToken(response.data.token);
      user.value = response.data.user;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.error || "Login failed";
      throw error.value;
    } finally {
      isLoading.value = false;
    }
  };

  const logout = async () => {
    try {
      await apiClient.post("/auth/logout");
    } catch (err) {
      console.error("Logout error:", err);
    } finally {
      token.value = null;
      user.value = null;
      localStorage.removeItem("auth_token");
    }
  };

  const verifyToken = async () => {
    if (!token.value) {
      user.value = null;
      return false;
    }
    try {
      const response = await apiClient.get("/auth/verify");
      user.value = response.data.user;
      return true;
    } catch (err) {
      token.value = null;
      user.value = null;
      localStorage.removeItem("auth_token");
      return false;
    }
  };

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    isLoggedIn,
    setToken,
    register,
    login,
    logout,
    verifyToken,
  };
});
