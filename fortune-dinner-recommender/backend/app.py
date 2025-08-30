from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import json
import os
from datetime import datetime
from fortune_engine import FortuneEngine
from validation import validate_fortune_request
import socket

# 프론트엔드 파일 경로 설정
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')

app = Flask(__name__, static_folder=frontend_path, static_url_path='')

# 개발 환경에서 외부 접근을 위한 CORS 설정
CORS(app, origins=['*'], methods=['GET', 'POST', 'OPTIONS'], 
     allow_headers=['Content-Type', 'Authorization'])

# 보안 헤더 설정
@app.after_request
def after_request(response):
    # 기본 보안 헤더
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # 프로덕션 환경에서 HTTPS 강제
    is_production = os.environ.get('FLASK_ENV') == 'production'
    if is_production:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        # 프로덕션에서는 디버그 로그 제거
        if 'debug' in response.get_data(as_text=True).lower():
            pass  # 프로덕션에서는 디버그 정보 숨김
    
    return response

# 운세 엔진 초기화
fortune_engine = FortuneEngine()

@app.route('/')
def home():
    """메인 페이지 - 프론트엔드 index.html 서빙"""
    try:
        return send_from_directory(frontend_path, 'index.html')
    except FileNotFoundError:
        return jsonify({
            "message": "Fortune Dinner Recommender API",
            "version": "1.0.0",
            "status": "running",
            "note": "프론트엔드 파일을 찾을 수 없습니다. API 엔드포인트만 사용 가능합니다."
        })

@app.route('/<path:filename>')
def serve_static_files(filename):
    """정적 파일 서빙 (CSS, JS, 이미지 등)"""
    try:
        return send_from_directory(frontend_path, filename)
    except FileNotFoundError:
        return jsonify({"error": "파일을 찾을 수 없습니다"}), 404

def get_local_ip():
    """로컬 네트워크 IP 주소 가져오기"""
    try:
        # 외부 연결을 시도하여 로컬 IP 확인
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

@app.route('/api/status')
def api_status():
    """API 상태 확인 엔드포인트"""
    local_ip = get_local_ip()
    port = int(os.environ.get('PORT', 8001))
    
    return jsonify({
        "message": "Fortune Dinner Recommender API",
        "version": "1.0.0",
        "status": "running",
        "server_info": {
            "local_ip": local_ip,
            "port": port,
            "local_url": f"http://127.0.0.1:{port}",
            "network_url": f"http://{local_ip}:{port}",
            "debug_mode": app.debug
        },
        "frontend_path": frontend_path,
        "frontend_available": os.path.exists(os.path.join(frontend_path, 'index.html')),
        "access_info": {
            "local_access": f"http://127.0.0.1:{port}",
            "network_access": f"http://{local_ip}:{port}",
            "note": "네트워크 접근을 위해서는 방화벽 설정을 확인하세요"
        }
    })

