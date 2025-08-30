// 전역 변수
let currentMode = null;
// API 기본 URL 설정 (같은 서버에서 서빙되므로 상대 경로 사용)
const API_BASE_URL = window.location.origin;

// DOM 요소들
const modeSelectionSection = document.getElementById('mode-selection');
const inputSection = document.getElementById('input-section');
const resultsSection = document.getElementById('results-section');
const loadingSection = document.getElementById('loading-section');

const individualModeBtn = document.getElementById('individual-mode-btn');
const groupModeBtn = document.getElementById('group-mode-btn');

const inputTitle = document.getElementById('input-title');
const individualInput = document.getElementById('individual-input');
const groupInput = document.getElementById('group-input');

const participantCountSelect = document.getElementById('participant-count');
const participantsList = document.getElementById('participants-list');

const backBtn = document.getElementById('back-btn');
const generateFortuneBtn = document.getElementById('generate-fortune-btn');
const shareBtn = document.getElementById('share-btn');
const newFortuneBtn = document.getElementById('new-fortune-btn');

// 이벤트 리스너 등록
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    initializeApp();
});

// 앱 초기화 (개선된 버전)
function initializeApp() {
    // 진행률 표시기 초기 설정
    updateProgressIndicator('mode');
    
    // 버튼 초기 상태 설정
    generateFortuneBtn.disabled = true;
    generateFortuneBtn.classList.add('disabled');
    
    // 오늘 날짜를 max 값으로 설정
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('birth-date').max = today;
    
    // 네트워크 상태 감지 설정
    setupNetworkMonitoring();
    
    // 성능 모니터링 설정
    setupPerformanceMonitoring();
    
    // 접근성 개선 설정
    setupAccessibilityFeatures();
    
    // 환영 메시지 표시
    showNotification('운세와 식사 추천 서비스에 오신 것을 환영합니다! 🎉', 'success', 3000);
}

// 네트워크 상태 모니터링
function setupNetworkMonitoring() {
    // 온라인/오프라인 상태 감지
    window.addEventListener('online', () => {
        showNotification('인터넷 연결이 복구되었습니다. 🌐', 'success', 3000);
    });
    
    window.addEventListener('offline', () => {
        showNotification('인터넷 연결이 끊어졌습니다. 오프라인 모드로 전환됩니다. 📱', 'warning', 0);
    });
    
    // 초기 네트워크 상태 확인
    if (!navigator.onLine) {
        showNotification('현재 오프라인 상태입니다. 인터넷 연결을 확인해주세요. 📱', 'warning', 0);
    }
}

// 성능 모니터링
function setupPerformanceMonitoring() {
    // 페이지 로드 성능 측정
    window.addEventListener('load', () => {
        if (performance && performance.timing) {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            console.log(`페이지 로드 시간: ${loadTime}ms`);
            
            // 로드 시간이 3초 이상이면 알림
            if (loadTime > 3000) {
                showNotification('페이지 로딩이 느릴 수 있습니다. 네트워크 상태를 확인해주세요.', 'info', 4000);
            }
        }
    });
}

// 접근성 기능 설정
function setupAccessibilityFeatures() {
    // 고대비 모드 감지
    if (window.matchMedia && window.matchMedia('(prefers-contrast: high)').matches) {
        document.body.classList.add('high-contrast');
    }
    
    // 애니메이션 감소 모드 감지
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.body.classList.add('reduced-motion');
    }
    
    // 다크 모드 감지
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.classList.add('dark-mode');
    }
}

function initializeEventListeners() {
    // 모드 선택 버튼
    individualModeBtn.addEventListener('click', () => selectMode('individual'));
    groupModeBtn.addEventListener('click', () => selectMode('group'));
    
    // 네비게이션 버튼
    backBtn.addEventListener('click', goBackToModeSelection);
    generateFortuneBtn.addEventListener('click', generateFortune);
    shareBtn.addEventListener('click', shareResults);
    newFortuneBtn.addEventListener('click', startNewFortune);
    
    // 그룹 모드 참석자 수 변경
    participantCountSelect.addEventListener('change', updateParticipantInputs);
    
    // 개인 모드 생년월일 실시간 검증 (디바운스 적용)
    document.getElementById('birth-date').addEventListener('blur', validateIndividualInput);
    document.getElementById('birth-date').addEventListener('input', debounce(clearIndividualError, 300));
    
    // 키보드 접근성 향상
    document.addEventListener('keydown', handleKeyboardNavigation);
    
    // 스크롤 이벤트 (성능 최적화 적용)
    window.addEventListener('scroll', throttledScrollHandler);
    
    // 리사이즈 이벤트 (성능 최적화 적용)
    window.addEventListener('resize', debounce(() => {
        // 뷰포트 변경 시 레이아웃 조정
        const viewport = {
            width: window.innerWidth,
            height: window.innerHeight
        };
        console.log('뷰포트 변경:', viewport);
        
        // 모바일/데스크톱 전환 감지
        if (viewport.width <= 768) {
            document.body.classList.add('mobile-view');
        } else {
            document.body.classList.remove('mobile-view');
        }
    }, 250));
}

// 개인 모드 입력 실시간 검증
function validateIndividualInput() {
    if (currentMode !== 'individual') return;
    
    const birthDateInput = document.getElementById('birth-date');
    const birthDate = birthDateInput.value;
    
    clearFieldError(birthDateInput);
    
    if (birthDate) {
        if (!isValidBirthDate(birthDate)) {
            showFieldError(birthDateInput, '미래 날짜는 입력할 수 없습니다.');
        } else if (!isReasonableAge(birthDate)) {
            showFieldError(birthDateInput, '1900년 이후 날짜를 입력해주세요.');
        } else {
            showFieldSuccess(birthDateInput);
        }
    }
    
    // 입력 완성도 체크
    checkInputCompletion();
}

// 개인 모드 에러 메시지 제거
function clearIndividualError() {
    const birthDateInput = document.getElementById('birth-date');
    clearFieldError(birthDateInput);
    checkInputCompletion();
}

// 그룹 모드 참석자 입력 실시간 검증
function validateParticipantInput(inputElement) {
    const birthDate = inputElement.value;
    
    clearFieldError(inputElement);
    
    if (birthDate) {
        if (!isValidBirthDate(birthDate)) {
            showFieldError(inputElement, '미래 날짜는 입력할 수 없습니다.');
        } else if (!isReasonableAge(birthDate)) {
            showFieldError(inputElement, '1900년 이후 날짜를 입력해주세요.');
        } else {
            showFieldSuccess(inputElement);
        }
    }
    
    // 입력 완성도 체크
    checkInputCompletion();
}

// 필드별 에러 제거
function clearFieldError(inputElement) {
    const existingError = inputElement.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    inputElement.classList.remove('error', 'success');
}

// 필드 성공 상태 표시
function showFieldSuccess(inputElement) {
    clearFieldError(inputElement);
    inputElement.classList.add('success');
}

// 키보드 네비게이션 처리
function handleKeyboardNavigation(event) {
    // Enter 키로 다음 단계 진행
    if (event.key === 'Enter') {
        if (!modeSelectionSection.classList.contains('hidden')) {
            // 모드 선택 화면에서 Enter 키 처리
            const focusedElement = document.activeElement;
            if (focusedElement === individualModeBtn) {
                selectMode('individual');
            } else if (focusedElement === groupModeBtn) {
                selectMode('group');
            }
        } else if (!inputSection.classList.contains('hidden')) {
            // 입력 화면에서 Enter 키 처리
            if (document.activeElement !== generateFortuneBtn) {
                event.preventDefault();
                generateFortuneBtn.focus();
            }
        }
    }
    
    // Escape 키로 이전 단계로 돌아가기
    if (event.key === 'Escape') {
        if (!inputSection.classList.contains('hidden')) {
            goBackToModeSelection();
        } else if (!resultsSection.classList.contains('hidden')) {
            startNewFortune();
        }
    }
}

// 모드 선택 함수
function selectMode(mode) {
    currentMode = mode;
    
    // 에러 메시지 초기화
    clearErrorMessages();
    
    // 모드 선택 섹션 숨기기
    modeSelectionSection.classList.add('hidden');
    
    // 입력 섹션 표시
    inputSection.classList.remove('hidden');
    
    if (mode === 'individual') {
        inputTitle.textContent = '생년월일을 입력해주세요';
        individualInput.classList.remove('hidden');
        groupInput.classList.add('hidden');
        
        // 개인 모드 입력 필드 설정
        const birthDateInput = document.getElementById('birth-date');
        birthDateInput.max = new Date().toISOString().split('T')[0];
        birthDateInput.min = '1900-01-01';
        
        // 포커스 설정
        setTimeout(() => {
            birthDateInput.focus();
        }, 100);
        
    } else {
        inputTitle.textContent = '참석자들의 생년월일을 입력해주세요';
        individualInput.classList.add('hidden');
        groupInput.classList.remove('hidden');
        updateParticipantInputs(); // 초기 참석자 입력 필드 생성
        
        // 포커스 설정
        setTimeout(() => {
            participantCountSelect.focus();
        }, 100);
    }
    
    // 진행률 표시 업데이트
    updateProgressIndicator('input');
}

// 참석자 입력 필드 업데이트
function updateParticipantInputs() {
    const count = parseInt(participantCountSelect.value);
    participantsList.innerHTML = '';
    
    for (let i = 1; i <= count; i++) {
        const participantDiv = document.createElement('div');
        participantDiv.className = 'participant-input';
        
        participantDiv.innerHTML = `
            <label for="participant-${i}">참석자 ${i}</label>
            <input type="date" 
                   id="participant-${i}" 
                   name="participant-${i}" 
                   required
                   aria-describedby="participant-${i}-help"
                   max="${new Date().toISOString().split('T')[0]}">
            <small id="participant-${i}-help" class="input-help">생년월일을 선택해주세요</small>
        `;
        
        participantsList.appendChild(participantDiv);
        
        // 실시간 검증 이벤트 리스너 추가 (디바운스 적용)
        const input = document.getElementById(`participant-${i}`);
        input.addEventListener('blur', () => validateParticipantInput(input));
        input.addEventListener('input', debounce(() => clearFieldError(input), 300));
    }
    
    // 첫 번째 입력 필드에 포커스
    if (count > 0) {
        setTimeout(() => {
            document.getElementById('participant-1').focus();
        }, 100);
    }
}

