# 🔮 Fortune Dinner Recommender

오늘의 운세를 제공하고, 운세에 맞는 오늘의 식사를 추천해주는 웹 서비스입니다.

## 🌟 주요 특징

- **개인/그룹 운세**: 개인 또는 최대 10명 그룹의 종합 운세 제공
- **맞춤 메뉴 추천**: 운세에 따른 개인화된 식사 추천
- **이미지 공유**: 결과를 예쁜 이미지로 생성하여 SNS 공유
- **반응형 디자인**: 모바일과 데스크톱 모두 최적화
- **네트워크 접근**: 같은 Wi-Fi의 다른 기기에서 접근 가능

## 📋 프로젝트 구조

```
fortune-dinner-recommender/
├── backend/                    # Flask 백엔드
│   ├── app.py                 # 메인 Flask 애플리케이션
│   ├── fortune_engine.py      # 운세 생성 엔진
│   ├── menu_recommendation_engine.py  # 메뉴 추천 엔진
│   ├── models.py              # 데이터 모델
│   ├── validation.py          # 입력 검증
│   └── data/                  # JSON 데이터 파일
├── frontend/                   # 프론트엔드
│   ├── index.html             # 메인 HTML 파일
│   ├── styles.css             # CSS 스타일
│   └── script.js              # JavaScript 로직
├── docs/                       # 문서
│   ├── USER_GUIDE.md          # 사용법 가이드
│   ├── FEATURE_DOCUMENTATION.md  # 기능 문서
│   ├── LIMITATIONS_AND_IMPROVEMENTS.md  # 제한사항 및 개선점
│   └── FUTURE_ROADMAP.md      # 향후 개발 계획
├── start_network_server.py     # 네트워크 서버 시작 스크립트
├── test_network_access.py      # 네트워크 접근 테스트
└── NETWORK_DEPLOYMENT_GUIDE.md # 네트워크 배포 가이드
```

## 🚀 빠른 시작

### 간편 실행 (권장)
```bash
# 프로젝트 루트에서
python start_network_server.py
```

서버가 시작되면 표시되는 URL로 접속:
- **로컬 접근**: http://127.0.0.1:8001
- **네트워크 접근**: http://[로컬IP]:8001 (같은 Wi-Fi의 다른 기기에서)

### 네트워크 접근 테스트
```bash
python test_network_access.py
```

### 수동 실행

#### 1. 의존성 설치
```bash
cd fortune-dinner-recommender/backend
pip install -r requirements.txt
```

#### 2. 서버 실행
```bash
python app.py
```

#### 3. 브라우저 접속
- http://127.0.0.1:8001 (로컬)
- http://[로컬IP]:8001 (네트워크)

## 🎯 현재 구현 상태

### ✅ 완료된 기능
- **프로젝트 구조**: 완전한 프론트엔드/백엔드 분리 구조
- **운세 생성 엔진**: 개인/그룹 운세 생성 알고리즘 완성
- **메뉴 추천 시스템**: 운세 기반 개인화 메뉴 추천
- **반응형 UI**: 모바일/데스크톱 최적화 인터페이스
- **이미지 생성**: Canvas API 기반 공유 이미지 생성
- **네트워크 접근**: 로컬 네트워크에서 다기기 접근 지원
- **데이터 시스템**: JSON 기반 메뉴 및 운세 데이터베이스
- **입력 검증**: 완전한 사용자 입력 검증 시스템

### 🎨 주요 기능
- **4가지 운세 카테고리**: 사랑, 건강, 재물, 학업/직장
- **그룹 화합도 분석**: 참석자들의 운세 종합 분석
- **3가지 메뉴 추천**: 다양한 옵션으로 선택의 폭 제공
- **상세 메뉴 정보**: 재료, 조리시간, 난이도, 추천 이유
- **소셜 공유**: 예쁜 이미지로 결과 공유

## 🛠️ 기술 스택

**Frontend:**
- HTML5/CSS3/JavaScript (바닐라)
- 반응형 디자인
- Canvas API (이미지 생성 예정)

**Backend:**
- Python Flask
- Flask-CORS
- RESTful API

## 📱 지원 기능

- **개인 모드**: 개인의 생년월일로 운세와 식사 추천
- **그룹 모드**: 최대 10명까지 그룹 운세와 최적 메뉴 추천
- **반응형 디자인**: 모바일과 데스크톱 모두 지원
- **이미지 공유**: 결과를 이미지로 생성하여 공유 (구현 예정)

## � 모바일 접드근

### QR 코드로 쉬운 공유
1. 서버 시작 후 네트워크 URL 확인
2. QR 코드 생성기에 URL 입력 (추천: https://www.qr-code-generator.com/)
3. 생성된 QR 코드를 다른 기기에서 스캔

### 모바일 최적화 기능
- 터치 친화적 인터페이스
- PWA 지원 (홈 화면에 추가 가능)
- 세로/가로 모드 모두 지원
- 빠른 로딩 및 반응성

## 🔗 API 엔드포인트

- `GET /api/status`: 서버 상태 및 네트워크 정보 확인
- `POST /api/fortune`: 개인/그룹 운세 생성
- `POST /api/menu-recommendation`: 운세 기반 메뉴 추천
- `GET /`: 프론트엔드 메인 페이지

## 📚 문서

- **[사용법 가이드](docs/USER_GUIDE.md)**: 서비스 사용 방법 상세 안내
- **[기능 문서](docs/FEATURE_DOCUMENTATION.md)**: 모든 기능의 기술적 설명
- **[네트워크 배포 가이드](NETWORK_DEPLOYMENT_GUIDE.md)**: 네트워크 접근 설정 방법
- **[제한사항 및 개선점](docs/LIMITATIONS_AND_IMPROVEMENTS.md)**: 알려진 이슈와 개선 계획
- **[향후 개발 계획](docs/FUTURE_ROADMAP.md)**: 장기 개발 로드맵

## 🧪 테스트

### 기본 기능 테스트
```bash
python test_basic_functionality.py
```

### 통합 테스트
```bash
python test_integration.py
```

### 브라우저 테스트
```bash
python test_browser_functionality.py
```

### 전체 테스트 실행
```bash
python run_all_tests.py
```

## 🔧 문제 해결

### 일반적인 문제
1. **서버 연결 실패**: 방화벽 설정 확인
2. **모바일에서 접근 불가**: 같은 Wi-Fi 네트워크 연결 확인
3. **이미지 생성 실패**: 브라우저 Canvas API 지원 확인

### 지원 및 문의
- 네트워크 접근 문제: `NETWORK_DEPLOYMENT_GUIDE.md` 참조
- 기능 관련 문의: `FEATURE_DOCUMENTATION.md` 참조
- 사용법 문의: `USER_GUIDE.md` 참조

## 🌟 기여하기

이 프로젝트는 오픈소스 프로젝트입니다. 기여를 환영합니다!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자유롭게 사용, 수정, 배포할 수 있습니다.

---

🍀 **Fortune Dinner Recommender와 함께 즐거운 식사 시간 되세요!** 🍽️