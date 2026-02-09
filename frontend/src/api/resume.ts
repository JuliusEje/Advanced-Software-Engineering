import axios from 'axios'
import type { UploadResponse, ResumeScore } from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

export const uploadResume = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)
  
  const { data } = await api.post<UploadResponse>('/resume/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  
  return data
}

export const getResumeScore = async (id: string): Promise<ResumeScore> => {
  const { data } = await api.get<ResumeScore>(`/resume/${id}/score`)
  return data
}