// 모드 선택으로 돌아가기
function goBackToModeSelection() {
    inputSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    modeSelectionSection.classList.remove('hidden');
    
    // 입력 필드 초기화
    resetInputs();
    
    // 진행률 표시기 업데이트
    updateProgressIndicator('mode');
    
    // 포커스 설정
    setTimeout(() => {
        individualModeBtn.focus();
    }, 100);
}

// 입력 필드 초기화
function resetInputs() {
    document.getElementById('birth-date').value = '';
    participantsList.innerHTML = '';
    participantCountSelect.value = '2';
    clearErrorMessages();
    currentMode = null;
}

// 진행률 표시기 업데이트
function updateProgressIndicator(step) {
    // 기존 진행률 표시기 제거
    const existingProgress = document.querySelector('.progress-indicator');
    if (existingProgress) {
        existingProgress.remove();
    }
    
    // 새 진행률 표시기 생성
    const progressDiv = document.createElement('div');
    progressDiv.className = 'progress-indicator';
    
    const steps = [
        { key: 'mode', label: '모드 선택', icon: '🎯' },
        { key: 'input', label: '정보 입력', icon: '📝' },
        { key: 'results', label: '결과 확인', icon: '🔮' }
    ];
    
    const currentStepIndex = steps.findIndex(s => s.key === step);
    
    progressDiv.innerHTML = steps.map((stepInfo, index) => {
        const isActive = index === currentStepIndex;
        const isCompleted = index < currentStepIndex;
        const statusClass = isActive ? 'active' : (isCompleted ? 'completed' : 'pending');
        
        return `
            <div class="progress-step ${statusClass}">
                <div class="step-icon">${stepInfo.icon}</div>
                <div class="step-label">${stepInfo.label}</div>
            </div>
        `;
    }).join('');
    
    // 현재 활성 섹션에 진행률 표시기 추가
    const activeSection = document.querySelector('.section:not(.hidden)');
    if (activeSection) {
        activeSection.insertBefore(progressDiv, activeSection.firstChild);
    }
}

// 입력 완성도 체크 (개선된 버전)
function checkInputCompletion() {
    let isComplete = false;
    let completionPercentage = 0;
    
    if (currentMode === 'individual') {
        const birthDate = document.getElementById('birth-date').value;
        isComplete = birthDate && isValidBirthDate(birthDate) && isReasonableAge(birthDate);
        completionPercentage = isComplete ? 100 : (birthDate ? 50 : 0);
    } else {
        const count = parseInt(participantCountSelect.value);
        let validInputs = 0;
        
        for (let i = 1; i <= count; i++) {
            const birthDate = document.getElementById(`participant-${i}`).value;
            if (birthDate && isValidBirthDate(birthDate) && isReasonableAge(birthDate)) {
                validInputs++;
            }
        }
        
        isComplete = validInputs === count;
        completionPercentage = Math.round((validInputs / count) * 100);
    }
    
    // 버튼 상태 업데이트
    generateFortuneBtn.disabled = !isComplete;
    generateFortuneBtn.classList.toggle('disabled', !isComplete);
    
    // 진행률 표시 업데이트
    updateInputProgress(completionPercentage);
    
    // 완성도에 따른 피드백 제공
    provideFeedback(completionPercentage, isComplete);
    
    return isComplete;
}

// 입력 진행률 표시
function updateInputProgress(percentage) {
    let progressBar = document.querySelector('.input-progress');
    
    if (!progressBar) {
        progressBar = document.createElement('div');
        progressBar.className = 'input-progress';
        progressBar.innerHTML = `
            <div class="progress-label">입력 완성도: <span class="progress-percentage">0%</span></div>
            <div class="progress-track">
                <div class="progress-bar-fill" style="width: 0%"></div>
            </div>
        `;
        
        const inputContainer = document.querySelector('.input-container:not(.hidden)');
        if (inputContainer) {
            inputContainer.insertBefore(progressBar, inputContainer.firstChild);
        }
    }
    
    const percentageSpan = progressBar.querySelector('.progress-percentage');
    const progressFill = progressBar.querySelector('.progress-bar-fill');
    
    if (percentageSpan && progressFill) {
        percentageSpan.textContent = `${percentage}%`;
        progressFill.style.width = `${percentage}%`;
        
        // 색상 변경
        if (percentage === 100) {
            progressFill.style.backgroundColor = '#48bb78';
        } else if (percentage >= 50) {
            progressFill.style.backgroundColor = '#ed8936';
        } else {
            progressFill.style.backgroundColor = '#667eea';
        }
    }
}

// 사용자 피드백 제공
function provideFeedback(percentage, isComplete) {
    const existingFeedback = document.querySelector('.input-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    let feedbackMessage = '';
    let feedbackType = 'info';
    
    if (isComplete) {
        feedbackMessage = '✅ 모든 정보가 입력되었습니다. 운세를 확인해보세요!';
        feedbackType = 'success';
    } else if (percentage >= 50) {
        feedbackMessage = '⏳ 조금만 더 입력하시면 됩니다.';
        feedbackType = 'info';
    } else if (percentage > 0) {
        feedbackMessage = '📝 정보를 계속 입력해주세요.';
        feedbackType = 'info';
    }
    
    if (feedbackMessage) {
        const feedback = document.createElement('div');
        feedback.className = `input-feedback ${feedbackType}`;
        feedback.textContent = feedbackMessage;
        
        const inputContainer = document.querySelector('.input-container:not(.hidden)');
        if (inputContainer) {
            const progressBar = inputContainer.querySelector('.input-progress');
            if (progressBar) {
                progressBar.appendChild(feedback);
            }
        }
    }
}

// 도움말 툴팁 표시
function showTooltip(element, message) {
    // 기존 툴팁 제거
    const existingTooltip = document.querySelector('.tooltip');
    if (existingTooltip) {
        existingTooltip.remove();
    }
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = message;
    tooltip.setAttribute('role', 'tooltip');
    
    document.body.appendChild(tooltip);
    
    // 위치 계산
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.bottom + 10 + 'px';
    
    // 3초 후 자동 제거
    setTimeout(() => {
        if (tooltip.parentNode) {
            tooltip.remove();
        }
    }, 3000);
}

// 사용자 친화적 알림 표시 (개선된 버전)
function showNotification(message, type = 'info', duration = 5000) {
    // 기존 알림 제거
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.classList.remove('show');
        setTimeout(() => {
            if (existingNotification.parentNode) {
                existingNotification.remove();
            }
        }, 300);
    }
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', type === 'error' ? 'assertive' : 'polite');
    
    const icons = {
        error: '❌',
        warning: '⚠️',
        success: '✅',
        info: 'ℹ️',
        loading: '⏳'
    };
    
    const icon = icons[type] || icons.info;
    
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon" aria-hidden="true">${icon}</span>
            <span class="notification-message">${message}</span>
            <button class="notification-close" aria-label="알림 닫기" onclick="closeNotification(this)">×</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // 애니메이션 효과
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // 자동 제거 (에러가 아닌 경우)
    if (type !== 'error' && duration > 0) {
        setTimeout(() => {
            if (notification.parentNode) {
                notification.classList.remove('show');
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.remove();
                    }
                }, 300);
            }
        }, duration);
    }
    
    return notification;
}

// 알림 닫기 함수
function closeNotification(closeButton) {
    const notification = closeButton.closest('.notification');
    if (notification) {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }
}

// 에러 메시지 표시 (더 상세한 정보 포함)
function showErrorMessage(userMessage, technicalDetails = '') {
    const errorContainer = document.createElement('div');
    errorContainer.className = 'error-container';
    errorContainer.setAttribute('role', 'alert');
    errorContainer.setAttribute('aria-live', 'assertive');
    
    errorContainer.innerHTML = `
        <div class="error-content">
            <div class="error-icon" aria-hidden="true">😞</div>
            <div class="error-text">
                <h3>문제가 발생했습니다</h3>
                <p>${userMessage}</p>
                ${technicalDetails ? `<details><summary>기술적 세부사항</summary><p>${technicalDetails}</p></details>` : ''}
            </div>
            <div class="error-actions">
                <button class="btn primary" onclick="location.reload()">페이지 새로고침</button>
                <button class="btn secondary" onclick="this.closest('.error-container').remove(); goBackToModeSelection()">다시 시도</button>
            </div>
        </div>
    `;
    
    // 기존 에러 컨테이너 제거
    const existingError = document.querySelector('.error-container');
    if (existingError) {
        existingError.remove();
    }
    
    document.body.appendChild(errorContainer);
    
    // 애니메이션 효과
    setTimeout(() => {
        errorContainer.classList.add('show');
    }, 100);
}

