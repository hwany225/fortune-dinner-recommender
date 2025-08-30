# -*- coding: utf-8 -*-
"""
데이터 모델 사용 예시 데모
실제 사용 시나리오를 보여주는 예제 코드
"""

from models import (
    Fortune, GroupFortune, Menu, CategoryFortune,
    DifficultyLevel, SharingType, MenuCategory
)
from validation import validate_json_data, ValidationError
import json


def demo_individual_fortune():
    """개인 운세 생성 데모"""
    print("=== 개인 운세 생성 데모 ===")
    
    # 카테고리별 운세 생성
    categories = {
        "love": CategoryFortune(
            score=85,
            message="오늘은 특별한 만남이 기다리고 있습니다. 평소보다 적극적으로 행동해보세요.",
            keywords=["만남", "행복", "로맨스"]
        ),
        "health": CategoryFortune(
            score=72,
            message="컨디션이 좋지만 과로는 금물입니다. 충분한 휴식을 취하세요.",
            keywords=["휴식", "균형", "건강관리"]
        ),
        "wealth": CategoryFortune(
            score=90,
            message="재물운이 상승세입니다. 투자나 부업에 좋은 기회가 올 수 있어요.",
            keywords=["투자", "수익", "기회"]
        ),
        "career": CategoryFortune(
            score=68,
            message="직장에서 인정받을 일이 생길 것입니다. 성실함이 빛을 발하는 날이에요.",
            keywords=["성과", "인정", "성실"]
        )
    }
    
    # 개인 운세 생성
    fortune = Fortune(
        date="2024-01-15",
        birth_date="1990-05-20",
        categories=categories,
        total_score=79
    )
    
    print(f"날짜: {fortune.date}")
    print(f"생년월일: {fortune.birth_date}")
    print(f"총 운세 점수: {fortune.total_score}점")
    print("\n카테고리별 운세:")
    
    category_names = {
        "love": "사랑운",
        "health": "건강운", 
        "wealth": "재물운",
        "career": "직장운"
    }
    
    for category, cat_fortune in fortune.categories.items():
        print(f"  {category_names[category]}: {cat_fortune.score}점")
        print(f"    {cat_fortune.message}")
        print(f"    키워드: {', '.join(cat_fortune.keywords)}")
        print()
    
    return fortune


def demo_group_fortune():
    """그룹 운세 생성 데모"""
    print("=== 그룹 운세 생성 데모 ===")
    
    # 첫 번째 참석자 운세
    categories1 = {
        "love": CategoryFortune(85, "사랑운이 매우 좋습니다", ["만남", "행복"]),
        "health": CategoryFortune(72, "건강에 주의하세요", ["휴식", "균형"]),
        "wealth": CategoryFortune(90, "재물운이 상승합니다", ["투자", "수익"]),
        "career": CategoryFortune(68, "직장에서 좋은 소식이 있을 것입니다", ["성과", "인정"])
    }
    
    # 두 번째 참석자 운세
    categories2 = {
        "love": CategoryFortune(75, "평범한 사랑운입니다", ["안정", "평화"]),
        "health": CategoryFortune(88, "건강이 매우 좋습니다", ["활력", "에너지"]),
        "wealth": CategoryFortune(65, "재물운이 보통입니다", ["절약", "계획"]),
        "career": CategoryFortune(92, "직장운이 최고조입니다", ["승진", "성공"])
    }
    
    # 세 번째 참석자 운세
    categories3 = {
        "love": CategoryFortune(80, "새로운 인연이 기다립니다", ["인연", "설렘"]),
        "health": CategoryFortune(70, "컨디션 관리가 필요합니다", ["관리", "주의"]),
        "wealth": CategoryFortune(85, "금전운이 좋습니다", ["행운", "기회"]),
        "career": CategoryFortune(75, "꾸준한 노력이 결실을 맺습니다", ["노력", "결실"])
    }
    
    # 개별 운세들 생성
    fortune1 = Fortune("2024-01-15", "1990-05-20", categories1, 79)
    fortune2 = Fortune("2024-01-15", "1985-03-10", categories2, 80)
    fortune3 = Fortune("2024-01-15", "1992-08-15", categories3, 78)
    
    # 그룹 운세 생성
    group_fortune = GroupFortune(
        average_score=79.0,
        harmony_score=88.0,
        dominant_categories=["career", "love"],
        group_message="오늘 모임은 서로에게 좋은 영향을 주며 즐거운 시간이 될 것입니다. 특히 직장과 사랑 관련해서 좋은 이야기가 많이 나올 것 같아요!",
        participant_count=3,
        individual_fortunes=[fortune1, fortune2, fortune3]
    )
    
    print(f"참석자 수: {group_fortune.participant_count}명")
    print(f"그룹 평균 점수: {group_fortune.average_score:.1f}점")
    print(f"화합 점수: {group_fortune.harmony_score:.1f}점")
    print(f"주요 카테고리: {', '.join(group_fortune.dominant_categories)}")
    print(f"그룹 메시지: {group_fortune.group_message}")
    print()
    
    print("개별 참석자 운세:")
    for i, fortune in enumerate(group_fortune.individual_fortunes, 1):
        print(f"  참석자 {i}: 총 {fortune.total_score}점")
        for category, cat_fortune in fortune.categories.items():
            print(f"    {category}: {cat_fortune.score}점")
        print()
    
    return group_fortune


