export interface ResumeScore {
  id: string
  score: number
  feedback: string
  suggestions: string[]
  createdAt: string
}

export interface UploadResponse {
  id: string
  message: string
}