// 운세 생성 함수
async function generateFortune() {
    // 입력 검증
    if (!validateInputs()) {
        return;
    }
    
    // 로딩 표시
    showLoading();
    
    try {
        // 입력 데이터 수집
        const inputData = collectInputData();
        
        // API 호출 (운세 생성) - 개발용 목업 데이터 사용
        let fortuneData, menuData;
        
        try {
            // 디버깅을 위한 로깅
            console.log('🔍 Fortune API 요청 시작');
            console.log('📤 전송 데이터:', JSON.stringify(inputData, null, 2));
            console.log('📤 API URL:', `${API_BASE_URL}/api/fortune`);
            
            const fortuneResponse = await fetch(`${API_BASE_URL}/api/fortune`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(inputData)
            });
            
            console.log('📥 Fortune API 응답 상태:', fortuneResponse.status);
            console.log('📥 Fortune API 응답 헤더:', Object.fromEntries(fortuneResponse.headers));
            
            if (!fortuneResponse.ok) {
                const errorText = await fortuneResponse.text();
                console.error('❌ Fortune API 오류:', errorText);
                throw new Error(`API 서버 오류 (${fortuneResponse.status}): ${errorText}`);
            }
            
            fortuneData = await fortuneResponse.json();
            console.log('✅ Fortune API 성공:', fortuneData);
            
            // 메뉴 추천을 위한 데이터 준비
            let menuRequestData = {
                mode: currentMode,
                fortune_data: {}
            };
            
            if (currentMode === 'individual') {
                // 개인 모드: individual_fortune 데이터 사용
                const individualFortune = fortuneData.individual_fortune;
                menuRequestData.fortune_data = {
                    individual_score: individualFortune.total_score,
                    categories: individualFortune.fortune,
                    date: fortuneData.date,
                    birth_date: individualFortune.birth_date
                };
            } else {
                // 그룹 모드: group_fortune 데이터 사용
                const groupFortune = fortuneData.group_fortune;
                menuRequestData.fortune_data = {
                    group_score: groupFortune.average_score,
                    harmony_score: groupFortune.harmony_score,
                    participant_count: groupFortune.participant_count,
                    dominant_categories: groupFortune.dominant_categories,
                    group_message: groupFortune.group_message,
                    individual_fortunes: fortuneData.individual_fortunes,
                    date: fortuneData.date
                };
            }
            
            // API 호출 (메뉴 추천)
            const menuResponse = await fetch(`${API_BASE_URL}/api/menu-recommendation`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(menuRequestData)
            });
            
            if (!menuResponse.ok) {
                throw new Error('메뉴 추천에 실패했습니다.');
            }
            
            menuData = await menuResponse.json();
            
        } catch (apiError) {
            console.log('API 서버를 사용할 수 없어 목업 데이터를 사용합니다:', apiError.message);
            
            // 사용자에게 알림 (너무 방해되지 않게)
            showNotification('서버 연결 중 문제가 발생하여 데모 데이터를 사용합니다.', 'warning');
            
            // 목업 데이터 사용
            fortuneData = generateMockFortuneData(inputData);
            menuData = generateMockMenuData(inputData);
        }
        
        // 결과 표시
        displayResults(fortuneData, menuData);
        
    } catch (error) {
        console.error('Error:', error);
        showErrorMessage('운세 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.', error.message);
        hideLoading();
    }
}

// 입력 검증 및 실시간 피드백
function validateInputs() {
    clearErrorMessages();
    let isValid = true;
    
    if (currentMode === 'individual') {
        const birthDate = document.getElementById('birth-date').value;
        const birthDateInput = document.getElementById('birth-date');
        
        if (!birthDate) {
            showFieldError(birthDateInput, '생년월일을 입력해주세요.');
            isValid = false;
        } else if (!isValidBirthDate(birthDate)) {
            showFieldError(birthDateInput, '올바른 생년월일을 입력해주세요. (미래 날짜는 불가능합니다)');
            isValid = false;
        } else if (!isReasonableAge(birthDate)) {
            showFieldError(birthDateInput, '생년월일을 다시 확인해주세요. (1900년 이후 날짜를 입력해주세요)');
            isValid = false;
        }
    } else {
        const count = parseInt(participantCountSelect.value);
        for (let i = 1; i <= count; i++) {
            const birthDateInput = document.getElementById(`participant-${i}`);
            const birthDate = birthDateInput.value;
            
            if (!birthDate) {
                showFieldError(birthDateInput, `참석자 ${i}의 생년월일을 입력해주세요.`);
                isValid = false;
            } else if (!isValidBirthDate(birthDate)) {
                showFieldError(birthDateInput, `올바른 생년월일을 입력해주세요. (미래 날짜는 불가능합니다)`);
                isValid = false;
            } else if (!isReasonableAge(birthDate)) {
                showFieldError(birthDateInput, `생년월일을 다시 확인해주세요. (1900년 이후 날짜를 입력해주세요)`);
                isValid = false;
            }
        }
    }
    
    return isValid;
}

// 생년월일 유효성 검사 헬퍼 함수들
function isValidBirthDate(dateString) {
    const birthDate = new Date(dateString);
    const today = new Date();
    return birthDate <= today;
}

function isReasonableAge(dateString) {
    const birthDate = new Date(dateString);
    const minDate = new Date('1900-01-01');
    return birthDate >= minDate;
}

// 필드별 에러 메시지 표시
function showFieldError(inputElement, message) {
    // 기존 에러 메시지 제거
    const existingError = inputElement.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // 에러 스타일 적용
    inputElement.classList.add('error');
    
    // 에러 메시지 생성
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.setAttribute('role', 'alert');
    errorDiv.setAttribute('aria-live', 'polite');
    
    // 에러 메시지 삽입
    inputElement.parentNode.appendChild(errorDiv);
}

// 모든 에러 메시지 제거
function clearErrorMessages() {
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(error => error.remove());
    
    const errorInputs = document.querySelectorAll('.error');
    errorInputs.forEach(input => input.classList.remove('error'));
}

// 입력 데이터 수집
function collectInputData() {
    const data = {
        mode: currentMode,
        participants: []
    };
    
    if (currentMode === 'individual') {
        const birthDate = document.getElementById('birth-date').value;
        data.participants.push({
            birth_date: birthDate,
            name: '사용자'
        });
    } else {
        const count = parseInt(participantCountSelect.value);
        for (let i = 1; i <= count; i++) {
            const birthDate = document.getElementById(`participant-${i}`).value;
            data.participants.push({
                birth_date: birthDate,
                name: `참석자 ${i}`
            });
        }
    }
    
    return data;
}

// 로딩 표시 (개선된 버전)
function showLoading() {
    inputSection.classList.add('hidden');
    loadingSection.classList.remove('hidden');
    
    // 로딩 메시지 랜덤화
    const loadingMessages = [
        '운세를 생성하고 있습니다...',
        '별자리를 확인하고 있습니다...',
        '오늘의 기운을 분석하고 있습니다...',
        '최적의 메뉴를 찾고 있습니다...',
        '운명의 실을 엮고 있습니다...'
    ];
    
    const randomMessage = loadingMessages[Math.floor(Math.random() * loadingMessages.length)];
    const loadingText = document.querySelector('#loading-section p');
    if (loadingText) {
        loadingText.textContent = randomMessage;
    }
    
    // 로딩 타임아웃 설정 (30초)
    const loadingTimeout = setTimeout(() => {
        hideLoading();
        showErrorMessage(
            '서버 응답이 지연되고 있습니다. 잠시 후 다시 시도해주세요.',
            '요청 시간이 30초를 초과했습니다.'
        );
    }, 30000);
    
    // 타임아웃 ID를 전역 변수에 저장
    window.currentLoadingTimeout = loadingTimeout;
}

// 로딩 숨기기 (개선된 버전)
function hideLoading() {
    loadingSection.classList.add('hidden');
    
    // 로딩 타임아웃 클리어
    if (window.currentLoadingTimeout) {
        clearTimeout(window.currentLoadingTimeout);
        window.currentLoadingTimeout = null;
    }
}

// 결과 표시
function displayResults(fortuneData, menuData) {
    hideLoading();
    
    // 진행률 표시기 업데이트
    updateProgressIndicator('results');
    
    // 운세 결과 표시
    displayFortuneResults(fortuneData);
    
    // 메뉴 추천 결과 표시
    displayMenuRecommendations(menuData);
    
    // 결과 섹션 표시
    resultsSection.classList.remove('hidden');
    
    // 포커스 설정
    setTimeout(() => {
        shareBtn.focus();
    }, 100);
}

// 운세 결과 표시 함수
function displayFortuneResults(fortuneData) {
    const fortuneResults = document.getElementById('fortune-results');
    
    if (currentMode === 'individual') {
        fortuneResults.innerHTML = createIndividualFortuneHTML(fortuneData);
    } else {
        fortuneResults.innerHTML = createGroupFortuneHTML(fortuneData);
    }
    
    // 애니메이션 효과 적용
    animateFortuneCards();
}