def demo_menu_creation():
    """메뉴 생성 데모"""
    print("=== 메뉴 데이터 생성 데모 ===")
    
    # 다양한 메뉴 생성
    menus = [
        Menu(
            id="korean_bbq_001",
            name="삼겹살 파티",
            category=MenuCategory.KOREAN,
            score_range=(70, 90),
            fortune_keywords=["화합", "즐거움", "모임", "행복"],
            ingredients=["삼겹살", "상추", "마늘", "된장찌개", "김치"],
            cooking_time="45분",
            difficulty=DifficultyLevel.EASY,
            description="친구들과 함께 즐기는 삼겹살 구이. 화합과 즐거움을 상징하는 대표적인 모임 음식입니다.",
            min_serving=2,
            max_serving=8,
            sharing_type=SharingType.SHARED,
            base_score=80
        ),
        Menu(
            id="italian_pasta_001",
            name="크림 파스타",
            category=MenuCategory.WESTERN,
            score_range=(60, 85),
            fortune_keywords=["로맨스", "만남", "특별함", "사랑"],
            ingredients=["파스타면", "생크림", "베이컨", "마늘", "파마산 치즈"],
            cooking_time="30분",
            difficulty=DifficultyLevel.MEDIUM,
            description="부드럽고 진한 맛의 크림 파스타. 특별한 날이나 로맨틱한 분위기에 완벽합니다.",
            min_serving=1,
            max_serving=4,
            sharing_type=SharingType.BOTH,
            base_score=70
        ),
        Menu(
            id="healthy_salad_001",
            name="그린 샐러드",
            category=MenuCategory.OTHER,
            score_range=(40, 70),
            fortune_keywords=["건강", "균형", "휴식", "관리"],
            ingredients=["양상추", "토마토", "오이", "올리브오일", "발사믹 식초"],
            cooking_time="15분",
            difficulty=DifficultyLevel.EASY,
            description="신선하고 건강한 그린 샐러드. 컨디션 관리가 필요한 날에 최적입니다.",
            min_serving=1,
            max_serving=6,
            sharing_type=SharingType.INDIVIDUAL,
            base_score=60
        )
    ]
    
    for menu in menus:
        print(f"메뉴: {menu.name} ({menu.category.value})")
        print(f"  ID: {menu.id}")
        print(f"  적합 점수 범위: {menu.score_range[0]}-{menu.score_range[1]}점")
        print(f"  인원: {menu.min_serving}-{menu.max_serving}명")
        print(f"  조리시간: {menu.cooking_time}")
        print(f"  난이도: {menu.difficulty.value}")
        print(f"  공유타입: {menu.sharing_type.value}")
        print(f"  설명: {menu.description}")
        print(f"  재료: {', '.join(menu.ingredients)}")
        print(f"  키워드: {', '.join(menu.fortune_keywords)}")
        print()
    
    return menus


def demo_validation():
    """검증 로직 데모"""
    print("=== JSON 스키마 검증 데모 ===")
    
    # 정상적인 요청 데이터
    valid_request = {
        "mode": "group",
        "participants": [
            {"birth_date": "1990-05-20", "name": "홍길동"},
            {"birth_date": "1985-03-10", "name": "김영희"},
            {"birth_date": "1992-08-15", "name": "이철수"}
        ]
    }
    
    print("정상적인 요청 데이터 검증:")
    print(json.dumps(valid_request, ensure_ascii=False, indent=2))
    
    try:
        validate_json_data(valid_request, "fortune_request")
        print("✓ 검증 통과!")
    except ValidationError as e:
        print(f"✗ 검증 실패: {e}")
    
    print()
    
    # 잘못된 요청 데이터
    invalid_request = {
        "mode": "group",
        "participants": [
            {"birth_date": "1990-05-20"}  # 그룹 모드인데 참석자가 1명만
        ]
    }
    
    print("잘못된 요청 데이터 검증:")
    print(json.dumps(invalid_request, ensure_ascii=False, indent=2))
    
    try:
        validate_json_data(invalid_request, "fortune_request")
        print("✓ 검증 통과!")
    except ValidationError as e:
        print(f"✗ 검증 실패: {e}")


def main():
    """메인 데모 함수"""
    print("🔮 운세 및 메뉴 데이터 모델 데모 🍽️")
    print("=" * 50)
    print()
    
    # 개인 운세 데모
    individual_fortune = demo_individual_fortune()
    print()
    
    # 그룹 운세 데모
    group_fortune = demo_group_fortune()
    print()
    
    # 메뉴 생성 데모
    menus = demo_menu_creation()
    print()
    
    # 검증 로직 데모
    demo_validation()
    print()
    
    print("=" * 50)
    print("데모가 완료되었습니다! 모든 데이터 모델이 정상적으로 작동합니다. ✨")
    
    # 실제 사용 예시
    print("\n실제 사용 예시:")
    print("1. Fortune 클래스로 개인 운세 생성 및 관리")
    print("2. GroupFortune 클래스로 그룹 운세 계산 및 화합도 분석")
    print("3. Menu 클래스로 메뉴 정보 관리 및 추천 로직 구현")
    print("4. JSON 스키마 검증으로 API 요청/응답 데이터 안전성 보장")


if __name__ == "__main__":
    main()