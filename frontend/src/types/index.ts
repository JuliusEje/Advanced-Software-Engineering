export interface User {
  id: string | number;
  email: string;
  name: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export interface ResumeScore {
  id: string;
  score: number;
  feedback: string;
  suggestions: string[];
  createdAt: string;
  company?: string;
  jobDescription?: string;
}

export interface UploadResponse {
  id: string;
  message: string;
  score?: number;
  feedback?: string;
  suggestions?: string[];
  company?: string;
  jobDescription?: string;
}

export interface ResumeSummary {
  id: string;
  filename: string;
  score: number;
  createdAt: string;
}