// 개인 운세 HTML 생성
function createIndividualFortuneHTML(fortuneData) {
    // 임시 데이터 구조 (실제 API 응답에 맞게 수정 필요)
    const mockFortune = {
        total_score: 78,
        categories: {
            love: { score: 85, message: "오늘은 사랑에 행운이 따를 것입니다. 새로운 만남이나 기존 관계의 발전이 기대됩니다." },
            health: { score: 72, message: "건강에 주의하세요. 충분한 휴식과 균형 잡힌 식사가 중요합니다." },
            wealth: { score: 90, message: "재물운이 상승하고 있습니다. 투자나 사업에 좋은 기회가 올 수 있습니다." },
            career: { score: 65, message: "직장에서 인내심이 필요한 시기입니다. 꾸준한 노력이 결실을 맺을 것입니다." }
        }
    };
    
    const categoryNames = {
        love: { name: '사랑운', icon: '💕', color: '#ff6b9d' },
        health: { name: '건강운', icon: '🌿', color: '#51cf66' },
        wealth: { name: '재물운', icon: '💰', color: '#ffd43b' },
        career: { name: '학업/직장운', icon: '📚', color: '#74c0fc' }
    };
    
    return `
        <div class="fortune-container">
            <div class="fortune-header">
                <h3>🔮 오늘의 운세</h3>
                <div class="total-score">
                    <div class="score-circle" role="img" aria-label="총 운세 점수 ${mockFortune.total_score}점">
                        <div class="score-value">${mockFortune.total_score}</div>
                        <div class="score-label">점</div>
                    </div>
                    <div class="score-description">
                        ${getScoreDescription(mockFortune.total_score)}
                    </div>
                </div>
            </div>
            
            <div class="fortune-categories" role="list" aria-label="운세 카테고리별 결과">
                ${Object.entries(mockFortune.categories).map(([key, category]) => {
                    const categoryInfo = categoryNames[key];
                    return `
                        <div class="fortune-card" data-category="${key}" role="listitem">
                            <div class="card-header">
                                <span class="category-icon" aria-hidden="true">${categoryInfo.icon}</span>
                                <span class="category-name">${categoryInfo.name}</span>
                                <div class="category-score" 
                                     style="background-color: ${categoryInfo.color}"
                                     aria-label="${categoryInfo.name} ${category.score}점">
                                    ${category.score}점
                                </div>
                            </div>
                            <div class="progress-bar" role="progressbar" 
                                 aria-valuenow="${category.score}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100"
                                 aria-label="${categoryInfo.name} 점수 진행률">
                                <div class="progress-fill" 
                                     style="width: ${category.score}%; background-color: ${categoryInfo.color}">
                                </div>
                            </div>
                            <div class="category-message">
                                ${category.message}
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
    `;
}

// 그룹 운세 HTML 생성
function createGroupFortuneHTML(fortuneData) {
    // 임시 데이터 구조 (실제 API 응답에 맞게 수정 필요)
    const mockGroupFortune = {
        group_fortune: {
            average_score: 75,
            harmony_score: 82,
            dominant_categories: ['love', 'wealth'],
            group_message: "오늘 모임은 화합과 즐거움이 가득할 것입니다"
        },
        individual_fortunes: [
            {
                name: "참석자 1",
                total_score: 78,
                categories: {
                    love: { score: 85, message: "사랑운이 좋습니다" },
                    health: { score: 72, message: "건강에 주의하세요" },
                    wealth: { score: 90, message: "재물운 상승" },
                    career: { score: 65, message: "꾸준한 노력 필요" }
                }
            },
            {
                name: "참석자 2",
                total_score: 72,
                categories: {
                    love: { score: 68, message: "평범한 사랑운" },
                    health: { score: 80, message: "건강 상태 양호" },
                    wealth: { score: 75, message: "안정적인 재물운" },
                    career: { score: 65, message: "새로운 기회 모색" }
                }
            }
        ]
    };
    
    const categoryNames = {
        love: { name: '사랑운', icon: '💕', color: '#ff6b9d' },
        health: { name: '건강운', icon: '🌿', color: '#51cf66' },
        wealth: { name: '재물운', icon: '💰', color: '#ffd43b' },
        career: { name: '학업/직장운', icon: '📚', color: '#74c0fc' }
    };
    
    return `
        <div class="fortune-container group-fortune">
            <!-- 그룹 종합 운세 -->
            <div class="group-summary" role="region" aria-label="그룹 종합 운세">
                <h3>👥 그룹 종합 운세</h3>
                <div class="group-scores">
                    <div class="group-score-item">
                        <div class="score-circle small" role="img" aria-label="그룹 평균 점수 ${mockGroupFortune.group_fortune.average_score}점">
                            <div class="score-value">${mockGroupFortune.group_fortune.average_score}</div>
                            <div class="score-label">평균</div>
                        </div>
                    </div>
                    <div class="group-score-item">
                        <div class="score-circle small harmony" role="img" aria-label="그룹 화합 점수 ${mockGroupFortune.group_fortune.harmony_score}점">
                            <div class="score-value">${mockGroupFortune.group_fortune.harmony_score}</div>
                            <div class="score-label">화합</div>
                        </div>
                    </div>
                </div>
                <div class="group-message">
                    ${mockGroupFortune.group_fortune.group_message}
                </div>
                <div class="dominant-categories" role="list" aria-label="주요 운세 카테고리">
                    <span class="label">주요 운세:</span>
                    ${mockGroupFortune.group_fortune.dominant_categories.map(cat => 
                        `<span class="category-tag" 
                               style="background-color: ${categoryNames[cat].color}"
                               role="listitem"
                               aria-label="${categoryNames[cat].name}">
                            <span aria-hidden="true">${categoryNames[cat].icon}</span> ${categoryNames[cat].name}
                        </span>`
                    ).join('')}
                </div>
            </div>
            
            <!-- 개별 참석자 운세 -->
            <div class="individual-fortunes" role="region" aria-label="개별 참석자 운세">
                <h4>📊 개별 참석자 운세</h4>
                <div class="participants-grid" role="list" aria-label="참석자별 운세 목록">
                    ${mockGroupFortune.individual_fortunes.map((participant, index) => `
                        <div class="participant-fortune" data-participant="${index}" role="listitem">
                            <div class="participant-header">
                                <span class="participant-name">${participant.name}</span>
                                <div class="participant-score" aria-label="${participant.name} 총 점수 ${participant.total_score}점">
                                    ${participant.total_score}점
                                </div>
                            </div>
                            <div class="participant-categories" role="list" aria-label="${participant.name}의 카테고리별 점수">
                                ${Object.entries(participant.categories).map(([key, category]) => {
                                    const categoryInfo = categoryNames[key];
                                    return `
                                        <div class="mini-category" role="listitem">
                                            <span class="mini-icon" aria-hidden="true">${categoryInfo.icon}</span>
                                            <div class="mini-progress" 
                                                 role="progressbar" 
                                                 aria-valuenow="${category.score}" 
                                                 aria-valuemin="0" 
                                                 aria-valuemax="100"
                                                 aria-label="${categoryInfo.name} ${category.score}점">
                                                <div class="mini-fill" 
                                                     style="width: ${category.score}%; background-color: ${categoryInfo.color}">
                                                </div>
                                            </div>
                                            <span class="mini-score" aria-label="${category.score}점">${category.score}</span>
                                        </div>
                                    `;
                                }).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
}

// 점수 설명 생성
function getScoreDescription(score) {
    if (score >= 90) return "🌟 최고의 운세! 모든 일이 순조롭게 풀릴 것입니다.";
    if (score >= 80) return "✨ 매우 좋은 운세! 긍정적인 에너지가 가득합니다.";
    if (score >= 70) return "😊 좋은 운세! 대체로 순조로운 하루가 될 것입니다.";
    if (score >= 60) return "🙂 평범한 운세. 꾸준한 노력이 좋은 결과를 가져올 것입니다.";
    if (score >= 50) return "😐 보통 운세. 신중한 판단이 필요한 시기입니다.";
    return "🤔 주의가 필요한 운세. 차분하게 행동하는 것이 좋겠습니다.";
}

// 운세 카드 애니메이션
function animateFortuneCards() {
    const cards = document.querySelectorAll('.fortune-card, .participant-fortune');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // 프로그레스 바 애니메이션
    setTimeout(() => {
        const progressBars = document.querySelectorAll('.progress-fill, .mini-fill');
        progressBars.forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.transition = 'width 1s ease-out';
                bar.style.width = width;
            }, 100);
        });
    }, 500);
    
    // 운세 카드 클릭 이벤트 추가
    addFortuneCardInteractions();
}

// 운세 카드 상호작용 추가
function addFortuneCardInteractions() {
    const fortuneCards = document.querySelectorAll('.fortune-card');
    fortuneCards.forEach(card => {
        card.addEventListener('click', () => {
            const category = card.dataset.category;
            showCategoryDetail(category);
        });
        
        // 키보드 접근성
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', '클릭하여 상세 정보 보기');
        
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const category = card.dataset.category;
                showCategoryDetail(category);
            }
        });
    });
    
    // 참석자 카드 클릭 이벤트
    const participantCards = document.querySelectorAll('.participant-fortune');
    participantCards.forEach(card => {
        card.addEventListener('click', () => {
            const participantIndex = card.dataset.participant;
            showParticipantDetail(participantIndex);
        });
        
        // 키보드 접근성
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', '클릭하여 상세 정보 보기');
        
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const participantIndex = card.dataset.participant;
                showParticipantDetail(participantIndex);
            }
        });
    });
}

// 카테고리 상세 정보 표시
function showCategoryDetail(category) {
    const categoryNames = {
        love: { name: '사랑운', icon: '💕', color: '#ff6b9d' },
        health: { name: '건강운', icon: '🌿', color: '#51cf66' },
        wealth: { name: '재물운', icon: '💰', color: '#ffd43b' },
        career: { name: '학업/직장운', icon: '📚', color: '#74c0fc' }
    };
    
    const categoryInfo = categoryNames[category];
    const detailMessages = {
        love: "오늘은 사랑에 행운이 따를 것입니다. 새로운 만남이나 기존 관계의 발전이 기대됩니다. 진솔한 마음으로 상대방에게 다가가보세요.",
        health: "건강에 주의하세요. 충분한 휴식과 균형 잡힌 식사가 중요합니다. 가벼운 운동으로 몸과 마음을 건강하게 유지하세요.",
        wealth: "재물운이 상승하고 있습니다. 투자나 사업에 좋은 기회가 올 수 있습니다. 하지만 신중한 판단을 잊지 마세요.",
        career: "직장에서 인내심이 필요한 시기입니다. 꾸준한 노력이 결실을 맺을 것입니다. 동료들과의 협력이 중요합니다."
    };
    
    showModal(`
        <div class="category-detail-modal">
            <div class="modal-header" style="background-color: ${categoryInfo.color}">
                <span class="modal-icon">${categoryInfo.icon}</span>
                <h3>${categoryInfo.name} 상세</h3>
            </div>
            <div class="modal-content">
                <p>${detailMessages[category]}</p>
                <div class="detail-tips">
                    <h4>💡 오늘의 팁</h4>
                    <ul>
                        ${getCategoryTips(category).map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `);
}

// 참석자 상세 정보 표시
function showParticipantDetail(participantIndex) {
    // 임시 데이터 - 실제로는 저장된 데이터에서 가져와야 함
    const participant = {
        name: `참석자 ${parseInt(participantIndex) + 1}`,
        total_score: 78,
        categories: {
            love: { score: 85, message: "사랑운이 좋습니다" },
            health: { score: 72, message: "건강에 주의하세요" },
            wealth: { score: 90, message: "재물운 상승" },
            career: { score: 65, message: "꾸준한 노력 필요" }
        }
    };
    
    const categoryNames = {
        love: { name: '사랑운', icon: '💕', color: '#ff6b9d' },
        health: { name: '건강운', icon: '🌿', color: '#51cf66' },
        wealth: { name: '재물운', icon: '💰', color: '#ffd43b' },
        career: { name: '학업/직장운', icon: '📚', color: '#74c0fc' }
    };
    
    showModal(`
        <div class="participant-detail-modal">
            <div class="modal-header">
                <h3>👤 ${participant.name} 상세 운세</h3>
                <div class="total-score-small">총 ${participant.total_score}점</div>
            </div>
            <div class="modal-content">
                <div class="detailed-categories">
                    ${Object.entries(participant.categories).map(([key, category]) => {
                        const categoryInfo = categoryNames[key];
                        return `
                            <div class="detailed-category">
                                <div class="category-header">
                                    <span class="category-icon">${categoryInfo.icon}</span>
                                    <span class="category-name">${categoryInfo.name}</span>
                                    <span class="category-score" style="background-color: ${categoryInfo.color}">
                                        ${category.score}점
                                    </span>
                                </div>
                                <p class="category-message">${category.message}</p>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        </div>
    `);
}

// 카테고리별 팁 생성
function getCategoryTips(category) {
    const tips = {
        love: [
            "진솔한 대화를 나누어보세요",
            "상대방의 말에 귀 기울여주세요",
            "작은 선물이나 관심 표현을 해보세요"
        ],
        health: [
            "충분한 수분 섭취를 하세요",
            "규칙적인 수면 패턴을 유지하세요",
            "스트레칭으로 몸을 풀어주세요"
        ],
        wealth: [
            "가계부를 작성해보세요",
            "불필요한 지출을 줄여보세요",
            "투자 전 충분한 정보를 수집하세요"
        ],
        career: [
            "목표를 명확히 설정하세요",
            "새로운 기술을 배워보세요",
            "네트워킹을 활용해보세요"
        ]
    };
    
    return tips[category] || [];
}

// 모달 표시 함수
function showModal(content) {
    // 기존 모달 제거
    const existingModal = document.querySelector('.modal-overlay');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modalOverlay = document.createElement('div');
    modalOverlay.className = 'modal-overlay';
    modalOverlay.innerHTML = `
        <div class="modal-container" role="dialog" aria-modal="true" aria-labelledby="modal-title">
            <button class="modal-close" aria-label="모달 닫기">&times;</button>
            ${content}
        </div>
    `;
    
    document.body.appendChild(modalOverlay);
    
    // 모달 닫기 이벤트
    const closeBtn = modalOverlay.querySelector('.modal-close');
    closeBtn.addEventListener('click', () => modalOverlay.remove());
    
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.remove();
        }
    });
    
    // ESC 키로 모달 닫기
    const handleEscape = (e) => {
        if (e.key === 'Escape') {
            modalOverlay.remove();
            document.removeEventListener('keydown', handleEscape);
        }
    };
    document.addEventListener('keydown', handleEscape);
    
    // 포커스 관리
    setTimeout(() => {
        closeBtn.focus();
    }, 100);
}

// 메뉴 추천 표시 함수
function displayMenuRecommendations(menuData) {
    const menuResults = document.getElementById('menu-results');
    
    if (currentMode === 'individual') {
        menuResults.innerHTML = createIndividualMenuHTML();
    } else {
        menuResults.innerHTML = createGroupMenuHTML();
    }
    
    // 메뉴 카드 애니메이션 및 상호작용 추가
    animateMenuCards();
}

// 개인 모드 메뉴 추천 HTML 생성
function createIndividualMenuHTML() {
    // 임시 데이터 구조 (실제 API 응답에 맞게 수정 필요)
    const mockMenuRecommendations = [
        {
            id: 1,
            name: "김치찌개",
            reason: "오늘의 건강운이 좋아 따뜻한 국물 요리가 몸에 좋을 것입니다",
            category: "한식",
            ingredients: ["김치", "돼지고기", "두부", "대파", "고춧가루"],
            cooking_time: "30분",
            difficulty: "쉬움",
            serving_size: "1-2인분",
            image: "🍲",
            nutrition: {
                calories: "320kcal",
                protein: "18g",
                carbs: "25g",
                fat: "15g"
            },
            recipe_steps: [
                "김치를 적당한 크기로 썰어주세요",
                "팬에 기름을 두르고 김치를 볶아주세요",
                "물을 넣고 끓인 후 돼지고기를 넣어주세요",
                "두부와 대파를 넣고 5분간 더 끓여주세요"
            ]
        },
        {
            id: 2,
            name: "연어 샐러드",
            reason: "재물운이 상승하는 날, 고급스러운 연어로 운을 더욱 높여보세요",
            category: "양식",
            ingredients: ["연어", "아보카도", "방울토마토", "양상추", "올리브오일"],
            cooking_time: "15분",
            difficulty: "쉬움",
            serving_size: "1인분",
            image: "🥗",
            nutrition: {
                calories: "280kcal",
                protein: "25g",
                carbs: "12g",
                fat: "16g"
            },
            recipe_steps: [
                "연어를 팬에 구워주세요",
                "야채들을 깨끗이 씻어 준비해주세요",
                "아보카도를 슬라이스해주세요",
                "모든 재료를 섞고 드레싱을 뿌려주세요"
            ]
        },
        {
            id: 3,
            name: "치킨 카레",
            reason: "사랑운이 좋은 날, 향신료가 풍부한 카레로 매력을 발산해보세요",
            category: "아시안",
            ingredients: ["닭가슴살", "양파", "당근", "감자", "카레가루", "코코넛밀크"],
            cooking_time: "45분",
            difficulty: "보통",
            serving_size: "2-3인분",
            image: "🍛",
            nutrition: {
                calories: "380kcal",
                protein: "28g",
                carbs: "35g",
                fat: "14g"
            },
            recipe_steps: [
                "닭가슴살을 한입 크기로 썰어주세요",
                "야채들을 적당한 크기로 썰어주세요",
                "팬에 닭고기를 볶은 후 야채를 넣어주세요",
                "카레가루와 코코넛밀크를 넣고 끓여주세요"
            ]
        }
    ];
    
    return `
        <div class="menu-container">
            <div class="menu-header">
                <h3>🍽️ 오늘의 추천 메뉴</h3>
                <p class="menu-subtitle">당신의 운세에 맞는 완벽한 식사를 준비했습니다</p>
            </div>
            
            <div class="menu-grid">
                ${mockMenuRecommendations.map((menu, index) => `
                    <div class="menu-card" data-menu-id="${menu.id}" role="article">
                        <div class="menu-image">
                            <span class="menu-emoji">${menu.image}</span>
                            <div class="menu-badge">${menu.category}</div>
                        </div>
                        
                        <div class="menu-content">
                            <h4 class="menu-name">${menu.name}</h4>
                            <p class="menu-reason">${menu.reason}</p>
                            
                            <div class="menu-info">
                                <div class="info-item">
                                    <span class="info-icon">⏱️</span>
                                    <span class="info-text">${menu.cooking_time}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-icon">👨‍🍳</span>
                                    <span class="info-text">${menu.difficulty}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-icon">🍽️</span>
                                    <span class="info-text">${menu.serving_size}</span>
                                </div>
                            </div>
                            
                            <div class="menu-ingredients">
                                <span class="ingredients-label">주요 재료:</span>
                                <div class="ingredients-list">
                                    ${menu.ingredients.slice(0, 3).map(ingredient => 
                                        `<span class="ingredient-tag">${ingredient}</span>`
                                    ).join('')}
                                    ${menu.ingredients.length > 3 ? 
                                        `<span class="ingredient-more">+${menu.ingredients.length - 3}</span>` : ''
                                    }
                                </div>
                            </div>
                            
                            <button class="menu-detail-btn" data-menu-id="${menu.id}" aria-label="${menu.name} 상세 정보 보기">
                                상세 보기
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// 그룹 모드 메뉴 추천 HTML 생성
function createGroupMenuHTML() {
    // 임시 데이터 구조 (실제 API 응답에 맞게 수정 필요)
    const mockGroupMenuRecommendations = [
        {
            id: 1,
            name: "삼겹살 BBQ 파티",
            reason: "그룹의 화합 운세가 높아 함께 구워먹는 음식이 최고입니다",
            category: "한식",
            ingredients: ["삼겹살", "상추", "마늘", "된장찌개", "김치", "쌈장"],
            cooking_time: "45분",
            difficulty: "쉬움",
            serving_size: "4-6인분",
            image: "🥓",
            group_benefit: "모든 참석자가 함께 참여할 수 있는 요리",
            sharing_type: "공유형",
            nutrition: {
                calories: "450kcal",
                protein: "32g",
                carbs: "15g",
                fat: "28g"
            },
            group_tips: [
                "각자 좋아하는 쌈 채소를 준비해보세요",
                "다양한 소스로 취향에 맞게 즐겨보세요",
                "함께 굽는 재미로 대화가 더욱 활발해집니다"
            ]
        },
        {
            id: 2,
            name: "해물 파전 & 막걸리",
            reason: "그룹의 주요 운세가 사랑운이라 정겨운 음식이 좋습니다",
            category: "한식",
            ingredients: ["해물믹스", "파", "부침가루", "계란", "막걸리"],
            cooking_time: "30분",
            difficulty: "보통",
            serving_size: "3-5인분",
            image: "🥞",
            group_benefit: "비오는 날 분위기에 완벽한 조합",
            sharing_type: "공유형",
            nutrition: {
                calories: "320kcal",
                protein: "18g",
                carbs: "35g",
                fat: "12g"
            },
            group_tips: [
                "바삭하게 부쳐서 나누어 드세요",
                "막걸리와 함께하면 더욱 맛있습니다",
                "각자 좋아하는 해물을 추가해보세요"
            ]
        },
        {
            id: 3,
            name: "치킨 & 피자 콤보",
            reason: "그룹 평균 점수가 높아 축하할 만한 특별한 메뉴를 준비했습니다",
            category: "양식",
            ingredients: ["치킨", "피자", "콜라", "치킨무", "피클"],
            cooking_time: "배달 30분",
            difficulty: "주문",
            serving_size: "4-8인분",
            image: "🍕",
            group_benefit: "준비 없이 간편하게 즐길 수 있는 파티 메뉴",
            sharing_type: "공유형",
            nutrition: {
                calories: "520kcal",
                protein: "28g",
                carbs: "45g",
                fat: "25g"
            },
            group_tips: [
                "다양한 피자 토핑으로 취향을 맞춰보세요",
                "치킨은 순한맛과 매운맛을 섞어 주문하세요",
                "게임이나 영화와 함께 즐기면 더욱 좋습니다"
            ]
        }
    ];
    
    return `
        <div class="menu-container group-menu">
            <div class="menu-header">
                <h3>🍽️ 그룹 추천 메뉴</h3>
                <p class="menu-subtitle">모든 참석자가 만족할 수 있는 완벽한 메뉴를 선별했습니다</p>
                <div class="group-menu-info">
                    <span class="group-info-badge">👥 ${participantCountSelect.value}명 기준</span>
                    <span class="group-info-badge">🤝 화합 중심</span>
                </div>
            </div>
            
            <div class="menu-grid group-grid">
                ${mockGroupMenuRecommendations.map((menu, index) => `
                    <div class="menu-card group-menu-card" data-menu-id="${menu.id}" role="article">
                        <div class="menu-image">
                            <span class="menu-emoji">${menu.image}</span>
                            <div class="menu-badge">${menu.category}</div>
                            <div class="sharing-badge">${menu.sharing_type}</div>
                        </div>
                        
                        <div class="menu-content">
                            <h4 class="menu-name">${menu.name}</h4>
                            <p class="menu-reason">${menu.reason}</p>
                            
                            <div class="group-benefit">
                                <span class="benefit-icon">✨</span>
                                <span class="benefit-text">${menu.group_benefit}</span>
                            </div>
                            
                            <div class="menu-info">
                                <div class="info-item">
                                    <span class="info-icon">⏱️</span>
                                    <span class="info-text">${menu.cooking_time}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-icon">👨‍🍳</span>
                                    <span class="info-text">${menu.difficulty}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-icon">🍽️</span>
                                    <span class="info-text">${menu.serving_size}</span>
                                </div>
                            </div>
                            
                            <div class="menu-ingredients">
                                <span class="ingredients-label">포함 구성:</span>
                                <div class="ingredients-list">
                                    ${menu.ingredients.slice(0, 3).map(ingredient => 
                                        `<span class="ingredient-tag">${ingredient}</span>`
                                    ).join('')}
                                    ${menu.ingredients.length > 3 ? 
                                        `<span class="ingredient-more">+${menu.ingredients.length - 3}</span>` : ''
                                    }
                                </div>
                            </div>
                            
                            <button class="menu-detail-btn group-detail-btn" data-menu-id="${menu.id}" aria-label="${menu.name} 상세 정보 보기">
                                그룹 메뉴 상세
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// 메뉴 카드 애니메이션 및 상호작용
function animateMenuCards() {
    const menuCards = document.querySelectorAll('.menu-card');
    menuCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 150);
    });
    
    // 메뉴 카드 상호작용 추가
    addMenuCardInteractions();
}

// 메뉴 카드 상호작용 추가
function addMenuCardInteractions() {
    const detailButtons = document.querySelectorAll('.menu-detail-btn');
    detailButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const menuId = button.dataset.menuId;
            showMenuDetail(menuId);
        });
    });
    
    // 메뉴 카드 클릭 이벤트
    const menuCards = document.querySelectorAll('.menu-card');
    menuCards.forEach(card => {
        card.addEventListener('click', () => {
            const menuId = card.dataset.menuId;
            showMenuDetail(menuId);
        });
        
        // 키보드 접근성
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', '클릭하여 메뉴 상세 정보 보기');
        
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const menuId = card.dataset.menuId;
                showMenuDetail(menuId);
            }
        });
    });
}

