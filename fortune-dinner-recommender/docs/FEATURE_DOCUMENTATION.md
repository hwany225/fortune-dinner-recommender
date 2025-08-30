# 🔧 Fortune Dinner Recommender 기능 문서

## 📋 전체 기능 개요

Fortune Dinner Recommender는 생년월일 기반 운세 생성과 운세에 맞는 식사 추천을 제공하는 웹 애플리케이션입니다.

### 🎯 핵심 기능
1. **개인/그룹 운세 생성**
2. **운세 기반 메뉴 추천**
3. **결과 이미지 생성 및 공유**
4. **반응형 웹 인터페이스**
5. **네트워크 접근 지원**

## 🧮 운세 생성 시스템

### 알고리즘 특징
- **일관성**: 동일한 생년월일 + 날짜 = 동일한 운세
- **다양성**: 날짜별로 다른 패턴의 운세 생성
- **균형성**: 정규분포 기반 점수 생성 (평균 60점, 표준편차 20)

### 개인 운세 생성
```python
# 시드 생성: 생년월일 + 현재날짜
seed = hash(birth_date) + hash(current_date)

# 카테고리별 점수 생성 (1-100점)
categories = ["love", "health", "wealth", "career"]
for category in categories:
    category_seed = seed + hash(category)
    score = generate_normal_distribution_score(category_seed)
```

### 그룹 운세 생성
```python
# 개별 운세 생성 후 종합 분석
individual_fortunes = [generate_individual_fortune(bd) for bd in birth_dates]

# 그룹 평균 점수
average_score = sum(f.total_score for f in individual_fortunes) / len(individual_fortunes)

# 화합 점수 (점수 편차가 적을수록 높음)
score_variance = calculate_variance([f.total_score for f in individual_fortunes])
harmony_score = max(0, 100 - (score_variance / 10))
```

### 운세 카테고리
1. **사랑 (Love)**: 연애, 인간관계, 소통
2. **건강 (Health)**: 체력, 컨디션, 웰빙
3. **재물 (Wealth)**: 금전, 투자, 경제적 상황
4. **학업/직장 (Career)**: 업무, 학습, 성취

## 🍽️ 메뉴 추천 시스템

### 추천 알고리즘
1. **점수 기반 필터링**: 운세 점수 범위에 맞는 메뉴 선별
2. **키워드 매칭**: 운세 키워드와 메뉴 키워드 매칭
3. **그룹 최적화**: 인원수, 화합도, 공유 타입 고려
4. **다양성 보장**: 카테고리별 균형 있는 추천

### 메뉴 데이터 구조
```python
class Menu:
    id: str                    # 메뉴 고유 ID
    name: str                  # 메뉴 이름
    category: MenuCategory     # 한식, 중식, 일식, 양식, 기타
    score_range: (int, int)    # 적합한 운세 점수 범위
    fortune_keywords: [str]    # 연관 운세 키워드
    ingredients: [str]         # 주요 재료
    cooking_time: str          # 조리 시간
    difficulty: Difficulty     # 쉬움, 보통, 어려움
    min_serving: int           # 최소 인원
    max_serving: int           # 최대 인원
    sharing_type: SharingType  # individual, shared, both
```

### 개인 모드 추천 로직
```python
def recommend_for_individual(fortune, count=3):
    # 1. 점수 범위 필터링
    suitable_menus = filter_by_score_range(fortune.total_score)
    
    # 2. 키워드 매칭 점수 계산
    for menu in suitable_menus:
        menu.keyword_score = calculate_keyword_match(fortune, menu)
    
    # 3. 카테고리 다양성 고려하여 상위 메뉴 선택
    return select_diverse_menus(suitable_menus, count)
```

### 그룹 모드 추천 로직
```python
def recommend_for_group(group_fortune, count=3):
    # 1. 인원수 필터링
    suitable_menus = filter_by_serving_size(group_fortune.participant_count)
    
    # 2. 화합도 고려 공유 음식 우선
    if group_fortune.harmony_score >= 70:
        prioritize_shared_menus(suitable_menus)
    
    # 3. 그룹 종합 점수 기반 필터링
    score_filtered = filter_by_score_range(group_fortune.average_score)
    
    # 4. 최종 추천
    return select_group_optimized_menus(score_filtered, count)
```

## 🎨 프론트엔드 기능

### 반응형 디자인
- **모바일 우선**: 모바일에서 최적화된 UI
- **데스크톱 지원**: 큰 화면에서도 편리한 사용
- **터치 친화적**: 터치 인터페이스 최적화

### 사용자 인터페이스 컴포넌트

#### 1. 모드 선택 컴포넌트
```javascript
class ModeSelector {
    // 개인/그룹 모드 선택
    // 각 모드별 설명 표시
    // 선택에 따른 UI 전환
}
```

#### 2. 입력 컴포넌트
```javascript
class InputComponent {
    // 생년월일 입력 검증
    // 그룹 모드: 동적 참석자 추가/삭제
    // 실시간 입력 유효성 검사
}
```

#### 3. 결과 표시 컴포넌트
```javascript
class ResultDisplay {
    // 운세 점수 시각화 (프로그레스 바)
    // 메뉴 카드 레이아웃
    // 애니메이션 효과
}
```

