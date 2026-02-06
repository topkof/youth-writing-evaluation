from typing import Dict, List, Tuple
from app.services.llm.base import LLMProvider, EssayScoringTemplate


ESSAY_TYPE_KEYWORDS = {
    "记叙文": ["我", "记得", "那天", "事情", "发生", "经过", "妈妈", "爸爸", "老师", "同学", "朋友", "小时候", "难忘"],
    "议论文": ["认为", "所以", "因为", "但是", "虽然", "如果", "应该", "必须", "道理", "观点", "支持", "反对"],
    "说明文": ["是什么", "怎样", "如何", "介绍", "特点", "原因", "方法", "步骤", "构成", "原理"],
    "读后感": ["读了", "书名", "这本书", "让我", "感悟", "体会", "启发", "深刻", "段落", "精彩"],
    "游记": ["旅行", "旅游", "景点", "美丽", "风景", "游览", "参观", "来到", "难忘", "景色"],
    "书信": ["亲爱的", "敬爱的", "您好", "此致敬礼", "祝您", "妈妈", "爸爸", "朋友", "老师", "一封信"],
    "诗歌": ["啊", "呀", "月亮", "太阳", "星星", "春风", "秋叶", "四季", "歌颂", "吟咏"]
}


ESSAY_TYPE_PATTERNS = {
    "记叙文": [
        r"^(我|我们|他|她).{0,20}(记得|想起|发生|那天)",
        r"(.|\n){50,}(最后|终于|从那以后)"
    ],
    "议论文": [
        r"(我认为|我觉得|在我看来)",
        r"(因为|所以|因此|但是|然而)"
    ],
    "说明文": [
        r"(什么是|怎样|如何)",
        r"(下面|首先|其次|最后)"
    ],
    "读后感": [
        r"(读了《|读完《)",
        r"(让我|使我|感受到)"
    ],
    "游记": [
        r"(来到|来到|游览|参观)",
        r"(美丽的|壮观的|难忘的)"
    ],
    "书信": [
        r"^(亲爱的|敬爱的|尊敬的)",
        r"(此致敬礼|祝您|身体健康)"
    ],
    "诗歌": [
        r"^(.|\n){0,20}(啊|呀|哦)",
        r"(.|\n){0,5}(月亮|太阳|星星|春风)"
    ]
}


class EssayClassifier:
    def __init__(self, llm_provider: LLMProvider = None):
        self.llm = llm_provider

    def classify(self, content: str, title: str = "") -> Dict[str, float]:
        scores = {}
        content_lower = content.lower()

        for essay_type, keywords in ESSAY_TYPE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in content)
            scores[essay_type] = score

        total = max(sum(scores.values()), 1)
        normalized_scores = {k: round(v / total, 4) for k, v in scores.items()}

        best_type = max(normalized_scores, key=normalized_scores.get)
        max_score = normalized_scores[best_type]

        return {
            "identified_type": best_type if max_score > 0.1 else "记叙文",
            "scores": normalized_scores,
            "confidence": min(max_score * 2, 1.0)
        }

    async def classify_with_llm(self, content: str, title: str = "") -> Dict[str, any]:
        if not self.llm:
            return self.classify(content, title)

        prompt = f"""请分析以下作文，判断其写作类型。

作文标题：{title or '无'}
作文内容：
---
{content[:500]}...
---

请判断这篇作文属于以下哪种类型：记叙文、议论文、说明文、读后感、游记、书信、诗歌。

请用JSON格式返回：
{{{{
    "essay_type": "类型",
    "confidence": 0.95,
    "reasons": ["理由1", "理由2"]
}}}}

只返回JSON，不要其他内容。"""

        from app.services.llm.base import LLMResponse
        response: LLMResponse = await self.llm.generate(
            prompt=prompt,
            temperature=0.3,
            max_tokens=512
        )

        import json
        try:
            result = json.loads(response.content.strip())
            return {
                "identified_type": result.get("essay_type", "记叙文"),
                "confidence": result.get("confidence", 0.5),
                "scores": {result.get("essay_type", "记叙文"): result.get("confidence", 0.5)},
                "reasons": result.get("reasons", [])
            }
        except Exception:
            return self.classify(content, title)
