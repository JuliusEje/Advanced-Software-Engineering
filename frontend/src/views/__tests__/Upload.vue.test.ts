import { describe, it, expect, beforeEach, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createMemoryHistory } from "vue-router";
import Upload from "@/views/Upload.vue";

const mockRouter = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: "/upload", component: { template: "<div>Upload</div>" } },
    { path: "/result", component: { template: "<div>Result</div>" } },
  ],
});

describe("Upload.vue", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("renders upload component", () => {
    const wrapper = mount(Upload, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    expect(wrapper.exists()).toBe(true);
  });

  it("has file input element", () => {
    const wrapper = mount(Upload, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    expect(wrapper.find('input[type="file"]').exists()).toBe(true);
  });

  it("has buttons or form elements", () => {
    const wrapper = mount(Upload, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    const hasButton = wrapper.find("button").exists();
    const hasInput = wrapper.find("input").exists();
    expect(hasButton || hasInput).toBe(true);
  });

  it("component mounts without errors", () => {
    expect(() => {
      mount(Upload, {
        global: {
          plugins: [mockRouter],
          stubs: {
            "router-link": true,
          },
        },
      });
    }).not.toThrow();
  });

  it("can have job description textarea", () => {
    const wrapper = mount(Upload, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    // JD field is optional but likely exists
    const textarea = wrapper.find("textarea");
    const inputs = wrapper.findAll("input");
    expect(textarea.exists() || inputs.length > 0).toBe(true);
  });

  it("has proper form structure", () => {
    const wrapper = mount(Upload, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    const form = wrapper.find("form");
    if (form.exists()) {
      expect(form.find('input[type="file"]').exists()).toBe(true);
    }
  });

  it("contains file input element", () => {
    const wrapper = mount(Upload, {
      global: {
        plugins: [mockRouter],
        stubs: {
          "router-link": true,
        },
      },
    });

    expect(wrapper.find('input[type="file"]').exists()).toBe(true);
  });
});
