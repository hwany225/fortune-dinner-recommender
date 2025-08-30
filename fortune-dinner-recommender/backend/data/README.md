# 데이터베이스 문서

## 개요

이 디렉토리는 운세 기반 식사 추천 시스템의 핵심 데이터를 포함합니다. 메뉴 데이터베이스와 운세 템플릿 데이터로 구성되어 있으며, 개인 모드와 그룹 모드 모두를 지원합니다.

## 파일 구조

```
data/
├── menus.json              # 메뉴 데이터베이스 (JSON 형식)
├── fortune_templates.json  # 운세 템플릿 데이터 (JSON 형식)
└── README.md              # 이 문서
```

## 운세 템플릿 데이터 (fortune_templates.json)

### 개요
운세 생성을 위한 템플릿 데이터로, 4개 카테고리별 점수 구간에 따른 메시지와 키워드를 제공합니다.

### 구조

#### 카테고리 (categories)
- **사랑운 (love)** 💕: 연애, 인간관계 관련 운세
- **건강운 (health)** 💪: 신체적, 정신적 건강 관련 운세  
- **재물운 (wealth)** 💰: 금전, 재정 관련 운세
- **학업/직장운 (career)** 📚: 업무, 학습 관련 운세

#### 점수 구간별 메시지
각 카테고리는 5개 점수 구간으로 나뉩니다:
- **excellent (90-100점)**: 최고 운세, 4개 메시지 변형
- **good (70-89점)**: 좋은 운세, 4개 메시지 변형  
- **average (50-69점)**: 평범한 운세, 4개 메시지 변형
- **poor (30-49점)**: 좋지 않은 운세, 4개 메시지 변형
- **bad (1-29점)**: 나쁜 운세, 4개 메시지 변형

#### 그룹 메시지 (group_messages)
그룹 모드에서 화합 점수에 따른 메시지:
- **harmony_excellent (90-100점)**: 완벽한 화합
- **harmony_good (70-89점)**: 좋은 화합
- **harmony_average (50-69점)**: 평범한 화합
- **harmony_poor (30-49점)**: 아쉬운 화합
- **harmony_bad (1-29점)**: 좋지 않은 화합

#### 특별 조합 (special_combinations)
특정 조건을 만족할 때 나타나는 특별 메시지:
- **all_excellent**: 모든 카테고리 90점 이상
- **love_wealth_high**: 사랑운과 재물운 모두 80점 이상
- **health_career_high**: 건강운과 학업/직장운 모두 80점 이상
- **all_low**: 모든 카테고리 30점 이하

### 키워드 시스템
각 점수 구간마다 5개의 키워드가 제공되어 메뉴 추천 시 활용됩니다:

#### 높은 점수 키워드
- **로맨틱, 달콤한, 특별한, 행복한, 따뜻한** (사랑운 excellent)
- **활력적인, 건강한, 신선한, 에너지, 활기찬** (건강운 excellent)
- **풍성한, 고급스러운, 특별한, 화려한, 럭셔리** (재물운 excellent)
- **활력적인, 집중력, 성취감, 창의적인, 도전적인** (학업/직장운 excellent)

#### 낮은 점수 키워드
- **차분한, 조용한, 편안한, 안정적인, 건강한** (사랑운 bad)
- **부드러운, 따뜻한, 편안한, 회복, 영양가** (건강운 bad)
- **경제적인, 간소한, 실속있는, 합리적인, 검소한** (재물운 bad)
- **차분한, 조용한, 안정적인, 부드러운, 편안한** (학업/직장운 bad)

### 사용 방법

#### Python에서 운세 템플릿 사용
```python
from fortune_template_loader import FortuneTemplateLoader

# 템플릿 로더 초기화
loader = FortuneTemplateLoader()

# 카테고리별 운세 메시지 생성
love_message = loader.get_fortune_message('love', 85)
health_keywords = loader.get_fortune_keywords('health', 45)

# 그룹 화합 메시지 생성
harmony_message = loader.get_group_harmony_message(75)

# 특별 조합 확인
scores = {'love': 95, 'health': 92, 'wealth': 98, 'career': 91}
special = loader.check_special_combination(scores)
```

#### 편의 함수 사용
```python
from fortune_template_loader import (
    get_fortune_message, 
    get_fortune_keywords,
    get_group_harmony_message,
    check_special_combination
)

# 직접 함수 호출
message = get_fortune_message('wealth', 70)
keywords = get_fortune_keywords('career', 30)
```