@app.route('/api/fortune', methods=['POST'])
def generate_fortune():
    """운세 생성 API 엔드포인트"""
    try:
        # 프로덕션 환경 확인
        is_production = os.environ.get('FLASK_ENV') == 'production'
        
        # 디버깅을 위한 요청 정보 로깅 (개발 환경에서만)
        if not is_production:
            print(f"🔍 Fortune API 요청 받음")
            print(f"   Content-Type: {request.content_type}")
            print(f"   Method: {request.method}")
        
        # Content-Type 확인
        if not request.is_json:
            if not is_production:
                print(f"❌ Content-Type 오류: {request.content_type}")
            return jsonify({"error": "Content-Type은 application/json이어야 합니다"}), 400
        
        # 요청 데이터 가져오기
        try:
            data = request.get_json()
            if not is_production:
                print(f"📥 받은 데이터: {data}")
        except Exception as e:
            if not is_production:
                print(f"❌ JSON 파싱 오류: {e}")
            return jsonify({"error": "잘못된 JSON 형식입니다"}), 400
            
        if not data:
            if not is_production:
                print("❌ 빈 데이터")
            return jsonify({"error": "요청 데이터가 없습니다"}), 400
        
        # 입력 검증
        if not is_production:
            print(f"🔍 데이터 검증 시작...")
        validation_result = validate_fortune_request(data)
        if not is_production:
            print(f"🔍 검증 결과: {validation_result}")
        if not validation_result["valid"]:
            if not is_production:
                print(f"❌ 검증 실패: {validation_result['error']}")
            return jsonify({"error": validation_result["error"]}), 400
        
        # 현재 날짜
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 모드에 따른 운세 생성
        mode = data.get("mode", "individual")
        participants = data.get("participants", [])
        
        if mode == "individual":
            # 개인 모드
            if not participants or len(participants) != 1:
                return jsonify({"error": "개인 모드에서는 정확히 1명의 참석자가 필요합니다"}), 400
            
            participant = participants[0]
            birth_date = participant.get("birth_date")
            name = participant.get("name", "사용자")
            
            # 개인 운세 생성
            fortune = fortune_engine.generate_individual_fortune(birth_date, current_date, name)
            
            response = {
                "date": current_date,
                "mode": "individual",
                "individual_fortune": {
                    "name": name,
                    "birth_date": birth_date,
                    "fortune": {
                        category: {
                            "score": cat_fortune.score,
                            "message": cat_fortune.message,
                            "keywords": cat_fortune.keywords
                        }
                        for category, cat_fortune in fortune.categories.items()
                    },
                    "total_score": fortune.total_score
                }
            }
            
        elif mode == "group":
            # 그룹 모드
            if len(participants) < 2:
                return jsonify({"error": "그룹 모드에서는 최소 2명의 참석자가 필요합니다"}), 400
            
            if len(participants) > 10:
                return jsonify({"error": "그룹 모드에서는 최대 10명까지 가능합니다"}), 400
            
            # 생년월일과 이름 추출
            birth_dates = [p.get("birth_date") for p in participants]
            names = [p.get("name", f"참석자{i+1}") for i, p in enumerate(participants)]
            
            # 그룹 운세 생성
            group_fortune = fortune_engine.generate_group_fortune(birth_dates, current_date, names)
            
            # 개별 운세 정보 구성
            individual_fortunes = []
            for fortune in group_fortune.individual_fortunes:
                individual_fortunes.append({
                    "name": names[group_fortune.individual_fortunes.index(fortune)],
                    "birth_date": fortune.birth_date,
                    "fortune": {
                        category: {
                            "score": cat_fortune.score,
                            "message": cat_fortune.message,
                            "keywords": cat_fortune.keywords
                        }
                        for category, cat_fortune in fortune.categories.items()
                    },
                    "total_score": fortune.total_score
                })
            
            response = {
                "date": current_date,
                "mode": "group",
                "individual_fortunes": individual_fortunes,
                "group_fortune": {
                    "average_score": round(group_fortune.average_score, 1),
                    "harmony_score": round(group_fortune.harmony_score, 1),
                    "dominant_categories": group_fortune.dominant_categories,
                    "group_message": group_fortune.group_message,
                    "participant_count": group_fortune.participant_count
                }
            }
        
        else:
            return jsonify({"error": "지원하지 않는 모드입니다. 'individual' 또는 'group'을 사용하세요"}), 400
        
        return jsonify(response)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"서버 오류가 발생했습니다: {str(e)}"}), 500

