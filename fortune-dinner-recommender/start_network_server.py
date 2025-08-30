#!/usr/bin/env python3
"""
Fortune Dinner Recommender - 네트워크 접근 가능한 서버 시작 스크립트

이 스크립트는 로컬 네트워크에서 접근 가능한 개발 서버를 시작합니다.
같은 Wi-Fi 네트워크의 다른 기기(모바일, 태블릿 등)에서 접근할 수 있습니다.
"""

import os
import sys
import socket
import subprocess
import platform
import webbrowser
from pathlib import Path

def get_local_ip():
    """로컬 네트워크 IP 주소 가져오기"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def check_port_available(port):
    """포트 사용 가능 여부 확인"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=8001):
    """사용 가능한 포트 찾기"""
    port = start_port
    while port < start_port + 100:
        if check_port_available(port):
            return port
        port += 1
    return None

def check_firewall_info():
    """방화벽 정보 및 가이드 제공"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return """
🔥 macOS 방화벽 설정:
  - 시스템 환경설정 > 보안 및 개인 정보 보호 > 방화벽
  - Python 또는 터미널 앱의 네트워크 접근 허용 확인
        """
    elif system == "Windows":
        return """
🔥 Windows 방화벽 설정:
  - Windows Defender 방화벽 > 앱 또는 기능이 Windows Defender 방화벽을 통과하도록 허용
  - Python 또는 해당 포트의 인바운드 규칙 허용
        """
    elif system == "Linux":
        return """
🔥 Linux 방화벽 설정:
  - UFW: sudo ufw allow [포트번호]
  - iptables: sudo iptables -A INPUT -p tcp --dport [포트번호] -j ACCEPT
        """
    else:
        return """
🔥 방화벽 설정:
  - 해당 포트에 대한 인바운드 연결을 허용하세요
        """

def main():
    print("🍀 Fortune Dinner Recommender - 네트워크 서버 시작")
    print("=" * 70)
    
    # 현재 디렉토리 확인
    current_dir = Path.cwd()
    backend_dir = current_dir / "backend"
    
    if not backend_dir.exists():
        print("❌ backend 디렉토리를 찾을 수 없습니다.")
        print("   fortune-dinner-recommender 프로젝트 루트에서 실행하세요.")
        sys.exit(1)
    
    # 포트 설정 (고정 포트 사용)
    port = 8001
    
    # 포트 사용 중인지 확인
    if not check_port_available(port):
        print(f"❌ 포트 {port}가 이미 사용 중입니다.")
        print("   다른 서버를 종료하거나 다른 포트를 사용하세요.")
        print(f"   현재 포트 {port} 사용 프로세스:")
        import subprocess
        try:
            result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
        except:
            pass
        sys.exit(1)
    
    # 네트워크 정보
    local_ip = get_local_ip()
    
    print(f"📍 서버 정보:")
    print(f"   로컬 접근: http://127.0.0.1:{port}")
    print(f"   네트워크 접근: http://{local_ip}:{port}")
    print(f"   포트: {port}")
    print()
    
    print("🌐 네트워크 접근 가이드:")
    print(f"   1. 같은 Wi-Fi 네트워크의 다른 기기에서 접근 가능")
    print(f"   2. 모바일/태블릿에서 http://{local_ip}:{port} 입력")
    print(f"   3. QR 코드 생성기로 URL을 QR 코드로 만들어 공유 가능")
    print()
    
    # 방화벽 정보
    print(check_firewall_info())
    print()
    
    # 환경 변수 설정
    os.environ['PORT'] = str(port)
    
    try:
        print("🚀 서버 시작 중...")
        print("   Ctrl+C로 서버를 중지할 수 있습니다.")
        print("=" * 70)
        
        # 백엔드 디렉토리로 이동하여 서버 시작
        os.chdir(backend_dir)
        
        # 브라우저에서 자동으로 열기 (선택사항)
        try:
            webbrowser.open(f"http://127.0.0.1:{port}")
        except:
            pass
        
        # Flask 서버 시작
        subprocess.run([sys.executable, "app.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n\n🛑 서버가 중지되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 서버 시작 중 오류 발생: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()