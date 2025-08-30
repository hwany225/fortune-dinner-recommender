# -*- coding: utf-8 -*-
"""
운세 생성 엔진
개인 및 그룹 운세 생성 알고리즘 구현
"""

import hashlib
import random
import statistics
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

from models import Fortune, CategoryFortune, GroupFortune
from fortune_template_loader import FortuneTemplateLoader


class FortuneEngine:
    """운세 생성 엔진 클래스"""
    
    def __init__(self):
        """초기화"""
        self.template_loader = FortuneTemplateLoader()
        self.categories = ["love", "health", "wealth", "career"]
    
    def generate_seed(self, birth_date: str, current_date: str) -> int:
        """
        생년월일과 현재 날짜를 조합하여 일관된 시드 생성
        
        Args:
            birth_date: 생년월일 (YYYY-MM-DD)
            current_date: 현재 날짜 (YYYY-MM-DD)
            
        Returns:
            int: 생성된 시드값
        """
        # 문자열을 조합하여 해시 생성
        combined_string = f"{birth_date}_{current_date}"
        hash_object = hashlib.md5(combined_string.encode())
        # 해시를 정수로 변환 (32비트 범위 내)
        seed = int(hash_object.hexdigest(), 16) % (2**31)
        return seed
    
    def generate_category_score(self, seed: int, category: str) -> int:
        """
        카테고리별 운세 점수 생성 (정규분포 기반)
        
        Args:
            seed: 기본 시드값
            category: 카테고리 이름
            
        Returns:
            int: 1-100 사이의 점수
        """
        # 카테고리별로 다른 시드 생성
        category_hash = hashlib.md5(category.encode()).hexdigest()
        category_seed = seed + int(category_hash[:8], 16)
        
        # 시드 설정
        random.seed(category_seed)
        
        # 정규분포를 따르는 점수 생성 (평균 60, 표준편차 20)
        score = random.normalvariate(60, 20)
        
        # 1-100 범위로 제한
        score = max(1, min(100, int(round(score))))
        
        return score
    
    def get_fortune_message_and_keywords(self, category: str, score: int) -> Tuple[str, List[str]]:
        """
        점수에 따른 운세 메시지와 키워드 가져오기
        
        Args:
            category: 카테고리 이름
            score: 운세 점수
            
        Returns:
            Tuple[str, List[str]]: (메시지, 키워드 리스트)
        """
        # 일관된 메시지 선택을 위해 시드 설정
        message_seed = score + hash(category)
        random.seed(message_seed)
        
        # FortuneTemplateLoader의 메서드 사용
        message = self.template_loader.get_fortune_message(category, score)
        keywords = self.template_loader.get_fortune_keywords(category, score)
        
        return message, keywords
    
    def calculate_total_score(self, category_scores: Dict[str, int]) -> int:
        """
        카테고리별 점수를 종합하여 전체 점수 계산
        
        Args:
            category_scores: 카테고리별 점수 딕셔너리
            
        Returns:
            int: 전체 운세 점수
        """
        if not category_scores:
            return 50
        
        # 단순 평균으로 계산
        total = sum(category_scores.values())
        average = total / len(category_scores)
        
        return int(round(average))
    
    def generate_individual_fortune(self, birth_date: str, current_date: str, name: str = "") -> Fortune:
        """
        개인 운세 생성
        
        Args:
            birth_date: 생년월일 (YYYY-MM-DD)
            current_date: 현재 날짜 (YYYY-MM-DD)
            name: 참석자 이름 (선택사항)
            
        Returns:
            Fortune: 생성된 개인 운세
        """
        # 시드 생성
        seed = self.generate_seed(birth_date, current_date)
        
        # 카테고리별 점수 및 운세 생성
        categories = {}
        category_scores = {}
        
        for category in self.categories:
            score = self.generate_category_score(seed, category)
            message, keywords = self.get_fortune_message_and_keywords(category, score)
            
            categories[category] = CategoryFortune(
                score=score,
                message=message,
                keywords=keywords
            )
            category_scores[category] = score
        
        # 전체 점수 계산
        total_score = self.calculate_total_score(category_scores)
        
        # Fortune 객체 생성
        fortune = Fortune(
            date=current_date,
            birth_date=birth_date,
            categories=categories,
            total_score=total_score
        )
        
        return fortune
    
    def calculate_group_harmony_score(self, individual_fortunes: List[Fortune]) -> float:
        """
        그룹 화합 점수 계산 (점수 편차 기반)
        
        Args:
            individual_fortunes: 개별 운세 리스트
            
        Returns:
            float: 화합 점수 (0-100)
        """
        if len(individual_fortunes) < 2:
            return 100.0
        
        # 전체 점수들 수집
        total_scores = [fortune.total_score for fortune in individual_fortunes]
        
        # 분산 계산
        variance = statistics.variance(total_scores)
        
        # 화합 점수 계산 (분산이 작을수록 높은 점수)
        # 최대 분산을 1000으로 가정하고 역비례 관계로 계산
        harmony_score = max(0, 100 - (variance / 10))
        
        return min(100, harmony_score)
    
    def find_dominant_categories(self, individual_fortunes: List[Fortune]) -> List[str]:
        """
        그룹의 주요 운세 카테고리 분석
        
        Args:
            individual_fortunes: 개별 운세 리스트
            
        Returns:
            List[str]: 주요 카테고리 리스트
        """
        # 카테고리별 점수 수집
        category_scores = defaultdict(list)
        
        for fortune in individual_fortunes:
            for category, category_fortune in fortune.categories.items():
                category_scores[category].append(category_fortune.score)
        
        # 카테고리별 평균 점수 계산
        category_averages = {}
        for category, scores in category_scores.items():
            category_averages[category] = sum(scores) / len(scores)
        
        # 평균 75점 이상인 카테고리를 주요 카테고리로 선정
        dominant_categories = []
        for category, avg_score in category_averages.items():
            if avg_score >= 75:
                dominant_categories.append(category)
        
        # 점수 순으로 정렬
        dominant_categories.sort(
            key=lambda cat: category_averages[cat], 
            reverse=True
        )
        
        return dominant_categories
    
    def generate_group_message(self, harmony_score: float) -> str:
        """
        화합 점수에 따른 그룹 메시지 생성
        
        Args:
            harmony_score: 화합 점수
            
        Returns:
            str: 그룹 메시지
        """
        # 일관된 메시지 선택을 위해 시드 설정
        message_seed = int(harmony_score * 100)
        random.seed(message_seed)
        
        # FortuneTemplateLoader의 메서드 사용
        return self.template_loader.get_group_harmony_message(int(harmony_score))
    
    def generate_group_fortune(self, birth_dates: List[str], current_date: str, names: List[str] = None) -> GroupFortune:
        """
        그룹 운세 생성
        
        Args:
            birth_dates: 참석자들의 생년월일 리스트
            current_date: 현재 날짜 (YYYY-MM-DD)
            names: 참석자 이름 리스트 (선택사항)
            
        Returns:
            GroupFortune: 생성된 그룹 운세
        """
        if len(birth_dates) < 2:
            raise ValueError("그룹은 최소 2명 이상이어야 합니다")
        
        if len(birth_dates) > 10:
            raise ValueError("그룹은 최대 10명까지 가능합니다")
        
        # 이름 리스트가 없으면 기본값 생성
        if names is None:
            names = [f"참석자{i+1}" for i in range(len(birth_dates))]
        
        # 개별 운세 생성
        individual_fortunes = []
        for i, birth_date in enumerate(birth_dates):
            name = names[i] if i < len(names) else f"참석자{i+1}"
            fortune = self.generate_individual_fortune(birth_date, current_date, name)
            individual_fortunes.append(fortune)
        
        # 그룹 평균 점수 계산
        total_scores = [fortune.total_score for fortune in individual_fortunes]
        average_score = sum(total_scores) / len(total_scores)
        
        # 화합 점수 계산
        harmony_score = self.calculate_group_harmony_score(individual_fortunes)
        
        # 주요 카테고리 분석
        dominant_categories = self.find_dominant_categories(individual_fortunes)
        
        # 그룹 메시지 생성
        group_message = self.generate_group_message(harmony_score)
        
        # GroupFortune 객체 생성
        group_fortune = GroupFortune(
            average_score=average_score,
            harmony_score=harmony_score,
            dominant_categories=dominant_categories,
            group_message=group_message,
            participant_count=len(birth_dates),
            individual_fortunes=individual_fortunes
        )
        
        return group_fortune