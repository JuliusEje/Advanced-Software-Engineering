import { describe, it, expect, beforeEach, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createMemoryHistory } from "vue-router";
import Login from "@/views/Login.vue";

const mockRouter = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: "/login", component: { template: "<div>Login</div>" } },
    { path: "/register", component: { template: "<div>Register</div>" } },
  ],
});

describe("Login.vue", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("renders login page", () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    expect(wrapper.exists()).toBe(true);
    expect(
      wrapper.find("form").exists() || wrapper.find("input").exists(),
    ).toBe(true);
  });

  it("has email and password inputs", () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    expect(wrapper.find('input[type="email"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
  });

  it("has submit button", () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
  });

  it("component is mounted without errors", () => {
    expect(() => {
      mount(Login, {
        global: {
          plugins: [mockRouter],
          stubs: {
            "router-link": true,
          },
        },
      });
    }).not.toThrow();
  });

  it("accepts email input", async () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    const emailInput = wrapper.find('input[type="email"]');
    if (emailInput.exists()) {
      await emailInput.setValue("test@example.com");
      expect((emailInput.element as HTMLInputElement).value).toContain(
        "test@example.com",
      );
    }
  });

  it("accepts password input", async () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    const passwordInput = wrapper.find('input[type="password"]');
    if (passwordInput.exists()) {
      await passwordInput.setValue("password123");
      expect((passwordInput.element as HTMLInputElement).value).toContain(
        "password123",
      );
    }
  });
});
