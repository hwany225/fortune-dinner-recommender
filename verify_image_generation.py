#!/usr/bin/env python3
"""
이미지 생성 기능 검증 스크립트
실제 기능이 작동하는지 간단히 확인합니다.
"""

import time
import requests
import json
from pathlib import Path

def check_server():
    """서버 상태 확인"""
    print("🔗 서버 상태를 확인합니다...")
    
    try:
        response = requests.get("http://localhost:5001", timeout=5)
        if response.status_code == 200:
            print("✅ 서버가 정상적으로 실행 중입니다.")
            return True
        else:
            print(f"❌ 서버 응답 오류: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 서버 연결 실패: {e}")
        return False

def test_fortune_api():
    """운세 API 테스트"""
    print("\n🔮 운세 API를 테스트합니다...")
    
    # 개인 모드 테스트
    individual_data = {
        "mode": "individual",
        "participants": [
            {"birth_date": "1990-01-01", "name": "테스트 사용자"}
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/api/fortune",
            json=individual_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 개인 운세 API 정상 작동")
            print(f"   총 점수: {result.get('individual_fortunes', [{}])[0].get('total_score', 'N/A')}")
        else:
            print(f"❌ 개인 운세 API 오류: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 개인 운세 API 테스트 실패: {e}")
        return False
    
    # 그룹 모드 테스트
    group_data = {
        "mode": "group",
        "participants": [
            {"birth_date": "1990-01-01", "name": "참석자1"},
            {"birth_date": "1992-05-15", "name": "참석자2"}
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/api/fortune",
            json=group_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 그룹 운세 API 정상 작동")
            print(f"   그룹 평균 점수: {result.get('group_fortune', {}).get('average_score', 'N/A')}")
        else:
            print(f"❌ 그룹 운세 API 오류: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 그룹 운세 API 테스트 실패: {e}")
        return False
    
    return True

def test_menu_api():
    """메뉴 추천 API 테스트"""
    print("\n🍽️  메뉴 추천 API를 테스트합니다...")
    
    menu_data = {
        "mode": "individual",
        "fortune_data": {
            "individual_score": 78,
            "categories": {
                "love": {"score": 85, "message": "좋은 사랑운", "keywords": ["행복", "만남"]},
                "health": {"score": 72, "message": "건강 주의", "keywords": ["휴식", "영양"]},
                "wealth": {"score": 90, "message": "재물운 상승", "keywords": ["투자", "기회"]},
                "career": {"score": 65, "message": "꾸준한 노력", "keywords": ["인내", "성장"]}
            },
            "date": "2024-01-15",
            "birth_date": "1990-01-01"
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/api/menu-recommendation",
            json=menu_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            recommendations = result.get('recommendations', [])
            print(f"✅ 메뉴 추천 API 정상 작동 ({len(recommendations)}개 메뉴 추천)")
            if recommendations:
                print(f"   첫 번째 추천: {recommendations[0].get('name', 'N/A')}")
        else:
            print(f"❌ 메뉴 추천 API 오류: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 메뉴 추천 API 테스트 실패: {e}")
        return False
    
    return True

def check_static_files():
    """정적 파일 접근 확인"""
    print("\n📁 정적 파일 접근을 확인합니다...")
    
    files_to_check = [
        "/",
        "/script.js",
        "/styles.css",
        "/test_image_generation.html"
    ]
    
    for file_path in files_to_check:
        try:
            response = requests.get(f"http://localhost:5001{file_path}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {file_path}: 접근 가능")
            else:
                print(f"❌ {file_path}: 응답 코드 {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {file_path}: 접근 실패 ({e})")
            return False
    
    return True

def create_manual_test_guide():
    """수동 테스트 가이드 생성"""
    print("\n📝 수동 테스트 가이드를 생성합니다...")
    
    guide = """# 이미지 생성 기능 수동 테스트 가이드

## 🚀 시작하기
1. 서버가 실행 중인지 확인: http://localhost:5001
2. 브라우저에서 위 주소로 접속

## 📋 테스트 시나리오

### 시나리오 1: 개인 모드 이미지 생성
1. "개인 운세" 버튼 클릭
2. 생년월일 입력 (예: 1990-01-01)
3. "운세 보기" 버튼 클릭
4. 결과 화면에서 "이미지로 공유" 버튼 클릭
5. 이미지 다운로드 확인

**예상 결과:**
- 파일명: `운세_개인_2024-01-15.png` (오늘 날짜)
- 이미지 내용: 제목, 날짜, 개인 운세 4개 카테고리, 메뉴 추천, 브랜딩

### 시나리오 2: 그룹 모드 이미지 생성
1. "그룹 운세" 버튼 클릭
2. 참석자 2명의 생년월일 입력
3. "운세 보기" 버튼 클릭
4. 그룹 결과에서 "이미지로 공유" 버튼 클릭
5. 이미지 다운로드 확인

**예상 결과:**
- 파일명: `운세_그룹_2024-01-15.png`
- 이미지 내용: 그룹 정보, 평균/화합 점수, 메뉴 추천, 브랜딩

### 시나리오 3: 테스트 페이지 확인
1. http://localhost:5001/test_image_generation.html 접속
2. "Canvas 지원 확인" 버튼 클릭
3. "개인 운세 이미지 생성" 버튼 클릭
4. "그룹 운세 이미지 생성" 버튼 클릭
5. 각 테스트 결과 메시지 확인

## 🔍 확인 사항
- [ ] 이미지가 정상적으로 생성되는가?
- [ ] 다운로드가 정상적으로 작동하는가?
- [ ] 이미지에 모든 정보가 포함되어 있는가?
- [ ] 텍스트가 읽기 쉽게 표시되는가?
- [ ] 그라데이션 배경이 적용되는가?
- [ ] 브랜딩 정보가 포함되어 있는가?

## 🐛 문제 해결
- 이미지가 생성되지 않으면: F12 개발자 도구에서 콘솔 오류 확인
- 다운로드가 안 되면: 브라우저 다운로드 설정 확인
- 서버 오류 시: 터미널에서 서버 로그 확인

## ✅ 테스트 완료 체크리스트
- [ ] 개인 모드 이미지 생성 및 다운로드
- [ ] 그룹 모드 이미지 생성 및 다운로드  
- [ ] 테스트 페이지 모든 기능 확인
- [ ] 다양한 브라우저에서 테스트 (Chrome, Firefox, Safari)
- [ ] 모바일 브라우저에서 테스트
"""
    
    try:
        with open("MANUAL_TEST_GUIDE.md", "w", encoding="utf-8") as f:
            f.write(guide)
        print("✅ 수동 테스트 가이드가 MANUAL_TEST_GUIDE.md에 저장되었습니다.")
        return True
    except Exception as e:
        print(f"❌ 가이드 생성 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("🧪 이미지 생성 기능 검증을 시작합니다...\n")
    
    # 서버 상태 확인
    if not check_server():
        print("❌ 서버가 실행되지 않았습니다. 먼저 서버를 시작해주세요:")
        print("   python backend/app.py")
        return False
    
    # API 테스트
    if not test_fortune_api():
        print("❌ 운세 API 테스트 실패")
        return False
    
    if not test_menu_api():
        print("❌ 메뉴 추천 API 테스트 실패")
        return False
    
    # 정적 파일 확인
    if not check_static_files():
        print("❌ 정적 파일 접근 실패")
        return False
    
    # 수동 테스트 가이드 생성
    create_manual_test_guide()
    
    print("\n" + "="*60)
    print("✅ 모든 자동 검증이 완료되었습니다!")
    print("="*60)
    print("🌐 이제 브라우저에서 수동 테스트를 진행하세요:")
    print("   1. http://localhost:5001 접속")
    print("   2. MANUAL_TEST_GUIDE.md 파일의 가이드를 따라 테스트")
    print("   3. 이미지 생성 및 다운로드 기능 확인")
    print("\n💡 테스트 페이지: http://localhost:5001/test_image_generation.html")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 검증 완료! 이제 브라우저에서 테스트해보세요.")
        else:
            print("\n❌ 검증 실패. 문제를 해결한 후 다시 시도해주세요.")
    except KeyboardInterrupt:
        print("\n⚠️  사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")