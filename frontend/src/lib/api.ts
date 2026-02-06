import axios from "axios"

const api = axios.create({
  baseURL: "/api",
  timeout: 300000,
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error)
    return Promise.reject(error)
  }
)

export interface EssaySubmission {
  title: string
  content: string
  grade: string
}

export interface ScoringResult {
  total_score: number
  grade: string
  dimensions: {
    content_theme: { score: number; max_score: number; comment: string }
    structure: { score: number; max_score: number; comment: string }
    language: { score: number; max_score: number; comment: string }
    writing_norm: { score: number; max_score: number; comment: string }
    creativity: { score: number; max_score: number; comment: string }
  }
  strengths: string[]
  weaknesses: string[]
  suggestions: string[]
}

export const essayApi = {
  submit: (data: EssaySubmission) =>
    api.post<ScoringResult>("/essays/evaluate", data),

  getResult: (essayId: string) =>
    api.get<ScoringResult>(`/essays/result/${essayId}`),
}

export default api