// 메뉴 상세 정보 표시
function showMenuDetail(menuId) {
    // 임시 데이터 - 실제로는 저장된 데이터에서 가져와야 함
    const menuData = getMenuData(menuId);
    
    if (currentMode === 'individual') {
        showIndividualMenuDetail(menuData);
    } else {
        showGroupMenuDetail(menuData);
    }
}

// 개인 모드 메뉴 상세 정보
function showIndividualMenuDetail(menu) {
    showModal(`
        <div class="menu-detail-modal">
            <div class="modal-header" style="background: linear-gradient(135deg, #ff6b9d 0%, #ff8a80 100%)">
                <span class="modal-icon">${menu.image}</span>
                <h3>${menu.name}</h3>
                <div class="menu-category-badge">${menu.category}</div>
            </div>
            <div class="modal-content">
                <div class="menu-reason-box">
                    <h4>🔮 추천 이유</h4>
                    <p>${menu.reason}</p>
                </div>
                
                <div class="menu-details-grid">
                    <div class="detail-section">
                        <h4>📋 재료 목록</h4>
                        <div class="ingredients-grid">
                            ${menu.ingredients.map(ingredient => 
                                `<span class="ingredient-item">${ingredient}</span>`
                            ).join('')}
                        </div>
                    </div>
                    
                    <div class="detail-section">
                        <h4>📊 영양 정보</h4>
                        <div class="nutrition-info">
                            <div class="nutrition-item">
                                <span class="nutrition-label">칼로리</span>
                                <span class="nutrition-value">${menu.nutrition.calories}</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">단백질</span>
                                <span class="nutrition-value">${menu.nutrition.protein}</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">탄수화물</span>
                                <span class="nutrition-value">${menu.nutrition.carbs}</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">지방</span>
                                <span class="nutrition-value">${menu.nutrition.fat}</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="recipe-section">
                    <h4>👨‍🍳 간단 레시피</h4>
                    <ol class="recipe-steps">
                        ${menu.recipe_steps.map(step => 
                            `<li class="recipe-step">${step}</li>`
                        ).join('')}
                    </ol>
                </div>
            </div>
        </div>
    `);
}

