"use client"

import React, { useState } from "react"
import { EssayEditor } from "@/components/essay-editor"
import { ScoreCard } from "@/components/score-card"
import { RadarChart } from "@/components/radar-chart"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { essayApi, ScoringResult } from "@/lib/api"

export default function Home() {
  const [result, setResult] = useState<ScoringResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (data: { title: string; content: string; grade: string }) => {
    setIsLoading(true)
    try {
      const response = await essayApi.submit(data)
      setResult(response.data)
    } catch (error) {
      console.error("评测失败:", error)
      alert("评测失败，请稍后重试")
    } finally {
      setIsLoading(false)
    }
  }

  const dimensionScores = result
    ? [
        { name: "内容主题", score: result.dimensions.content_theme.score, maxScore: result.dimensions.content_theme.max_score, comment: result.dimensions.content_theme.comment },
        { name: "结构组织", score: result.dimensions.structure.score, maxScore: result.dimensions.structure.max_score, comment: result.dimensions.structure.comment },
        { name: "语言表达", score: result.dimensions.language.score, maxScore: result.dimensions.language.max_score, comment: result.dimensions.language.comment },
        { name: "书写规范", score: result.dimensions.writing_norm.score, maxScore: result.dimensions.writing_norm.max_score, comment: result.dimensions.writing_norm.comment },
        { name: "创意特色", score: result.dimensions.creativity.score, maxScore: result.dimensions.creativity.max_score, comment: result.dimensions.creativity.comment },
      ]
    : []

  const radarData = dimensionScores.map((dim) => ({
    subject: dim.name,
    score: dim.score,
    fullMark: dim.maxScore,
  }))

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">青少年写作质量评测系统</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 px-4">
        <div className="grid gap-6 md:grid-cols-2">
          <div>
            <EssayEditor onSubmit={handleSubmit} />
          </div>

          {result && (
            <div className="space-y-6">
              <ScoreCard
                totalScore={result.total_score}
                grade={result.grade}
                dimensionScores={dimensionScores}
              />

              <Card>
                <CardHeader>
                  <CardTitle>维度分析</CardTitle>
                </CardHeader>
                <CardContent>
                  <RadarChart data={radarData} />
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>优点</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-5 space-y-2">
                    {result.strengths.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>改进建议</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-5 space-y-2">
                    {result.suggestions.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
