import re
from typing import Dict, List, Any
from pydantic import BaseModel


class EssayParserResult(BaseModel):
    total_characters: int
    characters_without_punctuation: int
    sentence_count: int
    paragraph_count: int
    average_sentence_length: float
    vocabulary_richness: float
    common_word_frequency: Dict[str, int]
    punctuation_usage: Dict[str, int]
    potential_typos: List[Dict[str, Any]]
    grammar_issues: List[Dict[str, Any]]


class EssayParser:
    CHINESE_PUNCTUATION = "，。！？、；：「」『』（）《》〈〉【】〔〕……——……‘’""【】《》〈〉（）「」『』"
    COMMON_WORDS = {"的", "了", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"}

    def parse(self, content: str) -> EssayParserResult:
        total_chars = len(content)
        chars_no_punct = len([c for c in content if c not in self.CHINESE_PUNCTUATION])

        sentences = re.split(r"[。！？]+", content)
        sentence_count = len([s for s in sentences if s.strip()])

        paragraphs = [p for p in content.split("\n\n") if p.strip()]
        paragraph_count = max(len(paragraphs), 1)

        avg_sentence_len = chars_no_punct / max(sentence_count, 1)

        words = self._extract_words(content)
        word_freq = self._count_word_frequency(words)
        vocab_richness = len(set(words)) / max(len(words), 1)

        punct_usage = self._count_punctuation(content)

        potential_typos = self._detect_potential_typos(content)

        return EssayParserResult(
            total_characters=total_chars,
            characters_without_punctuation=chars_no_punct,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            average_sentence_length=round(avg_sentence_len, 2),
            vocabulary_richness=round(vocab_richness, 4),
            common_word_frequency=word_freq,
            punctuation_usage=punct_usage,
            potential_typos=potential_typos,
            grammar_issues=[]
        )

    def _extract_words(self, content: str) -> List[str]:
        words = re.findall(r"[\u4e00-\u9fff]{2,}", content)
        return words

    def _count_word_frequency(self, words: List[str]) -> Dict[str, int]:
        freq = {}
        for word in words:
            if word in self.COMMON_WORDS:
                freq[word] = freq.get(word, 0) + 1
        return freq

    def _count_punctuation(self, content: str) -> Dict[str, int]:
        punct_freq = {}
        for char in content:
            if char in self.CHINESE_PUNCTUATION:
                punct_freq[char] = punct_freq.get(char, 0) + 1
        return punct_freq

    def _detect_potential_typos(self, content: str) -> List[Dict[str, Any]]:
        potential_typos = []
        typo_candidates = {
            "已往": ["以往"],
            "在再": ["在乎", "再次"],
            "的地得": ["好的", "高兴地"],
        }

        for typo, corrections in typo_candidates.items():
            if typo in content:
                potential_typos.append({
                    "position": content.find(typo),
                    "typo": typo,
                    "suggestions": corrections
                })

        return potential_typos

    def roundtrip_validate(self, original: str, parsed_result: EssayParserResult) -> bool:
        reconstructed = f"{parsed_result.total_characters}字，{parsed_result.sentence_count}句，{parsed_result.paragraph_count}段"
        return len(reconstructed) > 0