// 그룹 모드 메뉴 상세 정보
function showGroupMenuDetail(menu) {
    showModal(`
        <div class="menu-detail-modal group-detail">
            <div class="modal-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
                <span class="modal-icon">${menu.image}</span>
                <h3>${menu.name}</h3>
                <div class="menu-badges">
                    <span class="menu-category-badge">${menu.category}</span>
                    <span class="sharing-type-badge">${menu.sharing_type}</span>
                </div>
            </div>
            <div class="modal-content">
                <div class="menu-reason-box">
                    <h4>🔮 그룹 추천 이유</h4>
                    <p>${menu.reason}</p>
                </div>
                
                <div class="group-benefit-box">
                    <h4>✨ 그룹 혜택</h4>
                    <p>${menu.group_benefit}</p>
                </div>
                
                <div class="menu-details-grid">
                    <div class="detail-section">
                        <h4>📋 구성 요소</h4>
                        <div class="ingredients-grid">
                            ${menu.ingredients.map(ingredient => 
                                `<span class="ingredient-item">${ingredient}</span>`
                            ).join('')}
                        </div>
                    </div>
                    
                    <div class="detail-section">
                        <h4>📊 1인분 영양 정보</h4>
                        <div class="nutrition-info">
                            <div class="nutrition-item">
                                <span class="nutrition-label">칼로리</span>
                                <span class="nutrition-value">${menu.nutrition.calories}</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">단백질</span>
                                <span class="nutrition-value">${menu.nutrition.protein}</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">탄수화물</span>
                                <span class="nutrition-value">${menu.nutrition.carbs}</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">지방</span>
                                <span class="nutrition-value">${menu.nutrition.fat}</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="group-tips-section">
                    <h4>💡 그룹 활용 팁</h4>
                    <ul class="group-tips-list">
                        ${menu.group_tips.map(tip => 
                            `<li class="group-tip">${tip}</li>`
                        ).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `);
}

