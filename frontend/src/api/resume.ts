import apiClient from "@/api/client";

export async function uploadResume(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await apiClient.post("/resume/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  } catch (err: any) {
    const serverMessage = err.response?.data?.error;
    console.error("Backend said:", serverMessage);
    console.error("Status Code:", err.response?.status);
    throw new Error(serverMessage || "Failed to upload resume");
  }
}

export async function getResumeScore(resumeId: string) {
  try {
    const response = await apiClient.get(`/resume/${resumeId}/score`);
    return response.data;
  } catch (err: any) {
    const serverMessage = err.response?.data?.error;
    console.error("Backend said:", serverMessage);
    console.error("Status Code:", err.response?.status);
    throw new Error(serverMessage || "Failed to fetch resume score");
  }
}
