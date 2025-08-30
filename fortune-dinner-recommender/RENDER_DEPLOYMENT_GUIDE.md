# 🚀 Render.com 배포 가이드

## 📋 배포 준비 완료 체크리스트

✅ **requirements.txt** - Python 의존성 파일 생성 완료  
✅ **render.yaml** - Render 설정 파일 생성 완료  
✅ **프로덕션 보안 설정** - Flask 앱 프로덕션 모드 설정 완료  
✅ **디버그 로그 제거** - 프로덕션에서 민감한 정보 숨김 완료  

## 🎯 단계별 배포 가이드

### 1단계: GitHub 리포지토리 생성 (5분)

1. **GitHub에 로그인** 후 새 리포지토리 생성
   - 리포지토리 이름: `fortune-dinner-recommender`
   - Public 또는 Private 선택 (둘 다 가능)
   - README 체크 해제 (이미 있음)

2. **로컬 코드를 GitHub에 업로드**
   ```bash
   # 프로젝트 루트 디렉토리에서 실행
   cd fortune-dinner-recommender
   
   # Git 초기화 (아직 안 했다면)
   git init
   
   # 모든 파일 추가
   git add .
   
   # 커밋
   git commit -m "Initial commit: Fortune Dinner Recommender"
   
   # GitHub 리포지토리 연결 (YOUR_USERNAME을 실제 사용자명으로 변경)
   git remote add origin https://github.com/YOUR_USERNAME/fortune-dinner-recommender.git
   
   # 업로드
   git branch -M main
   git push -u origin main
   ```

### 2단계: Render.com 계정 생성 (2분)

1. **Render.com 접속**: https://render.com
2. **Sign Up** 클릭
3. **GitHub 계정으로 로그인** (권장)
   - "Continue with GitHub" 클릭
   - GitHub 권한 승인

### 3단계: 웹 서비스 생성 (10분)

1. **Dashboard에서 "New +" 클릭**
2. **"Web Service" 선택**
3. **GitHub 리포지토리 연결**
   - "Connect a repository" 클릭
   - `fortune-dinner-recommender` 리포지토리 선택
   - "Connect" 클릭

4. **서비스 설정**
   ```
   Name: fortune-dinner-recommender
   Region: Oregon (US West) 또는 가까운 지역
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: cd backend && gunicorn --bind 0.0.0.0:$PORT app:app
   ```

5. **환경 변수 설정**
   - "Advanced" 섹션 펼치기
   - "Add Environment Variable" 클릭
   - 다음 변수들 추가:
   ```
   FLASK_ENV = production
   PYTHON_VERSION = 3.11.0
   ```

6. **플랜 선택**
   - "Free" 플랜 선택 (월 750시간 무료)

7. **"Create Web Service" 클릭**

### 4단계: 배포 완료 및 확인 (5-10분)

1. **배포 진행 상황 확인**
   - 자동으로 빌드 로그 화면으로 이동
   - 빌드 과정을 실시간으로 확인 가능
   - "Build successful" 메시지 대기

2. **서비스 URL 확인**
   - 배포 완료 후 상단에 URL 표시
   - 예: `https://fortune-dinner-recommender.onrender.com`

3. **서비스 테스트**
   - 제공된 URL 클릭
   - Fortune Dinner Recommender 메인 페이지 확인
   - 개인/그룹 운세 기능 테스트

### 5단계: 커스텀 도메인 설정 (선택사항)

1. **도메인이 있다면**
   - Render Dashboard에서 "Settings" 탭
   - "Custom Domains" 섹션
   - "Add Custom Domain" 클릭
   - 도메인 입력 후 DNS 설정

## 🎉 배포 완료!

### 📱 접속 방법
- **메인 URL**: `https://your-app-name.onrender.com`
- **API 상태 확인**: `https://your-app-name.onrender.com/api/status`
- **모바일에서도 접속 가능**: 동일한 URL 사용

### 🔄 자동 배포 설정
- GitHub에 코드 푸시 시 자동으로 재배포
- 실시간 로그 확인 가능
- 롤백 기능 지원

## ⚠️ 주의사항

### 무료 플랜 제한사항
- **슬립 모드**: 15분간 비활성 시 자동 슬립
- **콜드 스타트**: 슬립 후 첫 접속 시 30초 정도 지연
- **월 750시간**: 한 달 사용 시간 제한

### 성능 최적화 팁
- **첫 접속 후 북마크**: 자주 사용할 URL 저장
- **정기적 접속**: 슬립 모드 방지를 위해 주기적 접속
- **업그레이드 고려**: 트래픽 증가 시 유료 플랜 검토

## 🛠️ 문제 해결

### 빌드 실패 시
1. **로그 확인**: 빌드 로그에서 오류 메시지 확인
2. **의존성 문제**: requirements.txt 파일 확인
3. **경로 문제**: 파일 경로 및 구조 확인

### 접속 불가 시
1. **URL 확인**: 올바른 Render URL 사용
2. **빌드 상태**: Dashboard에서 "Live" 상태 확인
3. **로그 확인**: Runtime 로그에서 오류 확인

### API 오류 시
1. **CORS 설정**: Flask-CORS 설정 확인
2. **환경 변수**: FLASK_ENV=production 설정 확인
3. **포트 설정**: $PORT 환경 변수 사용 확인

## 📞 다음 단계

### 🎯 즉시 가능한 개선사항
1. **커스텀 도메인 연결**
2. **Google Analytics 추가**
3. **SEO 최적화**
4. **소셜 미디어 공유 메타 태그**

### 🚀 장기적 개선 계획
1. **데이터베이스 연동** (PostgreSQL)
2. **사용자 계정 시스템**
3. **관리자 대시보드**
4. **API 사용량 모니터링**

---

## 🎉 축하합니다!

Fortune Dinner Recommender가 이제 전 세계 어디서든 접속 가능한 온라인 서비스가 되었습니다! 🌍

**공유하세요:**
- 친구들에게 URL 공유
- 소셜 미디어에 포스팅
- 포트폴리오에 추가

**피드백 수집:**
- 사용자 반응 확인
- 개선점 파악
- 새로운 기능 아이디어 수집