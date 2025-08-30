#!/bin/bash

# Fortune Dinner Recommender 백엔드 시작 스크립트

echo "🔮 Fortune Dinner Recommender 백엔드를 시작합니다..."

# 백엔드 디렉토리로 이동
cd backend

# 의존성 설치 확인
echo "📦 의존성을 확인하고 설치합니다..."
pip install -r requirements.txt

# Flask 서버 실행
echo "🚀 Flask 서버를 시작합니다..."
echo "서버 주소: http://localhost:5000"
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

python app.py