@app.route('/api/menu-recommendation', methods=['POST'])
def recommend_menu():
    """메뉴 추천 API 엔드포인트"""
    try:
        # Content-Type 확인
        if not request.is_json:
            return jsonify({"error": "Content-Type은 application/json이어야 합니다"}), 400
        
        # 요청 데이터 가져오기
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({"error": "잘못된 JSON 형식입니다"}), 400
            
        if not data:
            return jsonify({"error": "요청 데이터가 없습니다"}), 400
        
        # 필수 필드 확인
        mode = data.get("mode")
        if not mode:
            return jsonify({"error": "mode 필드가 필요합니다"}), 400
        
        if mode not in ["individual", "group"]:
            return jsonify({"error": "mode는 'individual' 또는 'group'이어야 합니다"}), 400
        
        fortune_data = data.get("fortune_data")
        if not fortune_data:
            return jsonify({"error": "fortune_data 필드가 필요합니다"}), 400
        
        # 메뉴 추천 엔진 import 및 초기화
        from menu_recommendation_engine import get_recommendation_engine
        from models import Fortune, GroupFortune, CategoryFortune
        
        recommendation_engine = get_recommendation_engine()
        
        if mode == "individual":
            # 개인 모드 메뉴 추천
            individual_score = fortune_data.get("individual_score")
            if individual_score is None:
                return jsonify({"error": "개인 모드에서는 individual_score가 필요합니다"}), 400
            
            # 운세 데이터에서 Fortune 객체 재구성
            categories_data = fortune_data.get("categories", {})
            if not categories_data:
                return jsonify({"error": "categories 데이터가 필요합니다"}), 400
            
            categories = {}
            for cat_name, cat_data in categories_data.items():
                categories[cat_name] = CategoryFortune(
                    score=cat_data.get("score", individual_score),
                    message=cat_data.get("message", ""),
                    keywords=cat_data.get("keywords", [])
                )
            
            fortune = Fortune(
                date=fortune_data.get("date", datetime.now().strftime("%Y-%m-%d")),
                birth_date=fortune_data.get("birth_date", "1990-01-01"),
                categories=categories,
                total_score=individual_score
            )
            
            # 메뉴 추천 실행
            recommendations = recommendation_engine.recommend_for_individual(fortune, 3)
            
        elif mode == "group":
            # 그룹 모드 메뉴 추천
            group_score = fortune_data.get("group_score")
            harmony_score = fortune_data.get("harmony_score")
            participant_count = fortune_data.get("participant_count")
            
            if group_score is None or harmony_score is None or participant_count is None:
                return jsonify({
                    "error": "그룹 모드에서는 group_score, harmony_score, participant_count가 필요합니다"
                }), 400
            
            # 개별 운세들 재구성 (간단화된 버전)
            individual_fortunes = []
            individual_fortunes_data = fortune_data.get("individual_fortunes", [])
            
            for i in range(participant_count):
                if i < len(individual_fortunes_data):
                    ind_data = individual_fortunes_data[i]
                    categories = {}
                    # 'fortune' 키를 사용하는 구조 처리
                    fortune_categories = ind_data.get("fortune", ind_data.get("categories", {}))
                    for cat_name, cat_data in fortune_categories.items():
                        categories[cat_name] = CategoryFortune(
                            score=cat_data.get("score", group_score),
                            message=cat_data.get("message", ""),
                            keywords=cat_data.get("keywords", [])
                        )
                else:
                    # 기본 카테고리 생성
                    categories = {
                        "love": CategoryFortune(score=int(group_score), message="", keywords=[]),
                        "health": CategoryFortune(score=int(group_score), message="", keywords=[]),
                        "wealth": CategoryFortune(score=int(group_score), message="", keywords=[]),
                        "career": CategoryFortune(score=int(group_score), message="", keywords=[])
                    }
                
                fortune = Fortune(
                    date=fortune_data.get("date", datetime.now().strftime("%Y-%m-%d")),
                    birth_date=ind_data.get("birth_date", "1990-01-01") if i < len(individual_fortunes_data) else "1990-01-01",
                    categories=categories,
                    total_score=ind_data.get("total_score", int(group_score)) if i < len(individual_fortunes_data) else int(group_score)
                )
                individual_fortunes.append(fortune)
            
            # GroupFortune 객체 생성
            group_message = fortune_data.get("group_message", "").strip()
            if not group_message:
                group_message = "그룹의 운세가 조화롭게 어우러져 좋은 시간을 보낼 수 있을 것 같습니다."
            
            group_fortune = GroupFortune(
                average_score=group_score,
                harmony_score=harmony_score,
                dominant_categories=fortune_data.get("dominant_categories", []),
                group_message=group_message,
                participant_count=participant_count,
                individual_fortunes=individual_fortunes
            )
            
            # 메뉴 추천 실행
            recommendations = recommendation_engine.recommend_for_group(group_fortune, 3)
        
        # 추천 결과 포맷팅
        formatted_recommendations = []
        for rec in recommendations:
            formatted_rec = {
                "menu_id": rec.menu.id,
                "name": rec.menu.name,
                "category": rec.menu.category.value,
                "reason": rec.reason,
                "recommendation_score": rec.recommendation_score,
                "matched_keywords": rec.keyword_matches,
                "ingredients": rec.menu.ingredients,
                "cooking_time": rec.menu.cooking_time,
                "difficulty": rec.menu.difficulty.value,
                "description": rec.menu.description,
                "serving_size": f"{rec.menu.min_serving}-{rec.menu.max_serving}명",
                "sharing_type": rec.menu.sharing_type.value
            }
            
            # 그룹 모드에서만 추가 정보 제공
            if mode == "group":
                formatted_rec["group_benefit"] = "모든 참석자의 운세를 고려한 최적 메뉴"
                if rec.menu.sharing_type.value in ["shared", "both"]:
                    formatted_rec["group_benefit"] = "함께 나눠먹기 좋은 메뉴로 그룹 화합에 도움"
            
            formatted_recommendations.append(formatted_rec)
        
        response = {
            "mode": mode,
            "recommendations": formatted_recommendations,
            "recommendation_count": len(formatted_recommendations),
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"서버 오류가 발생했습니다: {str(e)}"}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8001))
    
    # 환경 확인
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    if not is_production:
        # 개발 환경에서만 로컬 IP 정보 출력
        local_ip = get_local_ip()
        
        print("=" * 60)
        print("🍀 Fortune Dinner Recommender 서버 시작")
        print("=" * 60)
        print(f"📍 로컬 접근: http://127.0.0.1:{port}")
        print(f"🌐 네트워크 접근: http://{local_ip}:{port}")
        print(f"📱 모바일에서 접근: http://{local_ip}:{port}")
        print("=" * 60)
        print("💡 팁:")
        print("  - 같은 Wi-Fi 네트워크의 다른 기기에서 네트워크 주소로 접근 가능")
        print("  - 방화벽에서 포트가 차단되어 있다면 설정을 확인하세요")
        print("  - API 상태 확인: /api/status")
        print("=" * 60)
    
    # 프로덕션에서는 gunicorn이 실행하므로 이 부분은 개발 환경에서만 실행
    if not is_production:
        app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
    else:
        # 프로덕션에서는 gunicorn이 앱을 실행
        print("🚀 프로덕션 모드로 실행 중...")