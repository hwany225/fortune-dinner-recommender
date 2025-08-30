# -*- coding: utf-8 -*-
"""
메뉴 데이터 로더 및 관리 유틸리티
JSON 파일에서 메뉴 데이터를 로드하고 필터링하는 기능 제공
"""

import json
import os
from typing import List, Dict, Any, Optional
from models import Menu, MenuCategory, DifficultyLevel, SharingType


class MenuLoader:
    """메뉴 데이터 로더 클래스"""
    
    def __init__(self, data_file_path: str = "data/menus.json"):
        """
        메뉴 로더 초기화
        
        Args:
            data_file_path: 메뉴 데이터 JSON 파일 경로
        """
        self.data_file_path = data_file_path
        self._menus: List[Menu] = []
        self._load_menus()
    
    def _load_menus(self) -> None:
        """JSON 파일에서 메뉴 데이터를 로드"""
        try:
            # 여러 경로를 시도해서 파일을 찾습니다
            possible_paths = [
                # 현재 파일 기준 상대 경로
                os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_file_path),
                # 프로젝트 루트 기준 경로
                os.path.join(os.getcwd(), 'backend', self.data_file_path),
                # Render 배포 환경 경로
                os.path.join('/opt/render/project/src', 'backend', self.data_file_path),
                # 작업 디렉토리 기준 경로
                os.path.join(os.getcwd(), self.data_file_path),
                # 상대 경로
                self.data_file_path,
                f'backend/{self.data_file_path}'
            ]
            
            file_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    file_path = path
                    break
            
            if file_path is None:
                raise FileNotFoundError(f"메뉴 데이터 파일을 찾을 수 없습니다. 시도한 경로들: {possible_paths}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._menus = []
            for menu_data in data.get("menus", []):
                try:
                    menu = Menu.from_dict(menu_data)
                    self._menus.append(menu)
                except Exception as e:
                    print(f"메뉴 로드 오류 (ID: {menu_data.get('id', 'unknown')}): {e}")
            
            print(f"총 {len(self._menus)}개의 메뉴를 로드했습니다.")
            
        except FileNotFoundError:
            print(f"메뉴 데이터 파일을 찾을 수 없습니다: {self.data_file_path}")
            self._menus = []
        except json.JSONDecodeError as e:
            print(f"JSON 파일 파싱 오류: {e}")
            self._menus = []
        except Exception as e:
            print(f"메뉴 로드 중 예상치 못한 오류: {e}")
            self._menus = []
    
    def get_all_menus(self) -> List[Menu]:
        """모든 메뉴 반환"""
        return self._menus.copy()
    
    def get_menu_by_id(self, menu_id: str) -> Optional[Menu]:
        """ID로 특정 메뉴 조회"""
        for menu in self._menus:
            if menu.id == menu_id:
                return menu
        return None
    
    def filter_by_category(self, category: MenuCategory) -> List[Menu]:
        """카테고리별 메뉴 필터링"""
        return [menu for menu in self._menus if menu.category == category]
    
    def filter_by_score_range(self, min_score: int, max_score: int) -> List[Menu]:
        """점수 범위로 메뉴 필터링"""
        return [
            menu for menu in self._menus 
            if menu.score_range[0] <= max_score and menu.score_range[1] >= min_score
        ]
    
    def filter_by_serving_size(self, serving_size: int) -> List[Menu]:
        """인원수로 메뉴 필터링"""
        return [
            menu for menu in self._menus 
            if menu.min_serving <= serving_size <= menu.max_serving
        ]
    
    def filter_by_sharing_type(self, sharing_type: SharingType) -> List[Menu]:
        """공유 타입으로 메뉴 필터링"""
        return [
            menu for menu in self._menus 
            if menu.sharing_type == sharing_type or menu.sharing_type == SharingType.BOTH
        ]
    
    def filter_by_difficulty(self, difficulty: DifficultyLevel) -> List[Menu]:
        """난이도로 메뉴 필터링"""
        return [menu for menu in self._menus if menu.difficulty == difficulty]
    
    def filter_by_keywords(self, keywords: List[str]) -> List[Menu]:
        """키워드로 메뉴 필터링 (교집합이 있는 메뉴)"""
        keyword_set = set(keywords)
        return [
            menu for menu in self._menus 
            if keyword_set & set(menu.fortune_keywords)
        ]
    
    def get_suitable_menus_for_score(self, score: int) -> List[Menu]:
        """특정 점수에 적합한 메뉴들 반환"""
        return [menu for menu in self._menus if menu.is_suitable_for_score(score)]
    
    def get_suitable_menus_for_group(self, group_size: int, 
                                   prefer_shared: bool = False) -> List[Menu]:
        """
        그룹 크기에 적합한 메뉴들 반환
        
        Args:
            group_size: 그룹 크기
            prefer_shared: 공유 음식 우선 여부
        """
        suitable_menus = [
            menu for menu in self._menus 
            if menu.is_suitable_for_group_size(group_size)
        ]
        
        if prefer_shared:
            # 공유 가능한 메뉴를 우선적으로 반환
            shared_menus = [
                menu for menu in suitable_menus 
                if menu.sharing_type in [SharingType.SHARED, SharingType.BOTH]
            ]
            if shared_menus:
                return shared_menus
        
        return suitable_menus
    
    def get_menu_statistics(self) -> Dict[str, Any]:
        """메뉴 데이터 통계 정보 반환"""
        if not self._menus:
            return {"total": 0}
        
        categories = {}
        difficulties = {}
        sharing_types = {}
        
        for menu in self._menus:
            # 카테고리별 통계
            cat_name = menu.category.value
            categories[cat_name] = categories.get(cat_name, 0) + 1
            
            # 난이도별 통계
            diff_name = menu.difficulty.value
            difficulties[diff_name] = difficulties.get(diff_name, 0) + 1
            
            # 공유 타입별 통계
            share_name = menu.sharing_type.value
            sharing_types[share_name] = sharing_types.get(share_name, 0) + 1
        
        return {
            "total": len(self._menus),
            "categories": categories,
            "difficulties": difficulties,
            "sharing_types": sharing_types,
            "score_ranges": {
                "min": min(menu.score_range[0] for menu in self._menus),
                "max": max(menu.score_range[1] for menu in self._menus)
            },
            "serving_sizes": {
                "min": min(menu.min_serving for menu in self._menus),
                "max": max(menu.max_serving for menu in self._menus)
            }
        }
    
    def reload_menus(self) -> None:
        """메뉴 데이터 다시 로드"""
        self._load_menus()


# 전역 메뉴 로더 인스턴스
menu_loader = MenuLoader()


def get_menu_loader() -> MenuLoader:
    """메뉴 로더 인스턴스 반환"""
    return menu_loader


# 편의 함수들
def get_all_menus() -> List[Menu]:
    """모든 메뉴 반환 (편의 함수)"""
    return menu_loader.get_all_menus()


def get_menus_by_category(category: str) -> List[Menu]:
    """카테고리별 메뉴 반환 (편의 함수)"""
    try:
        menu_category = MenuCategory(category)
        return menu_loader.filter_by_category(menu_category)
    except ValueError:
        return []


def get_menus_for_score(score: int) -> List[Menu]:
    """점수에 적합한 메뉴 반환 (편의 함수)"""
    return menu_loader.get_suitable_menus_for_score(score)


def get_menus_for_group(group_size: int, prefer_shared: bool = False) -> List[Menu]:
    """그룹에 적합한 메뉴 반환 (편의 함수)"""
    return menu_loader.get_suitable_menus_for_group(group_size, prefer_shared)


if __name__ == "__main__":
    # 테스트 코드
    print("=== 메뉴 데이터 로더 테스트 ===")
    
    # 통계 정보 출력
    stats = menu_loader.get_menu_statistics()
    print(f"메뉴 통계: {stats}")
    
    # 카테고리별 메뉴 테스트
    korean_menus = get_menus_by_category("한식")
    print(f"\n한식 메뉴 {len(korean_menus)}개:")
    for menu in korean_menus[:3]:  # 처음 3개만 출력
        print(f"- {menu.name}: {menu.description[:30]}...")
    
    # 점수별 메뉴 테스트
    high_score_menus = get_menus_for_score(85)
    print(f"\n85점에 적합한 메뉴 {len(high_score_menus)}개:")
    for menu in high_score_menus[:3]:
        print(f"- {menu.name}: 점수범위 {menu.score_range}")
    
    # 그룹 메뉴 테스트
    group_menus = get_menus_for_group(4, prefer_shared=True)
    print(f"\n4명 그룹용 공유 메뉴 {len(group_menus)}개:")
    for menu in group_menus[:3]:
        print(f"- {menu.name}: {menu.min_serving}-{menu.max_serving}명, {menu.sharing_type.value}")