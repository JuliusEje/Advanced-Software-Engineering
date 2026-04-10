import { describe, it, expect, beforeEach, vi } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useAuthStore } from "@/stores/auth";

describe("Auth Store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
    vi.clearAllMocks();
  });

  it("initializes with no user", () => {
    const store = useAuthStore();
    expect(store.user).toBeFalsy();
    expect(store.isAuthenticated).toBe(false);
  });

  it("stores user when set", () => {
    const store = useAuthStore();

    store.user = { id: 1, email: "test@example.com", name: "Test User" };
    store.setToken("test-token-123");

    expect(store.token).toBe("test-token-123");
    expect(store.user?.email).toBe("test@example.com");
    expect(store.isAuthenticated).toBe(true);
  });

  it("computes isAuthenticated correctly", () => {
    const store = useAuthStore();

    expect(store.isAuthenticated).toBe(false);

    store.token = "token";
    store.user = { id: 1, email: "test@example.com", name: "Test" };

    expect(store.isAuthenticated).toBe(true);

    store.token = null;
    expect(store.isAuthenticated).toBe(false);
  });

  it("clears state on manual logout", () => {
    const store = useAuthStore();

    store.token = "test-token";
    store.user = { id: 1, email: "test@example.com", name: "Test User" };

    store.token = null;
    store.user = null;

    expect(store.user).toBeNull();
    expect(store.token).toBeNull();
    expect(store.isAuthenticated).toBe(false);
  });

  it("handles multiple user sessions", () => {
    const store = useAuthStore();

    store.user = { id: 1, email: "user1@example.com", name: "User One" };
    store.token = "token-1";
    expect(store.user.email).toBe("user1@example.com");

    store.user = { id: 2, email: "user2@example.com", name: "User Two" };
    store.token = "token-2";
    expect(store.user.email).toBe("user2@example.com");
    expect(store.token).toBe("token-2");
  });

  it("preserves user info when updating token", () => {
    const store = useAuthStore();

    const userData = { id: 1, email: "test@example.com", name: "Test User" };
    store.user = userData;
    store.token = "old-token";

    store.token = "new-token";

    expect(store.user).toStrictEqual(userData);
    expect(store.token).toBe("new-token");
  });
});
