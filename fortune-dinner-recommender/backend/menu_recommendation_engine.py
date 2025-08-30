# -*- coding: utf-8 -*-
"""
메뉴 추천 엔진
개인 및 그룹 모드에서 운세 기반 메뉴 추천 로직 구현
"""

import random
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from models import Menu, Fortune, GroupFortune, SharingType
from menu_loader import MenuLoader, get_menu_loader


@dataclass
class MenuRecommendation:
    """메뉴 추천 결과"""
    menu: Menu
    reason: str  # 추천 이유
    recommendation_score: int  # 최종 추천 점수
    keyword_matches: List[str]  # 매칭된 키워드들


class MenuRecommendationEngine:
    """메뉴 추천 엔진 클래스"""
    
    def __init__(self, menu_loader: Optional[MenuLoader] = None):
        """
        메뉴 추천 엔진 초기화
        
        Args:
            menu_loader: 메뉴 로더 인스턴스 (None이면 기본 로더 사용)
        """
        self.menu_loader = menu_loader or get_menu_loader()
    
    def recommend_for_individual(self, fortune: Fortune, 
                               num_recommendations: int = 3) -> List[MenuRecommendation]:
        """
        개인 모드 메뉴 추천
        
        Args:
            fortune: 개인 운세 정보
            num_recommendations: 추천할 메뉴 개수
            
        Returns:
            추천 메뉴 리스트
        """
        # 1. 운세 점수에 적합한 메뉴들 필터링
        suitable_menus = self._filter_by_score(fortune.total_score)
        
        if not suitable_menus:
            # 적합한 메뉴가 없으면 전체 메뉴에서 선택
            suitable_menus = self.menu_loader.get_all_menus()
        
        # 2. 키워드 매칭 및 점수 계산
        scored_menus = self._calculate_individual_scores(suitable_menus, fortune)
        
        # 3. 점수 순으로 정렬하고 상위 메뉴들 선택
        scored_menus.sort(key=lambda x: x.recommendation_score, reverse=True)
        
        # 4. 다양성을 위해 카테고리 중복 제거 (가능한 경우)
        diverse_menus = self._ensure_diversity(scored_menus, num_recommendations)
        
        return diverse_menus[:num_recommendations]
    
    def recommend_for_group(self, group_fortune: GroupFortune, 
                          num_recommendations: int = 3) -> List[MenuRecommendation]:
        """
        그룹 모드 메뉴 추천
        
        Args:
            group_fortune: 그룹 운세 정보
            num_recommendations: 추천할 메뉴 개수
            
        Returns:
            추천 메뉴 리스트
        """
        # 1. 인원수에 적합한 메뉴들 필터링
        suitable_menus = self._filter_by_group_size(group_fortune.participant_count)
        
        # 2. 화합 점수에 따른 공유 음식 우선 처리
        if group_fortune.harmony_score >= 70:
            shared_menus = self._filter_by_sharing_preference(suitable_menus, prefer_shared=True)
            if shared_menus:
                suitable_menus = shared_menus
        
        # 3. 그룹 평균 점수에 적합한 메뉴들로 추가 필터링
        score_filtered = self._filter_by_score_from_list(suitable_menus, group_fortune.average_score)
        if score_filtered:
            suitable_menus = score_filtered
        
        # 4. 그룹 키워드 매칭 및 점수 계산
        scored_menus = self._calculate_group_scores(suitable_menus, group_fortune)
        
        # 5. 점수 순으로 정렬하고 상위 메뉴들 선택
        scored_menus.sort(key=lambda x: x.recommendation_score, reverse=True)
        
        # 6. 다양성 확보
        diverse_menus = self._ensure_diversity(scored_menus, num_recommendations)
        
        return diverse_menus[:num_recommendations]
    
    def _filter_by_score(self, score: int) -> List[Menu]:
        """운세 점수에 적합한 메뉴들 필터링"""
        return self.menu_loader.get_suitable_menus_for_score(score)
    
    def _filter_by_score_from_list(self, menus: List[Menu], score: int) -> List[Menu]:
        """주어진 메뉴 리스트에서 점수에 적합한 메뉴들 필터링"""
        return [menu for menu in menus if menu.is_suitable_for_score(score)]
    
    def _filter_by_group_size(self, group_size: int) -> List[Menu]:
        """그룹 크기에 적합한 메뉴들 필터링"""
        return self.menu_loader.get_suitable_menus_for_group(group_size)
    
    def _filter_by_sharing_preference(self, menus: List[Menu], 
                                    prefer_shared: bool = True) -> List[Menu]:
        """공유 선호도에 따른 메뉴 필터링"""
        if prefer_shared:
            return [
                menu for menu in menus 
                if menu.sharing_type in [SharingType.SHARED, SharingType.BOTH]
            ]
        else:
            return [
                menu for menu in menus 
                if menu.sharing_type in [SharingType.INDIVIDUAL, SharingType.BOTH]
            ]
    
    def _calculate_individual_scores(self, menus: List[Menu], 
                                   fortune: Fortune) -> List[MenuRecommendation]:
        """개인 모드 메뉴 점수 계산"""
        recommendations = []
        
        # 운세에서 키워드 추출
        fortune_keywords = []
        for category_fortune in fortune.categories.values():
            fortune_keywords.extend(category_fortune.keywords)
        
        for menu in menus:
            # 기본 점수에서 시작
            score = menu.base_score
            
            # 키워드 매칭 보너스
            matched_keywords = list(set(menu.fortune_keywords) & set(fortune_keywords))
            keyword_bonus = len(matched_keywords) * 10
            score += keyword_bonus
            
            # 운세 점수와 메뉴 점수 범위의 적합도
            score_fit = self._calculate_score_fitness(fortune.total_score, menu.score_range)
            score += score_fit
            
            # 카테고리별 운세 점수 고려
            category_bonus = self._calculate_category_bonus(menu, fortune)
            score += category_bonus
            
            # 추천 이유 생성
            reason = self._generate_individual_reason(menu, fortune, matched_keywords)
            
            recommendations.append(MenuRecommendation(
                menu=menu,
                reason=reason,
                recommendation_score=score,
                keyword_matches=matched_keywords
            ))
        
        return recommendations
    
    def _calculate_group_scores(self, menus: List[Menu], 
                              group_fortune: GroupFortune) -> List[MenuRecommendation]:
        """그룹 모드 메뉴 점수 계산"""
        recommendations = []
        
        # 그룹의 주요 카테고리에서 키워드 추출
        group_keywords = []
        for individual_fortune in group_fortune.individual_fortunes:
            for category_name, category_fortune in individual_fortune.categories.items():
                if category_name in group_fortune.dominant_categories:
                    group_keywords.extend(category_fortune.keywords)
        
        # 중복 제거
        group_keywords = list(set(group_keywords))
        
        for menu in menus:
            # 기본 점수에서 시작
            score = menu.base_score
            
            # 키워드 매칭 보너스
            matched_keywords = list(set(menu.fortune_keywords) & set(group_keywords))
            keyword_bonus = len(matched_keywords) * 8  # 그룹에서는 개인보다 약간 낮게
            score += keyword_bonus
            
            # 화합 점수 보너스 (공유 음식일 때)
            if menu.sharing_type in [SharingType.SHARED, SharingType.BOTH]:
                harmony_bonus = int(group_fortune.harmony_score * 0.2)  # 최대 20점
                score += harmony_bonus
            
            # 그룹 평균 점수와의 적합도
            score_fit = self._calculate_score_fitness(group_fortune.average_score, menu.score_range)
            score += score_fit
            
            # 인원수 적합도 보너스
            group_size_bonus = self._calculate_group_size_bonus(menu, group_fortune.participant_count)
            score += group_size_bonus
            
            # 추천 이유 생성
            reason = self._generate_group_reason(menu, group_fortune, matched_keywords)
            
            recommendations.append(MenuRecommendation(
                menu=menu,
                reason=reason,
                recommendation_score=score,
                keyword_matches=matched_keywords
            ))
        
        return recommendations
    
    def _calculate_score_fitness(self, fortune_score: float, 
                               menu_score_range: Tuple[int, int]) -> int:
        """운세 점수와 메뉴 점수 범위의 적합도 계산"""
        min_score, max_score = menu_score_range
        
        if min_score <= fortune_score <= max_score:
            # 범위 내에 있으면 중앙에 가까울수록 높은 점수
            center = (min_score + max_score) / 2
            distance_from_center = abs(fortune_score - center)
            max_distance = (max_score - min_score) / 2
            fitness = 15 - (distance_from_center / max_distance * 15)
            return int(fitness)
        else:
            # 범위 밖이면 거리에 따라 감점
            if fortune_score < min_score:
                distance = min_score - fortune_score
            else:
                distance = fortune_score - max_score
            penalty = min(distance * 0.5, 10)  # 최대 10점 감점
            return int(-penalty)
    
    def _calculate_category_bonus(self, menu: Menu, fortune: Fortune) -> int:
        """카테고리별 운세 점수에 따른 보너스 계산"""
        bonus = 0
        
        # 각 카테고리의 점수가 높으면 관련 키워드가 있는 메뉴에 보너스
        for category_name, category_fortune in fortune.categories.items():
            if category_fortune.score >= 80:  # 높은 점수
                category_keywords = category_fortune.keywords
                matches = set(menu.fortune_keywords) & set(category_keywords)
                bonus += len(matches) * 5  # 매칭당 5점 보너스
        
        return bonus
    
    def _calculate_group_size_bonus(self, menu: Menu, group_size: int) -> int:
        """그룹 크기에 따른 적합도 보너스"""
        # 메뉴의 최적 인원수 범위 중앙에 가까울수록 보너스
        optimal_min = menu.min_serving
        optimal_max = menu.max_serving
        
        if optimal_min <= group_size <= optimal_max:
            # 범위 내에서 중앙에 가까울수록 높은 보너스
            center = (optimal_min + optimal_max) / 2
            distance_from_center = abs(group_size - center)
            max_distance = (optimal_max - optimal_min) / 2 if optimal_max > optimal_min else 1
            bonus = 10 - (distance_from_center / max_distance * 10)
            return int(bonus)
        
        return 0
    
    def _generate_individual_reason(self, menu: Menu, fortune: Fortune, 
                                  matched_keywords: List[str]) -> str:
        """개인 모드 추천 이유 생성"""
        reasons = []
        
        # 운세 점수 기반 이유
        if fortune.total_score >= 80:
            reasons.append("오늘의 운세가 매우 좋아서")
        elif fortune.total_score >= 60:
            reasons.append("오늘의 운세가 좋아서")
        elif fortune.total_score >= 40:
            reasons.append("오늘의 기운을 북돋기 위해")
        else:
            reasons.append("마음의 위로가 필요한 오늘")
        
        # 키워드 매칭 기반 이유
        if matched_keywords:
            if "건강" in matched_keywords:
                reasons.append("건강운이 좋은 오늘에 어울리는")
            if "사랑" in matched_keywords or "로맨틱" in matched_keywords:
                reasons.append("사랑운이 상승하는 오늘에 적합한")
            if "성공" in matched_keywords or "축하" in matched_keywords:
                reasons.append("성공운이 높은 오늘 축하할 만한")
            if "위로" in matched_keywords or "따뜻함" in matched_keywords:
                reasons.append("따뜻한 위로가 필요한 오늘에 좋은")
            if "에너지" in matched_keywords or "활력" in matched_keywords:
                reasons.append("활력이 필요한 오늘에 에너지를 주는")
        
        # 메뉴 특성 기반 이유
        if menu.difficulty.value == "쉬움":
            reasons.append("간편하게 만들 수 있는")
        elif menu.difficulty.value == "어려움" and fortune.total_score >= 70:
            reasons.append("도전해볼 만한")
        
        # 카테고리별 특성
        category_reasons = {
            "한식": "정겨운 한식",
            "중식": "풍미 깊은 중식",
            "일식": "정갈한 일식",
            "양식": "세련된 양식",
            "기타": "색다른"
        }
        
        if menu.category.value in category_reasons:
            reasons.append(category_reasons[menu.category.value])
        
        # 이유들을 자연스럽게 연결
        if len(reasons) >= 2:
            return f"{reasons[0]} {reasons[1]} 메뉴입니다."
        elif reasons:
            return f"{reasons[0]} 메뉴로 추천드립니다."
        else:
            return f"{menu.name}을(를) 추천드립니다."
    
    def _generate_group_reason(self, menu: Menu, group_fortune: GroupFortune, 
                             matched_keywords: List[str]) -> str:
        """그룹 모드 추천 이유 생성"""
        reasons = []
        
        # 그룹 화합 점수 기반 이유
        if group_fortune.harmony_score >= 80:
            reasons.append("그룹의 화합이 매우 좋아서")
        elif group_fortune.harmony_score >= 60:
            reasons.append("그룹의 분위기가 좋아서")
        else:
            reasons.append("그룹의 단합을 위해")
        
        # 공유 음식 여부
        if menu.sharing_type == SharingType.SHARED:
            reasons.append("함께 나눠먹을 수 있는")
        elif menu.sharing_type == SharingType.BOTH:
            reasons.append("개인별로도 함께도 즐길 수 있는")
        
        # 그룹 평균 점수 기반
        if group_fortune.average_score >= 75:
            reasons.append("그룹 전체의 운세가 좋은 오늘에 어울리는")
        elif group_fortune.average_score >= 50:
            reasons.append("그룹 모임에 적합한")
        else:
            reasons.append("그룹의 기운을 북돋을 수 있는")
        
        # 주요 카테고리 기반
        if "love" in group_fortune.dominant_categories:
            reasons.append("사랑운이 높은 그룹에게 좋은")
        if "wealth" in group_fortune.dominant_categories:
            reasons.append("재물운이 상승하는 그룹에게 적합한")
        if "health" in group_fortune.dominant_categories:
            reasons.append("건강운이 좋은 그룹에게 어울리는")
        
        # 인원수 고려
        if group_fortune.participant_count >= 6:
            reasons.append("대규모 모임에 적합한")
        elif group_fortune.participant_count <= 3:
            reasons.append("소규모 모임에 좋은")
        
        # 이유들을 자연스럽게 연결
        if len(reasons) >= 2:
            return f"{reasons[0]} {reasons[1]} 메뉴입니다."
        elif reasons:
            return f"{reasons[0]} 메뉴로 추천드립니다."
        else:
            return f"{menu.name}을(를) 그룹 메뉴로 추천드립니다."
    
    def _ensure_diversity(self, recommendations: List[MenuRecommendation], 
                         target_count: int) -> List[MenuRecommendation]:
        """추천 메뉴의 다양성 확보 (카테고리 중복 최소화)"""
        if len(recommendations) <= target_count:
            return recommendations
        
        diverse_recommendations = []
        used_categories = set()
        
        # 첫 번째 패스: 서로 다른 카테고리의 메뉴들 선택
        for rec in recommendations:
            if len(diverse_recommendations) >= target_count:
                break
            
            category = rec.menu.category.value
            if category not in used_categories:
                diverse_recommendations.append(rec)
                used_categories.add(category)
        
        # 두 번째 패스: 목표 개수에 못 미치면 점수 순으로 추가
        for rec in recommendations:
            if len(diverse_recommendations) >= target_count:
                break
            
            if rec not in diverse_recommendations:
                diverse_recommendations.append(rec)
        
        return diverse_recommendations
    
    def get_recommendation_explanation(self, recommendation: MenuRecommendation) -> Dict[str, Any]:
        """추천 결과에 대한 상세 설명 반환"""
        return {
            "menu_id": recommendation.menu.id,
            "menu_name": recommendation.menu.name,
            "category": recommendation.menu.category.value,
            "reason": recommendation.reason,
            "recommendation_score": recommendation.recommendation_score,
            "matched_keywords": recommendation.keyword_matches,
            "menu_details": {
                "ingredients": recommendation.menu.ingredients,
                "cooking_time": recommendation.menu.cooking_time,
                "difficulty": recommendation.menu.difficulty.value,
                "description": recommendation.menu.description,
                "serving_size": f"{recommendation.menu.min_serving}-{recommendation.menu.max_serving}명",
                "sharing_type": recommendation.menu.sharing_type.value
            }
        }