### 데이터 통계
- **총 메시지 수**: 100개 (카테고리별 20개 + 그룹 메시지 20개)
- **총 키워드 수**: 100개 (카테고리별 25개)
- **그룹 메시지 구간**: 5개
- **특별 조합**: 4개

### 테스트
운세 템플릿 데이터의 무결성을 확인하려면:

```bash
python test_fortune_templates.py      # 데이터 구조 검증
python test_fortune_template_loader.py  # 로더 기능 테스트
```

## 메뉴 데이터 구조

### 기본 정보
- **총 메뉴 수**: 30개
- **카테고리**: 한식(10), 중식(5), 일식(5), 양식(5), 기타(5)
- **난이도 분포**: 쉬움(13), 보통(12), 어려움(5)
- **공유 타입**: 개인용(15), 공유용(8), 둘 다 가능(7)

### JSON 스키마

각 메뉴는 다음과 같은 구조를 가집니다:

```json
{
  "id": "korean_001",                    // 고유 식별자
  "name": "삼겹살 구이",                  // 메뉴 이름
  "category": "한식",                    // 카테고리 (한식/중식/일식/양식/기타)
  "score_range": [60, 90],              // 적합한 운세 점수 범위 [최소, 최대]
  "fortune_keywords": [                  // 연관 운세 키워드
    "화합", "즐거움", "사교", "에너지"
  ],
  "ingredients": [                       // 주요 재료 목록
    "삼겹살", "상추", "깻잎", "마늘", "쌈장", "김치"
  ],
  "cooking_time": "30분",               // 조리 시간
  "difficulty": "쉬움",                 // 난이도 (쉬움/보통/어려움)
  "description": "함께 구워먹는...",     // 메뉴 설명
  "min_serving": 2,                     // 최소 인원
  "max_serving": 8,                     // 최대 인원
  "sharing_type": "shared",             // 공유 타입 (individual/shared/both)
  "base_score": 75                      // 기본 추천 점수 (0-100)
}
```

## 카테고리별 메뉴 목록

### 한식 (10개)
1. **삼겹살 구이** - 그룹 모임용 대표 메뉴
2. **김치찌개** - 따뜻한 위로의 음식
3. **불고기** - 특별한 날 축하 메뉴
4. **비빔밥** - 영양 균형 개인 메뉴
5. **전골** - 대규모 그룹 화합 메뉴
6. **냉면** - 시원하고 깔끔한 개인 메뉴
7. **갈비찜** - 고급 특별 메뉴
8. **순두부찌개** - 부드러운 위로 음식
9. **된장찌개** - 전통 구수한 집밥
10. **떡볶이** - 추억의 간식 메뉴

### 중식 (5개)
1. **짜장면** - 친근한 위로 음식
2. **탕수육** - 축하용 달콤한 메뉴
3. **마파두부** - 매콤한 활력 메뉴
4. **짬뽕** - 자극적인 에너지 메뉴
5. **양장피** - 고급 시원한 메뉴

### 일식 (5개)
1. **초밥** - 최고급 정교한 메뉴
2. **라멘** - 따뜻한 위로 면요리
3. **돈카츠** - 든든한 에너지 메뉴
4. **우동** - 부드러운 간편 메뉴
5. **덴푸라** - 정교한 고급 튀김

### 양식 (5개)
1. **스테이크** - 최고급 성공 축하 메뉴
2. **파스타** - 로맨틱한 사랑 메뉴
3. **피자** - 그룹 파티 메뉴
4. **햄버거** - 캐주얼 간편 메뉴
5. **리조또** - 고급 로맨틱 메뉴

### 기타 (5개)
1. **샐러드** - 건강한 신선 메뉴
2. **치킨** - 파티용 간편 메뉴
3. **쌀국수** - 이국적 모험 메뉴
4. **타코** - 색다른 파티 메뉴
5. **카레** - 향신료 풍미 메뉴

## 운세 점수별 추천 가이드

### 낮은 점수 (1-40점)
- **추천 키워드**: 위로, 따뜻함, 건강, 회복
- **대표 메뉴**: 김치찌개, 순두부찌개, 짜장면, 라멘, 우동
- **특징**: 따뜻하고 부드러운 음식으로 기운 회복

### 중간 점수 (41-70점)
- **추천 키워드**: 균형, 만족, 간편, 일상
- **대표 메뉴**: 비빔밥, 돈카츠, 파스타, 햄버거, 된장찌개
- **특징**: 일상적이면서 만족스러운 음식

