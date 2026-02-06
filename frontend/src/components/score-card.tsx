"use client"

import React from "react"
import {
  Card,
  CardContent,
} from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface DimensionScore {
  name: string
  score: number
  maxScore: number
  comment: string
}

interface ScoreCardProps {
  totalScore: number
  grade: string
  dimensionScores: DimensionScore[]
  onViewDetails?: () => void
}

const GRADE_COLORS: Record<string, string> = {
  "优秀": "text-green-500",
  "良好": "text-blue-500",
  "合格": "text-yellow-500",
  "待提高": "text-red-500",
}

const DIMENSION_COLORS: Record<string, string> = {
  "内容主题": "bg-blue-500",
  "结构组织": "bg-green-500",
  "语言表达": "bg-purple-500",
  "书写规范": "bg-orange-500",
  "创意特色": "bg-pink-500",
}

export function ScoreCard({ totalScore, grade, dimensionScores, onViewDetails }: ScoreCardProps) {
  const gradeColor = GRADE_COLORS[grade] || "text-gray-500"

  return (
    <Card className="bg-gradient-to-br from-blue-50 to-indigo-50">
      <CardContent className="pt-6">
        <div className="flex items-center justify-between">
          <div className="text-center">
            <p className="text-sm text-gray-500">总分</p>
            <p className="text-7xl font-bold text-blue-600">{totalScore}</p>
            <p className={`text-2xl font-medium ${gradeColor}`}>
              {grade}
            </p>
          </div>

          <div className="flex-1 ml-8 space-y-3">
            {dimensionScores.map((dim) => (
              <div key={dim.name} className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="font-medium">{dim.name}</span>
                  <span className="text-gray-500">
                    {dim.score}/{dim.maxScore}
                  </span>
                </div>
                <Progress
                  value={(dim.score / dim.maxScore) * 100}
                  className="h-2"
                />
              </div>
            ))}
          </div>
        </div>

        {onViewDetails && (
          <button
            onClick={onViewDetails}
            className="w-full mt-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
          >
            查看详细分析
          </button>
        )}
      </CardContent>
    </Card>
  )
}
