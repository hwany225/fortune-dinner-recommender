# 네트워크 배포 가이드

Fortune Dinner Recommender를 로컬 네트워크에서 접근 가능하도록 배포하는 가이드입니다.

## 🚀 빠른 시작

### 1. 서버 시작
```bash
# 프로젝트 루트 디렉토리에서
python start_network_server.py
```

### 2. 접근 확인
- **로컬 접근**: http://127.0.0.1:8001
- **네트워크 접근**: http://[로컬IP]:8001 (서버 시작 시 표시됨)

### 3. 네트워크 접근 테스트
```bash
python test_network_access.py
```

## 📱 모바일/다른 기기에서 접근

### 같은 Wi-Fi 네트워크의 기기에서 접근
1. 서버 시작 시 표시되는 네트워크 URL 확인
2. 모바일 브라우저에서 해당 URL 입력
3. 예: `http://192.168.1.100:8001`

### QR 코드로 공유
1. 네트워크 URL을 QR 코드 생성기에 입력
2. 추천 사이트: https://www.qr-code-generator.com/
3. 생성된 QR 코드를 다른 기기에서 스캔

## 🔧 설정 및 문제 해결

### 포트 변경
```bash
# 환경 변수로 포트 설정
export PORT=8080
python start_network_server.py
```

### 방화벽 설정

#### macOS
```bash
# 시스템 환경설정 > 보안 및 개인 정보 보호 > 방화벽
# Python 또는 터미널 앱의 네트워크 접근 허용
```

#### Windows
```bash
# Windows Defender 방화벽 설정
# 앱 또는 기능이 방화벽을 통과하도록 허용
# Python 또는 해당 포트 허용
```

#### Linux
```bash
# UFW 사용 시
sudo ufw allow 8001

# iptables 사용 시
sudo iptables -A INPUT -p tcp --dport 8001 -j ACCEPT
```

### 일반적인 문제 해결

#### 1. 연결 거부 (Connection Refused)
- 서버가 실행 중인지 확인
- 올바른 포트 번호 사용 확인
- 방화벽 설정 확인

#### 2. 네트워크에서 접근 불가
- 같은 Wi-Fi 네트워크에 연결되어 있는지 확인
- 라우터에서 기기 간 통신이 허용되어 있는지 확인
- 회사/학교 네트워크의 경우 네트워크 정책 확인

#### 3. 느린 응답 속도
- 네트워크 상태 확인
- 서버 리소스 사용량 확인
- 동시 접속자 수 확인

## 🔒 보안 고려사항

### 개발 환경 보안
- 현재 설정은 개발 환경용입니다
- 프로덕션 환경에서는 추가 보안 설정 필요
- HTTPS 사용 권장 (프로덕션)

### 네트워크 보안
- 신뢰할 수 있는 네트워크에서만 사용
- 공용 Wi-Fi에서는 사용 주의
- 필요시 VPN 사용 고려

## 📊 모니터링 및 로그

### 서버 상태 확인
```bash
# API 상태 확인
curl http://localhost:8001/api/status

# 또는 브라우저에서
http://localhost:8001/api/status
```

### 로그 확인
- 서버 실행 시 콘솔에 로그 출력
- 오류 발생 시 상세 정보 확인 가능

## 🌐 고급 설정

### 환경 변수 설정
```bash
# .env 파일 생성 (선택사항)
cp .env.example .env
# 필요한 설정 수정
```

### 커스텀 도메인 사용 (로컬)
```bash
# /etc/hosts 파일 수정 (관리자 권한 필요)
127.0.0.1 fortune.local
192.168.1.100 fortune.local

# 접근: http://fortune.local:8001
```

### 리버스 프록시 설정 (고급)
nginx나 Apache를 사용하여 리버스 프록시 설정 가능

## 📱 모바일 최적화

### PWA 기능
- 현재 기본 PWA 기능 지원
- 모바일에서 홈 화면에 추가 가능
- 오프라인 기본 지원

### 모바일 브라우저 호환성
- iOS Safari: 완전 지원
- Android Chrome: 완전 지원
- 기타 모바일 브라우저: 기본 지원

## 🔄 업데이트 및 재시작

### 코드 업데이트 후
```bash
# 서버 중지 (Ctrl+C)
# 코드 수정
# 서버 재시작
python start_network_server.py
```

### 자동 재시작 (개발 중)
Flask의 debug 모드가 활성화되어 있어 코드 변경 시 자동 재시작됩니다.

## 📞 지원 및 문의

### 문제 발생 시
1. `test_network_access.py` 실행하여 상태 확인
2. 서버 로그 확인
3. 네트워크 설정 확인
4. 방화벽 설정 확인

### 추가 기능 요청
- GitHub Issues 또는 프로젝트 문서 참조
- 로컬 개발 환경에서 기능 테스트 후 요청