// 메뉴 데이터 가져오기 (임시 함수)
function getMenuData(menuId) {
    const allMenus = [
        // 개인 모드 메뉴들
        {
            id: 1,
            name: "김치찌개",
            reason: "오늘의 건강운이 좋아 따뜻한 국물 요리가 몸에 좋을 것입니다",
            category: "한식",
            ingredients: ["김치", "돼지고기", "두부", "대파", "고춧가루"],
            cooking_time: "30분",
            difficulty: "쉬움",
            serving_size: "1-2인분",
            image: "🍲",
            nutrition: {
                calories: "320kcal",
                protein: "18g",
                carbs: "25g",
                fat: "15g"
            },
            recipe_steps: [
                "김치를 적당한 크기로 썰어주세요",
                "팬에 기름을 두르고 김치를 볶아주세요",
                "물을 넣고 끓인 후 돼지고기를 넣어주세요",
                "두부와 대파를 넣고 5분간 더 끓여주세요"
            ]
        },
        {
            id: 2,
            name: "연어 샐러드",
            reason: "재물운이 상승하는 날, 고급스러운 연어로 운을 더욱 높여보세요",
            category: "양식",
            ingredients: ["연어", "아보카도", "방울토마토", "양상추", "올리브오일"],
            cooking_time: "15분",
            difficulty: "쉬움",
            serving_size: "1인분",
            image: "🥗",
            nutrition: {
                calories: "280kcal",
                protein: "25g",
                carbs: "12g",
                fat: "16g"
            },
            recipe_steps: [
                "연어를 팬에 구워주세요",
                "야채들을 깨끗이 씻어 준비해주세요",
                "아보카도를 슬라이스해주세요",
                "모든 재료를 섞고 드레싱을 뿌려주세요"
            ]
        },
        {
            id: 3,
            name: "치킨 카레",
            reason: "사랑운이 좋은 날, 향신료가 풍부한 카레로 매력을 발산해보세요",
            category: "아시안",
            ingredients: ["닭가슴살", "양파", "당근", "감자", "카레가루", "코코넛밀크"],
            cooking_time: "45분",
            difficulty: "보통",
            serving_size: "2-3인분",
            image: "🍛",
            nutrition: {
                calories: "380kcal",
                protein: "28g",
                carbs: "35g",
                fat: "14g"
            },
            recipe_steps: [
                "닭가슴살을 한입 크기로 썰어주세요",
                "야채들을 적당한 크기로 썰어주세요",
                "팬에 닭고기를 볶은 후 야채를 넣어주세요",
                "카레가루와 코코넛밀크를 넣고 끓여주세요"
            ]
        }
    ];
    
    // 그룹 모드일 때는 그룹 메뉴 데이터 추가
    if (currentMode === 'group') {
        allMenus.push(
            {
                id: 1,
                name: "삼겹살 BBQ 파티",
                reason: "그룹의 화합 운세가 높아 함께 구워먹는 음식이 최고입니다",
                category: "한식",
                ingredients: ["삼겹살", "상추", "마늘", "된장찌개", "김치", "쌈장"],
                cooking_time: "45분",
                difficulty: "쉬움",
                serving_size: "4-6인분",
                image: "🥓",
                group_benefit: "모든 참석자가 함께 참여할 수 있는 요리",
                sharing_type: "공유형",
                nutrition: {
                    calories: "450kcal",
                    protein: "32g",
                    carbs: "15g",
                    fat: "28g"
                },
                group_tips: [
                    "각자 좋아하는 쌈 채소를 준비해보세요",
                    "다양한 소스로 취향에 맞게 즐겨보세요",
                    "함께 굽는 재미로 대화가 더욱 활발해집니다"
                ]
            }
        );
    }
    
    return allMenus.find(menu => menu.id == menuId) || allMenus[0];
}

// 결과 공유
function shareResults() {
    try {
        // 로딩 상태 표시
        shareBtn.disabled = true;
        shareBtn.textContent = '이미지 생성 중...';
        
        // 현재 결과 데이터 수집
        const fortuneData = getCurrentFortuneData();
        const menuData = getCurrentMenuData();
        
        // 이미지 생성
        generateShareImage(fortuneData, menuData);
        
    } catch (error) {
        console.error('이미지 생성 오류:', error);
        showNotification('이미지 생성 중 오류가 발생했습니다.', 'error');
    } finally {
        // 버튼 상태 복원
        shareBtn.disabled = false;
        shareBtn.textContent = '이미지로 공유';
    }
}

// 현재 운세 데이터 수집
function getCurrentFortuneData() {
    // DOM에서 현재 표시된 운세 데이터를 추출
    const fortuneContainer = document.querySelector('.fortune-container');
    if (!fortuneContainer) return null;
    
    const data = {
        mode: currentMode,
        date: new Date().toLocaleDateString('ko-KR'),
        totalScore: null,
        categories: {},
        groupData: null
    };
    
    if (currentMode === 'individual') {
        // 개인 모드 데이터 추출
        const scoreElement = document.querySelector('.score-value');
        if (scoreElement) {
            data.totalScore = parseInt(scoreElement.textContent);
        }
        
        // 카테고리별 데이터 추출
        const categoryCards = document.querySelectorAll('.fortune-card');
        categoryCards.forEach(card => {
            const category = card.dataset.category;
            const scoreElement = card.querySelector('.category-score');
            const messageElement = card.querySelector('.category-message');
            
            if (category && scoreElement && messageElement) {
                data.categories[category] = {
                    score: parseInt(scoreElement.textContent.replace('점', '')),
                    message: messageElement.textContent.trim()
                };
            }
        });
    } else {
        // 그룹 모드 데이터 추출
        const groupScores = document.querySelectorAll('.group-score-item .score-value');
        const groupMessage = document.querySelector('.group-message');
        
        data.groupData = {
            averageScore: groupScores[0] ? parseInt(groupScores[0].textContent) : 0,
            harmonyScore: groupScores[1] ? parseInt(groupScores[1].textContent) : 0,
            message: groupMessage ? groupMessage.textContent.trim() : '',
            participantCount: document.querySelectorAll('.participant-fortune').length
        };
    }
    
    return data;
}

// 현재 메뉴 데이터 수집
function getCurrentMenuData() {
    const menuCards = document.querySelectorAll('.menu-card');
    const menus = [];
    
    menuCards.forEach(card => {
        const nameElement = card.querySelector('.menu-name');
        const reasonElement = card.querySelector('.menu-reason');
        
        if (nameElement && reasonElement) {
            menus.push({
                name: nameElement.textContent.trim(),
                reason: reasonElement.textContent.trim()
            });
        }
    });
    
    return menus;
}

// Canvas API를 사용한 이미지 생성
function generateShareImage(fortuneData, menuData) {
    // Canvas 요소 생성
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // 이미지 크기 설정 (Instagram 정사각형 비율)
    const width = 1080;
    const height = 1080;
    canvas.width = width;
    canvas.height = height;
    
    // 배경 그라데이션 생성
    const gradient = ctx.createLinearGradient(0, 0, 0, height);
    gradient.addColorStop(0, '#667eea');
    gradient.addColorStop(1, '#764ba2');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);
    
    // 기본 스타일 설정
    ctx.textAlign = 'center';
    ctx.fillStyle = '#ffffff';
    
    // 제목 그리기
    ctx.font = 'bold 48px Arial, sans-serif';
    ctx.fillText('🔮 오늘의 운세 & 식사 추천', width / 2, 100);
    
    // 날짜 그리기
    ctx.font = '24px Arial, sans-serif';
    ctx.fillStyle = '#f0f0f0';
    ctx.fillText(fortuneData.date, width / 2, 140);
    
    let yPosition = 200;
    
    if (currentMode === 'individual') {
        // 개인 모드 이미지 생성
        yPosition = drawIndividualFortune(ctx, fortuneData, yPosition, width);
    } else {
        // 그룹 모드 이미지 생성
        yPosition = drawGroupFortune(ctx, fortuneData, yPosition, width);
    }
    
    // 메뉴 추천 그리기
    yPosition = drawMenuRecommendations(ctx, menuData, yPosition, width);
    
    // 브랜딩 정보 그리기
    drawBranding(ctx, width, height);
    
    // 이미지 다운로드 제공
    downloadImage(canvas);
}

// 개인 운세 그리기
function drawIndividualFortune(ctx, fortuneData, startY, width) {
    let yPos = startY;
    
    // 총 점수 그리기
    ctx.font = 'bold 36px Arial, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`총 운세: ${fortuneData.totalScore}점`, width / 2, yPos);
    yPos += 60;
    
    // 점수 설명 그리기
    ctx.font = '20px Arial, sans-serif';
    ctx.fillStyle = '#f0f0f0';
    const scoreDesc = getScoreDescription(fortuneData.totalScore);
    ctx.fillText(scoreDesc, width / 2, yPos);
    yPos += 80;
    
    // 카테고리별 운세 그리기
    const categoryNames = {
        love: { name: '💕 사랑운', color: '#ff6b9d' },
        health: { name: '🌿 건강운', color: '#51cf66' },
        wealth: { name: '💰 재물운', color: '#ffd43b' },
        career: { name: '📚 학업/직장운', color: '#74c0fc' }
    };
    
    Object.entries(fortuneData.categories).forEach(([key, category]) => {
        const categoryInfo = categoryNames[key];
        if (!categoryInfo) return;
        
        // 카테고리 제목과 점수
        ctx.font = 'bold 24px Arial, sans-serif';
        ctx.fillStyle = categoryInfo.color;
        ctx.fillText(`${categoryInfo.name}: ${category.score}점`, width / 2, yPos);
        yPos += 40;
        
        // 메시지 (여러 줄 처리)
        ctx.font = '18px Arial, sans-serif';
        ctx.fillStyle = '#ffffff';
        const lines = wrapText(ctx, category.message, width - 100);
        lines.forEach(line => {
            ctx.fillText(line, width / 2, yPos);
            yPos += 25;
        });
        yPos += 20;
    });
    
    return yPos;
}

// 그룹 운세 그리기
function drawGroupFortune(ctx, fortuneData, startY, width) {
    let yPos = startY;
    
    // 그룹 정보 그리기
    ctx.font = 'bold 32px Arial, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`👥 ${fortuneData.groupData.participantCount}명 그룹 운세`, width / 2, yPos);
    yPos += 60;
    
    // 그룹 점수들 그리기
    ctx.font = 'bold 24px Arial, sans-serif';
    ctx.fillStyle = '#ffd43b';
    ctx.fillText(`평균 점수: ${fortuneData.groupData.averageScore}점`, width / 2, yPos);
    yPos += 40;
    
    ctx.fillStyle = '#ff6b9d';
    ctx.fillText(`화합 점수: ${fortuneData.groupData.harmonyScore}점`, width / 2, yPos);
    yPos += 60;
    
    // 그룹 메시지 그리기
    ctx.font = '20px Arial, sans-serif';
    ctx.fillStyle = '#ffffff';
    const lines = wrapText(ctx, fortuneData.groupData.message, width - 100);
    lines.forEach(line => {
        ctx.fillText(line, width / 2, yPos);
        yPos += 30;
    });
    yPos += 40;
    
    return yPos;
}

