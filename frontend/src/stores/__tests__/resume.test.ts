import { describe, it, expect, beforeEach, vi } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useResumeStore } from "@/stores/resume";

describe("Resume Store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("initializes with null current score", () => {
    const store = useResumeStore();
    expect(store.currentScore).toBeNull();
  });

  it("can set current score", () => {
    const store = useResumeStore();

    const mockScore = {
      score: 85,
      feedback: "Good resume",
      suggestions: ["Add metrics", "Improve format", "Update skills"],
    };

    store.setScore(mockScore);

    expect(store.currentScore).toEqual(mockScore);
    expect(store.currentScore?.score).toBe(85);
  });

  it("can clear current score", () => {
    const store = useResumeStore();

    store.setScore({
      score: 80,
      feedback: "test",
      suggestions: [],
    });

    expect(store.currentScore).not.toBeNull();

    store.currentScore = null;

    expect(store.currentScore).toBeNull();
  });

  it("tracks scores with setScore", () => {
    const store = useResumeStore();

    const score1 = { score: 85, feedback: "Ok", suggestions: [] };
    const score2 = {
      score: 90,
      feedback: "Great",
      suggestions: ["Keep it up"],
    };

    store.setScore(score1);
    expect(store.currentScore?.score).toBe(85);

    store.setScore(score2);
    expect(store.currentScore?.score).toBe(90);
  });

  it("manages loading state", () => {
    const store = useResumeStore();

    expect(store.isLoading).toBe(false);

    store.setLoading(true);
    expect(store.isLoading).toBe(true);

    store.setLoading(false);
    expect(store.isLoading).toBe(false);
  });
});