#### 4. 이미지 생성 컴포넌트
```javascript
class ImageGenerator {
    // Canvas API 활용
    // 운세 정보 시각화
    // 다운로드 기능
}
```

### 상태 관리
```javascript
class AppState {
    mode: 'individual' | 'group'
    participants: Participant[]
    fortune_result: FortuneResult
    menu_recommendations: MenuRecommendation[]
    ui_state: UIState
}
```

## 🖼️ 이미지 생성 기능

### Canvas API 활용
- **동적 이미지 생성**: 운세 데이터를 시각적으로 표현
- **커스텀 디자인**: 브랜딩과 일관된 디자인
- **고해상도 지원**: 다양한 기기에서 선명한 이미지

### 이미지 구성 요소
1. **헤더**: 서비스 로고, 날짜
2. **운세 정보**: 카테고리별 점수, 총점
3. **메뉴 추천**: 추천 메뉴 이름, 이유
4. **푸터**: 브랜딩, 공유 정보

```javascript
function generateShareImage(fortuneData, menuData) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // 캔버스 크기 설정 (소셜미디어 최적화)
    canvas.width = 800;
    canvas.height = 1200;
    
    // 배경 그라디언트
    drawBackground(ctx);
    
    // 운세 정보 그리기
    drawFortuneInfo(ctx, fortuneData);
    
    // 메뉴 추천 그리기
    drawMenuRecommendations(ctx, menuData);
    
    // 브랜딩 요소
    drawBranding(ctx);
    
    return canvas.toDataURL('image/png');
}
```

## 🌐 네트워크 및 API

### RESTful API 설계
- **GET /api/status**: 서버 상태 확인
- **POST /api/fortune**: 운세 생성
- **POST /api/menu-recommendation**: 메뉴 추천

### API 응답 형식
```json
{
    "success": true,
    "data": {
        "date": "2024-01-15",
        "mode": "individual",
        "individual_fortune": {
            "name": "사용자",
            "total_score": 75,
            "fortune": {
                "love": {"score": 80, "message": "...", "keywords": [...]},
                "health": {"score": 70, "message": "...", "keywords": [...]}
            }
        }
    },
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### 오류 처리
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "생년월일 형식이 올바르지 않습니다",
        "details": "YYYY-MM-DD 형식으로 입력해주세요"
    }
}
```

## 🔒 보안 및 성능

### 보안 기능
1. **입력 검증**: 모든 사용자 입력 검증
2. **CORS 설정**: 허용된 도메인만 접근
3. **Rate Limiting**: API 호출 제한
4. **XSS 방지**: 입력 데이터 sanitization

### 성능 최적화
1. **캐싱**: 동일 요청 결과 캐싱 (1시간)
2. **압축**: gzip 응답 압축
3. **최적화된 이미지**: 적절한 해상도와 압축
4. **비동기 처리**: 논블로킹 API 처리

## 📱 PWA 기능

### Service Worker
```javascript
// 오프라인 지원
self.addEventListener('fetch', event => {
    if (event.request.url.includes('/api/')) {
        // API 요청은 네트워크 우선
        event.respondWith(networkFirst(event.request));
    } else {
        // 정적 파일은 캐시 우선
        event.respondWith(cacheFirst(event.request));
    }
});
```

### 매니페스트 파일
```json
{
    "name": "Fortune Dinner Recommender",
    "short_name": "Fortune Dinner",
    "description": "운세 기반 식사 추천 서비스",
    "start_url": "/",
    "display": "standalone",
    "theme_color": "#4CAF50",
    "background_color": "#ffffff",
    "icons": [...]
}
```

## 🧪 테스트 기능

### 자동화된 테스트
1. **단위 테스트**: 운세 생성, 메뉴 추천 알고리즘
2. **통합 테스트**: API 엔드포인트
3. **E2E 테스트**: 사용자 시나리오
4. **성능 테스트**: 응답 시간, 동시 접속

### 테스트 커버리지
- 운세 생성 엔진: 95%
- 메뉴 추천 엔진: 90%
- API 엔드포인트: 100%
- 프론트엔드 컴포넌트: 85%

## 🔄 확장 가능성

### 향후 추가 가능한 기능
1. **사용자 계정**: 운세 히스토리 저장
2. **소셜 기능**: 친구와 운세 비교
3. **AI 개선**: 머신러닝 기반 추천 개선
4. **다국어 지원**: 영어, 일본어 등
5. **음성 인터페이스**: 음성으로 운세 듣기
6. **위치 기반**: 근처 맛집 추천
7. **영양 정보**: 칼로리, 영양소 정보
8. **레시피 연동**: 상세 조리법 제공

### 기술적 확장
1. **마이크로서비스**: 기능별 서비스 분리
2. **데이터베이스**: PostgreSQL, MongoDB 연동
3. **클라우드 배포**: AWS, GCP 배포
4. **CDN**: 전 세계 빠른 접근
5. **모니터링**: 실시간 성능 모니터링

---

이 문서는 Fortune Dinner Recommender의 모든 기능과 기술적 구현 사항을 상세히 설명합니다. 각 기능은 사용자 경험과 기술적 안정성을 모두 고려하여 설계되었습니다.