# 전역 추천 엔진 인스턴스
recommendation_engine = MenuRecommendationEngine()


def get_recommendation_engine() -> MenuRecommendationEngine:
    """추천 엔진 인스턴스 반환"""
    return recommendation_engine


# 편의 함수들
def recommend_individual_menus(fortune: Fortune, count: int = 3) -> List[MenuRecommendation]:
    """개인 모드 메뉴 추천 (편의 함수)"""
    return recommendation_engine.recommend_for_individual(fortune, count)


def recommend_group_menus(group_fortune: GroupFortune, count: int = 3) -> List[MenuRecommendation]:
    """그룹 모드 메뉴 추천 (편의 함수)"""
    return recommendation_engine.recommend_for_group(group_fortune, count)


if __name__ == "__main__":
    # 테스트 코드
    from fortune_engine import FortuneEngine
    from datetime import datetime
    
    print("=== 메뉴 추천 엔진 테스트 ===")
    
    # 운세 엔진으로 테스트 운세 생성
    fortune_engine = FortuneEngine()
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 개인 운세 테스트
    print("\n--- 개인 모드 테스트 ---")
    individual_fortune = fortune_engine.generate_individual_fortune("1990-05-15", current_date)
    print(f"개인 운세 점수: {individual_fortune.total_score}")
    
    individual_recommendations = recommend_individual_menus(individual_fortune)
    print(f"\n개인 추천 메뉴 {len(individual_recommendations)}개:")
    for i, rec in enumerate(individual_recommendations, 1):
        print(f"{i}. {rec.menu.name} (점수: {rec.recommendation_score})")
        print(f"   이유: {rec.reason}")
        print(f"   매칭 키워드: {rec.keyword_matches}")
    
    # 그룹 운세 테스트
    print("\n--- 그룹 모드 테스트 ---")
    birth_dates = ["1990-05-15", "1985-12-03", "1992-08-20", "1988-03-10"]
    names = ["참석자1", "참석자2", "참석자3", "참석자4"]
    
    group_fortune = fortune_engine.generate_group_fortune(birth_dates, current_date, names)
    print(f"그룹 평균 점수: {group_fortune.average_score:.1f}")
    print(f"그룹 화합 점수: {group_fortune.harmony_score:.1f}")
    print(f"주요 카테고리: {group_fortune.dominant_categories}")
    
    group_recommendations = recommend_group_menus(group_fortune)
    print(f"\n그룹 추천 메뉴 {len(group_recommendations)}개:")
    for i, rec in enumerate(group_recommendations, 1):
        print(f"{i}. {rec.menu.name} (점수: {rec.recommendation_score})")
        print(f"   이유: {rec.reason}")
        print(f"   공유타입: {rec.menu.sharing_type.value}")
        print(f"   인원: {rec.menu.min_serving}-{rec.menu.max_serving}명")