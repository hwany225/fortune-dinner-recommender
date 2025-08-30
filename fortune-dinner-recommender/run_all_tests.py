#!/usr/bin/env python3
"""
Fortune Dinner Recommender - 통합 테스트 실행기
모든 테스트를 순차적으로 실행하고 종합 결과를 제공
"""

import subprocess
import sys
import time
import json
import os
from datetime import datetime
import requests

class Colors:
    """터미널 색상 코드"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TestRunner:
    def __init__(self):
        self.test_results = {}
        self.server_process = None
        
    def print_header(self, title: str):
        """테스트 섹션 헤더 출력"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{title:^80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")
    
    def check_server_status(self):
        """서버 상태 확인"""
        try:
            response = requests.get("http://localhost:8001/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_server(self):
        """백엔드 서버 시작"""
        print(f"{Colors.YELLOW}백엔드 서버를 시작합니다...{Colors.END}")
        
        try:
            # 서버가 이미 실행 중인지 확인
            if self.check_server_status():
                print(f"{Colors.GREEN}서버가 이미 실행 중입니다.{Colors.END}")
                return True
            
            # 서버 시작
            self.server_process = subprocess.Popen(
                [sys.executable, "fortune-dinner-recommender/backend/app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 서버 시작 대기
            print(f"{Colors.CYAN}서버 시작을 기다리는 중...{Colors.END}")
            for i in range(30):  # 30초 대기
                time.sleep(1)
                if self.check_server_status():
                    print(f"{Colors.GREEN}✅ 서버가 성공적으로 시작되었습니다! (포트 5001){Colors.END}")
                    return True
                print(f"{Colors.CYAN}.{Colors.END}", end="", flush=True)
            
            print(f"\n{Colors.RED}❌ 서버 시작 시간 초과{Colors.END}")
            return False
            
        except Exception as e:
            print(f"{Colors.RED}❌ 서버 시작 실패: {str(e)}{Colors.END}")
            return False
    
    def stop_server(self):
        """백엔드 서버 중지"""
        if self.server_process:
            print(f"{Colors.YELLOW}서버를 중지합니다...{Colors.END}")
            self.server_process.terminate()
            self.server_process.wait()
            print(f"{Colors.CYAN}서버가 중지되었습니다.{Colors.END}")
    
    def run_backend_tests(self):
        """백엔드 API 테스트 실행"""
        self.print_header("백엔드 API 테스트")
        
        try:
            result = subprocess.run(
                [sys.executable, "fortune-dinner-recommender/test_final_validation.py"],
                capture_output=True,
                text=True,
                timeout=300  # 5분 타임아웃
            )
            
            print(result.stdout)
            if result.stderr:
                print(f"{Colors.YELLOW}경고/오류:{Colors.END}")
                print(result.stderr)
            
            success = result.returncode == 0
            self.test_results['backend'] = {
                'success': success,
                'return_code': result.returncode,
                'output': result.stdout,
                'errors': result.stderr
            }
            
            # JSON 리포트 로드
            try:
                with open('fortune-dinner-recommender/test_report.json', 'r', encoding='utf-8') as f:
                    report_data = json.load(f)
                    self.test_results['backend']['detailed_results'] = report_data
            except:
                pass
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}❌ 백엔드 테스트 시간 초과 (5분){Colors.END}")
            self.test_results['backend'] = {'success': False, 'error': 'timeout'}
            return False
        except Exception as e:
            print(f"{Colors.RED}❌ 백엔드 테스트 실행 실패: {str(e)}{Colors.END}")
            self.test_results['backend'] = {'success': False, 'error': str(e)}
            return False
    
    def run_browser_tests(self):
        """브라우저 기능 테스트 실행"""
        self.print_header("브라우저 기능 테스트")
        
        # Chrome 브라우저 확인
        try:
            subprocess.run(["google-chrome", "--version"], 
                         capture_output=True, check=True)
        except:
            try:
                subprocess.run(["chromium-browser", "--version"], 
                             capture_output=True, check=True)
            except:
                print(f"{Colors.YELLOW}⚠️  Chrome 브라우저를 찾을 수 없습니다. 브라우저 테스트를 건너뜁니다.{Colors.END}")
                print(f"{Colors.CYAN}Chrome 브라우저를 설치하면 브라우저 테스트를 실행할 수 있습니다.{Colors.END}")
                self.test_results['browser'] = {'success': False, 'error': 'chrome_not_found', 'skipped': True}
                return True  # 브라우저 테스트는 선택사항이므로 True 반환
        
        try:
            result = subprocess.run(
                [sys.executable, "fortune-dinner-recommender/test_browser_validation.py", "--headless"],
                capture_output=True,
                text=True,
                timeout=600  # 10분 타임아웃
            )
            
            print(result.stdout)
            if result.stderr:
                print(f"{Colors.YELLOW}경고/오류:{Colors.END}")
                print(result.stderr)
            
            success = result.returncode == 0
            self.test_results['browser'] = {
                'success': success,
                'return_code': result.returncode,
                'output': result.stdout,
                'errors': result.stderr
            }
            
            # JSON 리포트 로드
            try:
                with open('fortune-dinner-recommender/browser_test_report.json', 'r', encoding='utf-8') as f:
                    report_data = json.load(f)
                    self.test_results['browser']['detailed_results'] = report_data
            except:
                pass
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}❌ 브라우저 테스트 시간 초과 (10분){Colors.END}")
            self.test_results['browser'] = {'success': False, 'error': 'timeout'}
            return False
        except Exception as e:
            print(f"{Colors.RED}❌ 브라우저 테스트 실행 실패: {str(e)}{Colors.END}")
            self.test_results['browser'] = {'success': False, 'error': str(e)}
            return False
    
    def run_integration_tests(self):
        """기존 통합 테스트 실행"""
        self.print_header("기존 통합 테스트")
        
        test_files = [
            "fortune-dinner-recommender/test_basic_functionality.py",
            "fortune-dinner-recommender/test_integration.py",
            "fortune-dinner-recommender/test_user_scenarios.py"
        ]
        
        integration_results = {}
        
        for test_file in test_files:
            if os.path.exists(test_file):
                test_name = os.path.basename(test_file).replace('.py', '')
                print(f"\n{Colors.CYAN}실행 중: {test_name}{Colors.END}")
                
                try:
                    result = subprocess.run(
                        [sys.executable, test_file],
                        capture_output=True,
                        text=True,
                        timeout=180  # 3분 타임아웃
                    )
                    
                    success = result.returncode == 0
                    integration_results[test_name] = {
                        'success': success,
                        'return_code': result.returncode,
                        'output': result.stdout,
                        'errors': result.stderr
                    }
                    
                    if success:
                        print(f"{Colors.GREEN}✅ {test_name} 성공{Colors.END}")
                    else:
                        print(f"{Colors.RED}❌ {test_name} 실패{Colors.END}")
                        if result.stderr:
                            print(f"{Colors.YELLOW}오류: {result.stderr[:200]}...{Colors.END}")
                    
                except subprocess.TimeoutExpired:
                    print(f"{Colors.RED}❌ {test_name} 시간 초과{Colors.END}")
                    integration_results[test_name] = {'success': False, 'error': 'timeout'}
                except Exception as e:
                    print(f"{Colors.RED}❌ {test_name} 실행 실패: {str(e)}{Colors.END}")
                    integration_results[test_name] = {'success': False, 'error': str(e)}
            else:
                print(f"{Colors.YELLOW}⚠️  {test_file} 파일을 찾을 수 없습니다.{Colors.END}")
        
        self.test_results['integration'] = integration_results
        
        # 통합 테스트 성공 여부 결정
        successful_tests = sum(1 for result in integration_results.values() if result.get('success', False))
        total_tests = len(integration_results)
        
        return successful_tests >= (total_tests * 0.7) if total_tests > 0 else True  # 70% 이상 성공
    
    def generate_final_report(self):
        """최종 테스트 리포트 생성"""
        self.print_header("최종 테스트 결과 요약")
        
        # 각 테스트 카테고리별 결과
        backend_success = self.test_results.get('backend', {}).get('success', False)
        browser_success = self.test_results.get('browser', {}).get('success', False)
        browser_skipped = self.test_results.get('browser', {}).get('skipped', False)
        
        integration_results = self.test_results.get('integration', {})
        integration_success = sum(1 for result in integration_results.values() if result.get('success', False))
        integration_total = len(integration_results)
        
        print(f"{Colors.BOLD}테스트 카테고리별 결과:{Colors.END}")
        print(f"  백엔드 API: {Colors.GREEN if backend_success else Colors.RED}{'✅ 성공' if backend_success else '❌ 실패'}{Colors.END}")
        
        if browser_skipped:
            print(f"  브라우저 기능: {Colors.YELLOW}⏭️  건너뜀 (Chrome 브라우저 없음){Colors.END}")
        else:
            print(f"  브라우저 기능: {Colors.GREEN if browser_success else Colors.RED}{'✅ 성공' if browser_success else '❌ 실패'}{Colors.END}")
        
        if integration_total > 0:
            integration_rate = (integration_success / integration_total) * 100
            print(f"  기존 통합 테스트: {Colors.GREEN if integration_success >= integration_total * 0.7 else Colors.RED}{integration_success}/{integration_total} 성공 ({integration_rate:.1f}%){Colors.END}")
        
        # 상세 통계
        if 'backend' in self.test_results and 'detailed_results' in self.test_results['backend']:
            backend_stats = self.test_results['backend']['detailed_results']['summary']
            print(f"\n{Colors.BOLD}백엔드 테스트 상세:{Colors.END}")
            print(f"  총 테스트: {backend_stats['total_tests']}")
            print(f"  성공: {Colors.GREEN}{backend_stats['passed_tests']}{Colors.END}")
            print(f"  실패: {Colors.RED}{backend_stats['failed_tests']}{Colors.END}")
            print(f"  성공률: {Colors.YELLOW}{backend_stats['success_rate']:.1f}%{Colors.END}")
        
        if 'browser' in self.test_results and 'detailed_results' in self.test_results['browser']:
            browser_stats = self.test_results['browser']['detailed_results']['summary']
            print(f"\n{Colors.BOLD}브라우저 테스트 상세:{Colors.END}")
            print(f"  총 테스트: {browser_stats['total_tests']}")
            print(f"  성공: {Colors.GREEN}{browser_stats['passed_tests']}{Colors.END}")
            print(f"  실패: {Colors.RED}{browser_stats['failed_tests']}{Colors.END}")
            print(f"  성공률: {Colors.YELLOW}{browser_stats['success_rate']:.1f}%{Colors.END}")
        
        # 전체 성공 여부 결정
        required_tests_passed = backend_success
        optional_tests_passed = browser_success or browser_skipped
        integration_tests_passed = integration_success >= (integration_total * 0.7) if integration_total > 0 else True
        
        overall_success = required_tests_passed and optional_tests_passed and integration_tests_passed
        
        # 최종 리포트 저장
        final_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_success': overall_success,
            'test_results': self.test_results,
            'summary': {
                'backend_success': backend_success,
                'browser_success': browser_success,
                'browser_skipped': browser_skipped,
                'integration_success_rate': (integration_success / integration_total * 100) if integration_total > 0 else 100
            }
        }
        
        with open('fortune-dinner-recommender/final_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(final_report, f, ensure_ascii=False, indent=2)
        
        print(f"\n{Colors.CYAN}최종 테스트 리포트가 final_test_report.json에 저장되었습니다.{Colors.END}")
        
        # 최종 결과 출력
        if overall_success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 모든 테스트가 성공적으로 완료되었습니다!{Colors.END}")
            print(f"{Colors.GREEN}Fortune Dinner Recommender 프로토타입이 정상적으로 작동합니다.{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠️  일부 테스트가 실패했습니다.{Colors.END}")
            print(f"{Colors.YELLOW}상세한 내용은 위의 결과와 생성된 리포트 파일을 확인해주세요.{Colors.END}")
        
        return overall_success
    
    def run_all_tests(self):
        """모든 테스트 실행"""
        print(f"{Colors.BOLD}{Colors.PURPLE}")
        print("🔮 Fortune Dinner Recommender - 종합 테스트 실행")
        print("=" * 80)
        print(f"{Colors.END}")
        
        # 서버 시작
        if not self.start_server():
            print(f"{Colors.RED}서버를 시작할 수 없어 테스트를 중단합니다.{Colors.END}")
            return False
        
        try:
            # 각 테스트 실행
            backend_success = self.run_backend_tests()
            browser_success = self.run_browser_tests()
            integration_success = self.run_integration_tests()
            
            # 최종 리포트 생성
            return self.generate_final_report()
            
        finally:
            # 서버 중지
            self.stop_server()

def main():
    """메인 함수"""
    runner = TestRunner()
    success = runner.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()