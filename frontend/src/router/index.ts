import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "Home",
    component: () => import("@/views/Home.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("@/views/Register.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/upload",
    name: "Upload",
    component: () => import("@/views/Upload.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/result/:id",
    name: "Result",
    component: () => import("@/views/Result.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard for authentication
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Initialize auth state on first load
  if (!authStore.isAuthenticated && authStore.token) {
    await authStore.verifyToken();
  }

  const requiresAuth = to.meta.requiresAuth as boolean;

  if (requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login if trying to access protected route
    next({ name: "Login", query: { redirect: to.fullPath } });
  } else if (
    !requiresAuth &&
    authStore.isAuthenticated &&
    (to.name === "Login" || to.name === "Register")
  ) {
    // Redirect to home if already authenticated and trying to access auth pages
    next("/");
  } else {
    next();
  }
});

export default router;
