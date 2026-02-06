"use client"

import React, { useState, useRef } from "react"
import { Upload, FileText, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface EssayEditorProps {
  onSubmit: (data: { title: string; content: string; grade: string }) => Promise<void>
}

const GRADES = ["一年级", "二年级", "三年级", "四年级", "五年级", "六年级"]

export function EssayEditor({ onSubmit }: EssayEditorProps) {
  const [title, setTitle] = useState("")
  const [content, setContent] = useState("")
  const [grade, setGrade] = useState("三年级")
  const [isLoading, setIsLoading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = async () => {
    if (!content.trim()) return

    setIsLoading(true)
    try {
      await onSubmit({ title, content, grade })
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        const text = e.target?.result as string
        setContent(text)
      }
      reader.readAsText(file)
    }
  }

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">作文评测</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex gap-4">
          <div className="w-1/3">
            <label className="text-sm font-medium">年级</label>
            <Select value={grade} onValueChange={setGrade}>
              <SelectTrigger className="mt-1">
                <SelectValue placeholder="选择年级" />
              </SelectTrigger>
              <SelectContent>
                {GRADES.map((g) => (
                  <SelectItem key={g} value={g}>
                    {g}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="w-2/3">
            <label className="text-sm font-medium">标题（可选）</label>
            <Input
              placeholder="请输入作文标题"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="mt-1"
            />
          </div>
        </div>

        <div>
          <label className="text-sm font-medium">作文内容</label>
          <Textarea
            placeholder="请输入或粘贴作文内容..."
            className="min-h-[300px] font-medium text-base leading-relaxed mt-1"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
        </div>

        <div className="border-2 border-dashed border-gray-200 rounded-lg p-6 text-center">
          <Upload className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-2 text-sm text-gray-600">
            支持拖拽上传 .txt .doc .docx .md .zip
          </p>
          <input
            type="file"
            ref={fileInputRef}
            className="hidden"
            accept=".txt,.doc,.docx,.md,.zip"
            multiple={true}
            onChange={handleFileUpload}
          />
          <Button
            variant="outline"
            className="mt-4"
            onClick={() => fileInputRef.current?.click()}
          >
            选择文件
          </Button>
        </div>

        <Button
          className="w-full h-12 text-lg"
          onClick={handleSubmit}
          disabled={isLoading || !content.trim()}
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              评测中...
            </>
          ) : (
            "开始评测"
          )}
        </Button>
      </CardContent>
    </Card>
  )
}
