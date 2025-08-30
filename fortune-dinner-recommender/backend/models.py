# -*- coding: utf-8 -*-
"""
운세 및 메뉴 데이터 모델 정의
Fortune, GroupFortune, Menu 클래스와 JSON 스키마 검증 로직 구현
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import json
from enum import Enum


class DifficultyLevel(Enum):
    """요리 난이도 레벨"""
    EASY = "쉬움"
    MEDIUM = "보통"
    HARD = "어려움"


class SharingType(Enum):
    """음식 공유 타입"""
    INDIVIDUAL = "individual"  # 개인용
    SHARED = "shared"         # 공유용
    BOTH = "both"            # 둘 다 가능


class MenuCategory(Enum):
    """메뉴 카테고리"""
    KOREAN = "한식"
    CHINESE = "중식"
    JAPANESE = "일식"
    WESTERN = "양식"
    OTHER = "기타"


@dataclass
class CategoryFortune:
    """카테고리별 운세 정보"""
    score: int  # 1-100 점수
    message: str  # 운세 메시지
    keywords: List[str] = field(default_factory=list)  # 연관 키워드
    
    def __post_init__(self):
        """초기화 후 검증"""
        if not (1 <= self.score <= 100):
            raise ValueError("운세 점수는 1-100 사이여야 합니다")
        if not self.message.strip():
            raise ValueError("운세 메시지는 비어있을 수 없습니다")


@dataclass
class Fortune:
    """개인 운세 정보"""
    date: str  # YYYY-MM-DD 형식
    birth_date: str  # YYYY-MM-DD 형식
    categories: Dict[str, CategoryFortune]  # 카테고리별 운세
    total_score: int  # 전체 운세 점수
    
    def __post_init__(self):
        """초기화 후 검증"""
        # 날짜 형식 검증
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
            datetime.strptime(self.birth_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("날짜는 YYYY-MM-DD 형식이어야 합니다")
        
        # 필수 카테고리 확인
        required_categories = ["love", "health", "wealth", "career"]
        for category in required_categories:
            if category not in self.categories:
                raise ValueError(f"필수 카테고리 '{category}'가 누락되었습니다")
        
        # 전체 점수 검증
        if not (1 <= self.total_score <= 100):
            raise ValueError("전체 운세 점수는 1-100 사이여야 합니다")
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "date": self.date,
            "birth_date": self.birth_date,
            "categories": {
                name: {
                    "score": cat.score,
                    "message": cat.message,
                    "keywords": cat.keywords
                }
                for name, cat in self.categories.items()
            },
            "total_score": self.total_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Fortune':
        """딕셔너리에서 생성"""
        categories = {}
        for name, cat_data in data["categories"].items():
            categories[name] = CategoryFortune(
                score=cat_data["score"],
                message=cat_data["message"],
                keywords=cat_data.get("keywords", [])
            )
        
        return cls(
            date=data["date"],
            birth_date=data["birth_date"],
            categories=categories,
            total_score=data["total_score"]
        )


@dataclass
class GroupFortune:
    """그룹 운세 정보"""
    average_score: float  # 그룹 평균 점수
    harmony_score: float  # 그룹 화합 점수 (0-100)
    dominant_categories: List[str]  # 주요 운세 카테고리
    group_message: str  # 그룹 종합 메시지
    participant_count: int  # 참석자 수
    individual_fortunes: List[Fortune] = field(default_factory=list)  # 개별 운세들
    
    def __post_init__(self):
        """초기화 후 검증"""
        if not (0 <= self.average_score <= 100):
            raise ValueError("평균 점수는 0-100 사이여야 합니다")
        if not (0 <= self.harmony_score <= 100):
            raise ValueError("화합 점수는 0-100 사이여야 합니다")
        if self.participant_count < 2:
            raise ValueError("그룹은 최소 2명 이상이어야 합니다")
        if self.participant_count > 10:
            raise ValueError("그룹은 최대 10명까지 가능합니다")
        if not self.group_message.strip():
            raise ValueError("그룹 메시지는 비어있을 수 없습니다")
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "average_score": self.average_score,
            "harmony_score": self.harmony_score,
            "dominant_categories": self.dominant_categories,
            "group_message": self.group_message,
            "participant_count": self.participant_count,
            "individual_fortunes": [fortune.to_dict() for fortune in self.individual_fortunes]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GroupFortune':
        """딕셔너리에서 생성"""
        individual_fortunes = [
            Fortune.from_dict(fortune_data) 
            for fortune_data in data.get("individual_fortunes", [])
        ]
        
        return cls(
            average_score=data["average_score"],
            harmony_score=data["harmony_score"],
            dominant_categories=data["dominant_categories"],
            group_message=data["group_message"],
            participant_count=data["participant_count"],
            individual_fortunes=individual_fortunes
        )


@dataclass
class Menu:
    """메뉴 정보"""
    id: str  # 메뉴 고유 ID
    name: str  # 메뉴 이름
    category: MenuCategory  # 메뉴 카테고리
    score_range: Tuple[int, int]  # 적합한 운세 점수 범위 (min, max)
    fortune_keywords: List[str]  # 연관 운세 키워드
    ingredients: List[str]  # 재료 목록
    cooking_time: str  # 조리 시간 (예: "30분", "1시간")
    difficulty: DifficultyLevel  # 요리 난이도
    description: str  # 메뉴 설명
    min_serving: int  # 최소 인원
    max_serving: int  # 최대 인원
    sharing_type: SharingType  # 공유 타입
    base_score: int = 50  # 기본 추천 점수
    recommendation_score: int = 0  # 계산된 추천 점수 (동적)
    
    def __post_init__(self):
        """초기화 후 검증"""
        if not self.id.strip():
            raise ValueError("메뉴 ID는 비어있을 수 없습니다")
        if not self.name.strip():
            raise ValueError("메뉴 이름은 비어있을 수 없습니다")
        
        # 점수 범위 검증
        min_score, max_score = self.score_range
        if not (1 <= min_score <= 100) or not (1 <= max_score <= 100):
            raise ValueError("점수 범위는 1-100 사이여야 합니다")
        if min_score > max_score:
            raise ValueError("최소 점수가 최대 점수보다 클 수 없습니다")
        
        # 인원수 검증
        if self.min_serving < 1:
            raise ValueError("최소 인원은 1명 이상이어야 합니다")
        if self.max_serving < self.min_serving:
            raise ValueError("최대 인원이 최소 인원보다 작을 수 없습니다")
        
        # 기본 점수 검증
        if not (0 <= self.base_score <= 100):
            raise ValueError("기본 점수는 0-100 사이여야 합니다")
    
    def is_suitable_for_score(self, score: int) -> bool:
        """주어진 점수에 적합한 메뉴인지 확인"""
        return self.score_range[0] <= score <= self.score_range[1]
    
    def is_suitable_for_group_size(self, group_size: int) -> bool:
        """주어진 그룹 크기에 적합한 메뉴인지 확인"""
        return self.min_serving <= group_size <= self.max_serving
    
    def calculate_keyword_match_score(self, keywords: List[str]) -> int:
        """키워드 매칭 점수 계산"""
        matches = len(set(self.fortune_keywords) & set(keywords))
        return matches * 10  # 매칭당 10점
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "score_range": self.score_range,
            "fortune_keywords": self.fortune_keywords,
            "ingredients": self.ingredients,
            "cooking_time": self.cooking_time,
            "difficulty": self.difficulty.value,
            "description": self.description,
            "min_serving": self.min_serving,
            "max_serving": self.max_serving,
            "sharing_type": self.sharing_type.value,
            "base_score": self.base_score,
            "recommendation_score": self.recommendation_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Menu':
        """딕셔너리에서 생성"""
        return cls(
            id=data["id"],
            name=data["name"],
            category=MenuCategory(data["category"]),
            score_range=tuple(data["score_range"]),
            fortune_keywords=data["fortune_keywords"],
            ingredients=data["ingredients"],
            cooking_time=data["cooking_time"],
            difficulty=DifficultyLevel(data["difficulty"]),
            description=data["description"],
            min_serving=data["min_serving"],
            max_serving=data["max_serving"],
            sharing_type=SharingType(data["sharing_type"]),
            base_score=data.get("base_score", 50),
            recommendation_score=data.get("recommendation_score", 0)
        )