### 높은 점수 (71-100점)
- **추천 키워드**: 축하, 고급, 특별, 성공, 풍요
- **대표 메뉴**: 갈비찜, 초밥, 스테이크, 불고기, 탕수육
- **특징**: 고급스럽고 특별한 축하 음식

## 그룹 모드 고려사항

### 인원수별 적합 메뉴

#### 1-2명 (소규모)
- 개인용 메뉴 중심
- 예: 비빔밥, 냉면, 라멘, 파스타, 리조또

#### 3-4명 (중간 그룹)
- 개인용 + 공유 가능 메뉴
- 예: 김치찌개, 마파두부, 돈카츠, 타코, 카레

#### 5-8명 (대규모 그룹)
- 공유용 메뉴 중심
- 예: 삼겹살 구이, 전골, 갈비찜, 피자, 치킨

#### 9-10명 (최대 그룹)
- 대용량 공유 메뉴만
- 예: 전골, 치킨

### 화합 점수별 추천

#### 높은 화합 (70점 이상)
- **우선 추천**: 공유 음식 (shared 타입)
- **대표 메뉴**: 삼겹살 구이, 전골, 피자, 치킨
- **이유**: 함께 나눠먹으며 더욱 친밀감 증진

#### 낮은 화합 (70점 미만)
- **우선 추천**: 개인 음식 또는 둘 다 가능한 음식
- **대표 메뉴**: 비빔밥, 돈카츠, 카레, 타코
- **이유**: 개인 취향을 존중하면서 점진적 화합 도모

## 키워드 시스템

### 감정/분위기 키워드
- **긍정적**: 축하, 즐거움, 행복, 기쁨, 성공, 풍요
- **위로**: 따뜻함, 위로, 회복, 부드러움, 평안
- **활력**: 에너지, 활력, 자극, 도전, 모험

### 사회적 키워드
- **개인**: 로맨틱, 사랑, 우아, 여유, 정교
- **그룹**: 화합, 사교, 친목, 파티, 공유, 단합

### 건강/영양 키워드
- **건강**: 건강, 영양, 균형, 신선, 깔끔
- **전통**: 전통, 구수함, 집밥, 추억, 친근

## 사용 방법

### Python에서 메뉴 로드
```python
from menu_loader import MenuLoader

# 메뉴 로더 초기화
loader = MenuLoader()

# 모든 메뉴 조회
all_menus = loader.get_all_menus()

# 점수별 메뉴 조회
high_score_menus = loader.get_suitable_menus_for_score(85)

# 그룹용 메뉴 조회
group_menus = loader.get_suitable_menus_for_group(4, prefer_shared=True)

# 카테고리별 메뉴 조회
korean_menus = loader.filter_by_category(MenuCategory.KOREAN)
```

### 메뉴 추천 로직 예시
```python
def recommend_menu(fortune_score, group_size=1, harmony_score=50):
    loader = MenuLoader()
    
    # 1. 점수에 적합한 메뉴 필터링
    suitable_menus = loader.get_suitable_menus_for_score(fortune_score)
    
    # 2. 그룹 크기에 맞는 메뉴 필터링
    if group_size > 1:
        prefer_shared = harmony_score >= 70
        suitable_menus = [
            menu for menu in suitable_menus 
            if menu.is_suitable_for_group_size(group_size)
        ]
        
        if prefer_shared:
            shared_menus = [
                menu for menu in suitable_menus 
                if menu.sharing_type in ["shared", "both"]
            ]
            if shared_menus:
                suitable_menus = shared_menus
    
    # 3. 상위 3개 메뉴 반환
    return sorted(suitable_menus, key=lambda x: x.base_score, reverse=True)[:3]
```

## 데이터 확장 가이드

새로운 메뉴를 추가할 때는 다음 사항을 고려하세요:

1. **고유 ID**: `{category}_{number}` 형식 사용
2. **점수 범위**: 전체 점수 구간(1-100)을 고르게 커버
3. **인원수**: 다양한 그룹 크기 지원
4. **키워드**: 운세 카테고리와 연관성 있는 키워드 선택
5. **공유 타입**: 그룹 모드 지원을 위한 적절한 타입 설정

## 테스트

메뉴 데이터베이스의 무결성을 확인하려면:

```bash
python test_menu_database.py
```

이 테스트는 다음을 검증합니다:
- 데이터 무결성 (필수 필드, 유효한 값 범위)
- 카테고리별 분포
- 점수 범위 커버리지
- 그룹 크기 커버리지
- 키워드 기능
- ID 유일성
- 추천 로직 정확성