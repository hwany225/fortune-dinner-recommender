#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
운세 템플릿 로더 유틸리티
"""

import json
import os
import random
from typing import Dict, List, Optional, Tuple

class FortuneTemplateLoader:
    """운세 템플릿 데이터를 로드하고 관리하는 클래스"""
    
    def __init__(self, template_path: Optional[str] = None):
        """
        운세 템플릿 로더 초기화
        
        Args:
            template_path: 템플릿 파일 경로 (기본값: data/fortune_templates.json)
        """
        if template_path is None:
            template_path = os.path.join(os.path.dirname(__file__), 'data', 'fortune_templates.json')
        
        self.template_path = template_path
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """템플릿 파일을 로드합니다."""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"운세 템플릿 파일을 찾을 수 없습니다: {self.template_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"운세 템플릿 파일의 JSON 형식이 올바르지 않습니다: {e}")
    
    def get_category_info(self, category: str) -> Dict:
        """
        카테고리 정보를 반환합니다.
        
        Args:
            category: 카테고리 이름 (love, health, wealth, career)
            
        Returns:
            카테고리 정보 딕셔너리
        """
        if category not in self.templates['categories']:
            raise ValueError(f"존재하지 않는 카테고리입니다: {category}")
        
        return self.templates['categories'][category]
    
    def get_score_range_name(self, score: int) -> str:
        """
        점수에 해당하는 구간 이름을 반환합니다.
        
        Args:
            score: 운세 점수 (1-100)
            
        Returns:
            구간 이름 (excellent, good, average, poor, bad)
        """
        if not 1 <= score <= 100:
            raise ValueError(f"점수는 1-100 사이여야 합니다: {score}")
        
        if score >= 90:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 50:
            return "average"
        elif score >= 30:
            return "poor"
        else:
            return "bad"
    
    def get_fortune_message(self, category: str, score: int) -> str:
        """
        카테고리와 점수에 맞는 운세 메시지를 반환합니다.
        
        Args:
            category: 카테고리 이름
            score: 운세 점수
            
        Returns:
            운세 메시지
        """
        category_data = self.get_category_info(category)
        range_name = self.get_score_range_name(score)
        
        messages = category_data['score_ranges'][range_name]['messages']
        return random.choice(messages)
    
    def get_fortune_keywords(self, category: str, score: int) -> List[str]:
        """
        카테고리와 점수에 맞는 키워드 목록을 반환합니다.
        
        Args:
            category: 카테고리 이름
            score: 운세 점수
            
        Returns:
            키워드 목록
        """
        category_data = self.get_category_info(category)
        range_name = self.get_score_range_name(score)
        
        return category_data['score_ranges'][range_name]['keywords']
    
    def get_group_harmony_message(self, harmony_score: int) -> str:
        """
        그룹 화합 점수에 맞는 메시지를 반환합니다.
        
        Args:
            harmony_score: 그룹 화합 점수 (1-100)
            
        Returns:
            그룹 화합 메시지
        """
        range_name = self.get_score_range_name(harmony_score)
        harmony_range = f"harmony_{range_name}"
        
        if harmony_range not in self.templates['group_messages']:
            raise ValueError(f"존재하지 않는 그룹 메시지 구간입니다: {harmony_range}")
        
        messages = self.templates['group_messages'][harmony_range]['messages']
        return random.choice(messages)
    
    def check_special_combination(self, scores: Dict[str, int]) -> Optional[Tuple[str, str, List[str]]]:
        """
        특별한 점수 조합을 확인하고 해당하는 메시지와 키워드를 반환합니다.
        
        Args:
            scores: 카테고리별 점수 딕셔너리
            
        Returns:
            (조합명, 메시지, 키워드) 튜플 또는 None
        """
        # 모든 카테고리가 90점 이상인지 확인
        if all(score >= 90 for score in scores.values()):
            combo = self.templates['special_combinations']['all_excellent']
            return ('all_excellent', combo['message'], combo['keywords'])
        
        # 사랑운과 재물운이 모두 80점 이상인지 확인
        if scores.get('love', 0) >= 80 and scores.get('wealth', 0) >= 80:
            combo = self.templates['special_combinations']['love_wealth_high']
            return ('love_wealth_high', combo['message'], combo['keywords'])
        
        # 건강운과 학업/직장운이 모두 80점 이상인지 확인
        if scores.get('health', 0) >= 80 and scores.get('career', 0) >= 80:
            combo = self.templates['special_combinations']['health_career_high']
            return ('health_career_high', combo['message'], combo['keywords'])
        
        # 모든 카테고리가 30점 이하인지 확인
        if all(score <= 30 for score in scores.values()):
            combo = self.templates['special_combinations']['all_low']
            return ('all_low', combo['message'], combo['keywords'])
        
        return None
    
    def get_all_categories(self) -> List[str]:
        """모든 카테고리 이름을 반환합니다."""
        return list(self.templates['categories'].keys())
    
    def get_category_display_name(self, category: str) -> str:
        """카테고리의 표시 이름을 반환합니다."""
        category_data = self.get_category_info(category)
        return category_data['name']
    
    def get_category_icon(self, category: str) -> str:
        """카테고리의 아이콘을 반환합니다."""
        category_data = self.get_category_info(category)
        return category_data['icon']

# 전역 인스턴스 (싱글톤 패턴)
_template_loader = None

def get_template_loader() -> FortuneTemplateLoader:
    """전역 템플릿 로더 인스턴스를 반환합니다."""
    global _template_loader
    if _template_loader is None:
        _template_loader = FortuneTemplateLoader()
    return _template_loader

# 편의 함수들
def get_fortune_message(category: str, score: int) -> str:
    """운세 메시지를 반환하는 편의 함수"""
    return get_template_loader().get_fortune_message(category, score)

def get_fortune_keywords(category: str, score: int) -> List[str]:
    """운세 키워드를 반환하는 편의 함수"""
    return get_template_loader().get_fortune_keywords(category, score)

def get_group_harmony_message(harmony_score: int) -> str:
    """그룹 화합 메시지를 반환하는 편의 함수"""
    return get_template_loader().get_group_harmony_message(harmony_score)

def check_special_combination(scores: Dict[str, int]) -> Optional[Tuple[str, str, List[str]]]:
    """특별 조합을 확인하는 편의 함수"""
    return get_template_loader().check_special_combination(scores)