from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class LLMResponse(BaseModel):
    content: str
    usage: Optional[Dict[str, int]] = None
    model: str
    finish_reason: Optional[str] = None
    raw_response: Optional[Any] = None


class LLMProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def supported_models(self) -> List[str]:
        pass

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        pass

    @abstractmethod
    def validate_api_key(self, api_key: str) -> bool:
        pass

    @abstractmethod
    def to_config_dict(self, api_key: str) -> Dict[str, Any]:
        pass


class EssayScoringTemplate:
    SYSTEM_PROMPT = """你是一位经验丰富的小学语文教师，专门负责评价小学生的作文。你的评价应当：
1. 温和鼓励：始终以鼓励为主，避免打击学生积极性
2. 具体明确：指出具体优点和需要改进的地方
3. 适龄评价：根据学生的年级调整评价标准
4. 建设性建议：提供切实可行的改进建议"""

    SCORING_DIMENSIONS = {
        "content_theme": {
            "name": "内容主题",
            "weight": {"一年级": 0.25, "二年级": 0.25, "三年级": 0.25, "四年级": 0.28, "五年级": 0.30, "六年级": 0.30}
        },
        "structure": {
            "name": "结构组织",
            "weight": {"一年级": 0.15, "二年级": 0.15, "三年级": 0.20, "四年级": 0.22, "五年级": 0.22, "六年级": 0.25}
        },
        "language": {
            "name": "语言表达",
            "weight": {"一年级": 0.30, "二年级": 0.30, "三年级": 0.25, "四年级": 0.25, "五年级": 0.23, "六年级": 0.22}
        },
        "writing_norm": {
            "name": "书写规范",
            "weight": {"一年级": 0.25, "二年级": 0.25, "三年级": 0.20, "四年级": 0.15, "五年级": 0.15, "六年级": 0.13}
        },
        "creativity": {
            "name": "创意特色",
            "weight": {"一年级": 0.05, "二年级": 0.05, "三年级": 0.10, "四年级": 0.10, "五年级": 0.10, "六年级": 0.10}
        }
    }

    @classmethod
    def build_scoring_prompt(cls, essay_content: str, essay_title: Optional[str], grade: str, essay_type: str) -> str:
        weight = {
            dim: info["weight"][grade]
            for dim, info in cls.SCORING_DIMENSIONS.items()
        }

        return f"""{cls.SYSTEM_PROMPT}

## 作文信息
- 年级：{grade}
- 写作类型：{essay_type}
- 标题：{essay_title or '无'}
- 正文：
---
{essay_content}
---

## 评分维度与权重
请对以下五个维度进行评分（总分100分）：

### 1. 内容主题（满分30分，权重{weight['content_theme']*100:.0f}%）
### 2. 结构组织（满分20分，权重{weight['structure']*100:.0f}%）
### 3. 语言表达（满分25分，权重{weight['language']*100:.0f}%）
### 4. 书写规范（满分15分，权重{weight['writing_norm']*100:.0f}%）
### 5. 创意特色（满分10分，权重{weight['creativity']*100:.0f}%）

## 输出格式
请严格按照以下 JSON 格式输出评分结果：
{{{{
    "total_score": 85,
    "grade": "优秀",
    "dimensions": {{{{
        "content_theme": {{{{
            "score": 28,
            "max_score": 30,
            "comment": "内容充实，主题明确..."
        }}}},
        "structure": {{{{
            "score": 18,
            "max_score": 20,
            "comment": "结构清晰..."
        }}}},
        "language": {{{{
            "score": 22,
            "max_score": 25,
            "comment": "语言流畅..."
        }}}},
        "writing_norm": {{{{
            "score": 12,
            "max_score": 15,
            "comment": "错别字较少..."
        }}}},
        "creativity": {{{{
            "score": 5,
            "max_score": 10,
            "comment": "有一定创意..."
        }}}}
    }}}},
    "strengths": ["主题明确，情感真挚"],
    "weaknesses": ["结构略显单一"],
    "suggestions": ["建议增加更多细节描写"],
    "essay_type_analysis": {{{{
        "identified_type": "记叙文",
        "type_match_score": 0.9
    }}}}
}}}}
"""
