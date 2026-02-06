"use client"

import React from "react"
import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts"

interface RadarChartProps {
  data: {
    subject: string
    score: number
    fullMark: number
  }[]
}

export function RadarChart({ data }: RadarChartProps) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <RechartsRadarChart data={data}>
        <PolarGrid stroke="#E2E8F0" />
        <PolarAngleAxis
          dataKey="subject"
          tick={{ fill: "#64748B", fontSize: 12 }}
        />
        <PolarRadiusAxis
          angle={30}
          domain={[0, "auto"]}
          tick={{ fill: "#94A3B8", fontSize: 10 }}
        />
        <Radar
          name="得分"
          dataKey="score"
          stroke="#3B82F6"
          fill="#3B82F6"
          fillOpacity={0.5}
        />
      </RechartsRadarChart>
    </ResponsiveContainer>
  )
}