// 메뉴 추천 그리기
function drawMenuRecommendations(ctx, menuData, startY, width) {
    let yPos = startY;
    
    // 메뉴 추천 제목
    ctx.font = 'bold 28px Arial, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('🍽️ 추천 메뉴', width / 2, yPos);
    yPos += 50;
    
    // 메뉴들 그리기 (최대 3개)
    menuData.slice(0, 3).forEach((menu, index) => {
        // 메뉴 이름
        ctx.font = 'bold 22px Arial, sans-serif';
        ctx.fillStyle = '#ffd43b';
        ctx.fillText(`${index + 1}. ${menu.name}`, width / 2, yPos);
        yPos += 35;
        
        // 추천 이유 (여러 줄 처리)
        ctx.font = '16px Arial, sans-serif';
        ctx.fillStyle = '#f0f0f0';
        const lines = wrapText(ctx, menu.reason, width - 120);
        lines.forEach(line => {
            ctx.fillText(line, width / 2, yPos);
            yPos += 22;
        });
        yPos += 25;
    });
    
    return yPos;
}

// 브랜딩 정보 그리기
function drawBranding(ctx, width, height) {
    // 하단 브랜딩
    ctx.font = '16px Arial, sans-serif';
    ctx.fillStyle = '#cccccc';
    ctx.textAlign = 'center';
    ctx.fillText('Fortune Dinner Recommender', width / 2, height - 40);
    ctx.fillText('오늘의 운세와 식사 추천 서비스', width / 2, height - 20);
}

// 텍스트 줄바꿈 처리
function wrapText(ctx, text, maxWidth) {
    const words = text.split(' ');
    const lines = [];
    let currentLine = words[0];
    
    for (let i = 1; i < words.length; i++) {
        const word = words[i];
        const width = ctx.measureText(currentLine + ' ' + word).width;
        if (width < maxWidth) {
            currentLine += ' ' + word;
        } else {
            lines.push(currentLine);
            currentLine = word;
        }
    }
    lines.push(currentLine);
    
    return lines;
}

// 점수 설명 생성
function getScoreDescription(score) {
    if (score >= 90) return '🌟 최고의 하루가 될 것 같아요!';
    if (score >= 80) return '✨ 좋은 일이 많을 것 같아요!';
    if (score >= 70) return '😊 평온하고 안정적인 하루예요';
    if (score >= 60) return '🤔 조심스럽게 행동하는 것이 좋겠어요';
    if (score >= 50) return '😐 평범한 하루가 될 것 같아요';
    return '💪 힘든 시기지만 곧 좋아질 거예요!';
}

// 이미지 다운로드
function downloadImage(canvas) {
    try {
        // Canvas를 Blob으로 변환
        canvas.toBlob((blob) => {
            if (!blob) {
                showNotification('이미지 생성에 실패했습니다.', 'error');
                return;
            }
            
            // 다운로드 링크 생성
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            
            // 파일명 생성 (날짜 포함)
            const today = new Date();
            const dateStr = today.toISOString().split('T')[0];
            const modeStr = currentMode === 'individual' ? '개인' : '그룹';
            link.download = `운세_${modeStr}_${dateStr}.png`;
            
            // 다운로드 실행
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // 메모리 정리
            URL.revokeObjectURL(url);
            
            // 성공 알림
            showNotification('이미지가 성공적으로 생성되었습니다! 다운로드를 확인해주세요.', 'success');
            
        }, 'image/png', 0.9);
        
    } catch (error) {
        console.error('이미지 다운로드 오류:', error);
        showNotification('이미지 다운로드 중 오류가 발생했습니다.', 'error');
    }
}

// 새로운 운세 시작
function startNewFortune() {
    // 결과 섹션 숨기기
    resultsSection.classList.add('hidden');
    
    // 진행률 표시기 제거
    const existingProgress = document.querySelector('.input-progress');
    if (existingProgress) {
        existingProgress.remove();
    }
    
    // 모드 선택으로 돌아가기
    goBackToModeSelection();
    
    // 성공 메시지 표시
    showNotification('새로운 운세를 시작합니다! 🎯', 'success', 2000);
}

// 디바운스 함수 (성능 최적화)
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 스로틀 함수 (성능 최적화)
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// 지연 로딩 (Lazy Loading)
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// 메모리 사용량 모니터링
function monitorMemoryUsage() {
    if (performance.memory) {
        const memoryInfo = performance.memory;
        const usedMB = Math.round(memoryInfo.usedJSHeapSize / 1048576);
        const totalMB = Math.round(memoryInfo.totalJSHeapSize / 1048576);
        
        console.log(`메모리 사용량: ${usedMB}MB / ${totalMB}MB`);
        
        // 메모리 사용량이 높으면 경고
        if (usedMB > 100) {
            console.warn('높은 메모리 사용량이 감지되었습니다.');
        }
    }
}

// 사용자 상호작용 추적
function trackUserInteraction(action, details = {}) {
    const interaction = {
        action,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        viewport: {
            width: window.innerWidth,
            height: window.innerHeight
        },
        ...details
    };
    
    console.log('사용자 상호작용:', interaction);
    
    // 실제 서비스에서는 분석 서비스로 전송
    // analytics.track(interaction);
}

// 오류 리포팅
function reportError(error, context = {}) {
    const errorReport = {
        message: error.message,
        stack: error.stack,
        timestamp: new Date().toISOString(),
        url: window.location.href,
        userAgent: navigator.userAgent,
        context
    };
    
    console.error('오류 리포트:', errorReport);
    
    // 실제 서비스에서는 오류 추적 서비스로 전송
    // errorTracker.report(errorReport);
}

// 전역 오류 처리기
window.addEventListener('error', (event) => {
    reportError(event.error, {
        type: 'javascript',
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
    });
});

window.addEventListener('unhandledrejection', (event) => {
    reportError(new Error(event.reason), {
        type: 'promise_rejection'
    });
});

// 성능 메트릭 수집
function collectPerformanceMetrics() {
    if (performance.getEntriesByType) {
        const navigation = performance.getEntriesByType('navigation')[0];
        const paint = performance.getEntriesByType('paint');
        
        const metrics = {
            domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
            loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
            firstPaint: paint.find(entry => entry.name === 'first-paint')?.startTime,
            firstContentfulPaint: paint.find(entry => entry.name === 'first-contentful-paint')?.startTime
        };
        
        console.log('성능 메트릭:', metrics);
        return metrics;
    }
}

// 사용자 경험 개선을 위한 디바운스된 이벤트 리스너 설정
const debouncedInputValidation = debounce((inputElement) => {
    if (currentMode === 'individual') {
        validateIndividualInput();
    } else {
        validateParticipantInput(inputElement);
    }
}, 300);

const throttledScrollHandler = throttle(() => {
    // 스크롤 관련 처리
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollTop > 100) {
        document.body.classList.add('scrolled');
    } else {
        document.body.classList.remove('scrolled');
    }
}, 100);

// 목업 운세 데이터 생성 (개발/테스트용)
function generateMockFortuneData(inputData) {
    const mockData = {
        mode: inputData.mode,
        message: "목업 데이터로 운세를 생성했습니다.",
        timestamp: new Date().toISOString()
    };
    
    if (inputData.mode === 'individual') {
        mockData.individual_fortune = {
            total_score: Math.floor(Math.random() * 40) + 60, // 60-100 점
            categories: {
                love: {
                    score: Math.floor(Math.random() * 40) + 60,
                    message: "사랑에 행운이 따를 것입니다."
                },
                health: {
                    score: Math.floor(Math.random() * 40) + 60,
                    message: "건강에 주의하며 균형잡힌 생활을 하세요."
                },
                wealth: {
                    score: Math.floor(Math.random() * 40) + 60,
                    message: "재물운이 상승하고 있습니다."
                },
                career: {
                    score: Math.floor(Math.random() * 40) + 60,
                    message: "꾸준한 노력이 결실을 맺을 것입니다."
                }
            }
        };
    } else {
        mockData.group_fortune = {
            average_score: Math.floor(Math.random() * 30) + 70,
            harmony_score: Math.floor(Math.random() * 30) + 70,
            dominant_categories: ['love', 'wealth'],
            group_message: "오늘 모임은 화합과 즐거움이 가득할 것입니다",
            individual_fortunes: inputData.participants.map((participant, index) => ({
                name: participant.name,
                total_score: Math.floor(Math.random() * 40) + 60,
                categories: {
                    love: { score: Math.floor(Math.random() * 40) + 60, message: "사랑운이 좋습니다" },
                    health: { score: Math.floor(Math.random() * 40) + 60, message: "건강에 주의하세요" },
                    wealth: { score: Math.floor(Math.random() * 40) + 60, message: "재물운 상승" },
                    career: { score: Math.floor(Math.random() * 40) + 60, message: "꾸준한 노력 필요" }
                }
            }))
        };
    }
    
    return mockData;
}

// 목업 메뉴 데이터 생성 (개발/테스트용)
function generateMockMenuData(inputData) {
    return {
        mode: inputData.mode,
        message: "목업 데이터로 메뉴를 추천했습니다.",
        recommendations: inputData.mode === 'individual' ? 
            ["김치찌개", "연어 샐러드", "치킨 카레"] :
            ["삼겹살 BBQ 파티", "해물 파전 & 막걸리", "치킨 & 피자 콤보"],
        timestamp: new Date().toISOString()
    };
}

// 임시 스타일 (개발용)
const tempStyle = document.createElement('style');
tempStyle.textContent = `
    .temp-result {
        background: #f7fafc;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    .temp-result pre {
        background: #2d3748;
        color: #e2e8f0;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
        font-size: 0.8rem;
        margin-top: 10px;
    }
`;
document.head.appendChild(tempStyle);