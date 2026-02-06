import json
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from app.services.llm.base import LLMProvider, EssayScoringTemplate


class DimensionScore(BaseModel):
    name: str
    score: float
    max_score: float
    comment: str


class ScoringResult(BaseModel):
    total_score: int
    grade: str
    dimensions: Dict[str, DimensionScore]
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    essay_type_analysis: Dict[str, Any]


class EssayScoringEngine:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    async def score_essay(
        self,
        content: str,
        title: Optional[str],
        grade: str,
        essay_type: str
    ) -> ScoringResult:
        prompt = EssayScoringTemplate.build_scoring_prompt(content, title, grade, essay_type)

        response = await self.llm.generate(
            prompt=prompt,
            temperature=0.3,
            max_tokens=4096
        )

        return self._parse_response(response.content)

    def _parse_response(self, response: str) -> ScoringResult:
        try:
            json_str = response.strip().strip("```json").strip("```").strip()
            data = json.loads(json_str)

            dimensions = {}
            for key, value in data.get("dimensions", {}).items():
                dimensions[key] = DimensionScore(
                    name=value.get("name", key),
                    score=value.get("score", 0),
                    max_score=value.get("max_score", 100),
                    comment=value.get("comment", "")
                )

            return ScoringResult(
                total_score=data.get("total_score", 0),
                grade=data.get("grade", "合格"),
                dimensions=dimensions,
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", []),
                suggestions=data.get("suggestions", []),
                essay_type_analysis=data.get("essay_type_analysis", {})
            )
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {e}")

    def calculate_grade(self, score: int) -> str:
        if score >= 85:
            return "优秀"
        elif score >= 70:
            return "良好"
        elif score >= 60:
            return "合格"
        else:
            return "待提高"
