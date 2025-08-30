#!/bin/bash

# Fortune Dinner Recommender 프론트엔드 시작 스크립트

echo "🌐 Fortune Dinner Recommender 프론트엔드를 시작합니다..."

# 프론트엔드 디렉토리로 이동
cd frontend

# Python 내장 서버로 정적 파일 서빙
echo "🚀 프론트엔드 서버를 시작합니다..."
echo "서버 주소: http://localhost:8000"
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

python -m http.server 8000