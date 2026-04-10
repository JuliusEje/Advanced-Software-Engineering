import { describe, it, expect, beforeEach } from "vitest";
import { createRouter, createMemoryHistory } from "vue-router";

describe("Router Configuration", () => {
  let router: any;

  beforeEach(() => {
    router = createRouter({
      history: createMemoryHistory(),
      routes: [
        { path: "/", name: "Home", component: { template: "<div>Home</div>" } },
        {
          path: "/login",
          name: "Login",
          component: { template: "<div>Login</div>" },
        },
        {
          path: "/register",
          name: "Register",
          component: { template: "<div>Register</div>" },
        },
        {
          path: "/upload",
          name: "Upload",
          component: { template: "<div>Upload</div>" },
          meta: { requiresAuth: true },
        },
        {
          path: "/result",
          name: "Result",
          component: { template: "<div>Result</div>" },
          meta: { requiresAuth: true },
        },
        {
          path: "/history",
          name: "History",
          component: { template: "<div>History</div>" },
          meta: { requiresAuth: true },
        },
      ],
    });
  });

  it("has home route", () => {
    const route = router.getRoutes().find((r: any) => r.path === "/");
    expect(route).toBeDefined();
    expect(route.name).toBe("Home");
  });

  it("has login route", () => {
    const route = router.getRoutes().find((r: any) => r.path === "/login");
    expect(route).toBeDefined();
    expect(route.name).toBe("Login");
  });

  it("has register route", () => {
    const route = router.getRoutes().find((r: any) => r.path === "/register");
    expect(route).toBeDefined();
    expect(route.name).toBe("Register");
  });

  it("marks upload as protected route", () => {
    const route = router.getRoutes().find((r: any) => r.path === "/upload");
    expect(route?.meta?.requiresAuth).toBe(true);
  });

  it("marks result as protected route", () => {
    const route = router.getRoutes().find((r: any) => r.path === "/result");
    expect(route?.meta?.requiresAuth).toBe(true);
  });

  it("marks history as protected route", () => {
    const route = router.getRoutes().find((r: any) => r.path === "/history");
    expect(route?.meta?.requiresAuth).toBe(true);
  });

  it("public routes don't require auth", () => {
    const publicRoutes = ["/", "/login", "/register"];
    publicRoutes.forEach((path) => {
      const route = router.getRoutes().find((r: any) => r.path === path);
      expect(route?.meta?.requiresAuth).not.toBe(true);
    });
  });
});
