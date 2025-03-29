.PHONY: setup install run test clean push backup check-deps

# Python 가상 환경 설정
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

# 기본 설정
setup:
	@echo "개발 환경 설정 중..."
	brew install git-lfs
	git lfs install
	git lfs track "*.model"
	git lfs track "*.bin"
	git lfs track "*.fst"
	git lfs track "*.hmm"
	git lfs track "*.conf"
	git lfs track "*.json"
	@echo "개발 환경 설정이 완료되었습니다."

# 패키지 설치
install:
	@echo "가상 환경 생성 및 패키지 설치 중..."
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "패키지 설치가 완료되었습니다."

# 의존성 체크 및 설치
check-deps:
	@echo "필요한 패키지 확인 중..."
	@if [ ! -d "$(VENV)" ]; then \
		echo "가상 환경이 없습니다. 가상 환경을 생성합니다..."; \
		make install; \
	fi
	@if [ ! -f "requirements.txt" ]; then \
		echo "requirements.txt 파일이 없습니다. 기본 패키지를 설치합니다..."; \
		$(PIP) install fastapi uvicorn python-dotenv websockets; \
	else \
		$(PIP) install -r requirements.txt; \
	fi

# 서버 실행
start: check-deps
	@echo "서버 실행 중..."
	$(PYTHON) run.py

# 테스트 실행
test: check-deps
	@echo "테스트 실행 중..."
	$(PYTHON) -m pytest tests/ -v -s

# 캐시 파일 정리
clean:
	@echo "캐시 파일 정리 중..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	@echo "캐시 파일이 정리되었습니다."

# Git 변경사항 푸시
push:
	@echo "Git 변경사항 푸시 중..."
	git add .
	git commit -m "chore: 자동 커밋"
	git push origin voice-server

# requirements.txt 백업
backup:
	@echo "requirements.txt 백업 중..."
	$(PIP) freeze > requirements.txt
	git add requirements.txt
	git commit -m "chore: requirements.txt 업데이트"
	git push origin voice-server

# 도움말
help:
	@echo "사용 가능한 명령어:"
	@echo "  make setup    - 개발 환경 설정"
	@echo "  make install  - 패키지 설치"
	@echo "  make start    - 서버 실행"
	@echo "  make test     - 테스트 실행"
	@echo "  make clean    - 캐시 파일 정리"
	@echo "  make push     - Git 변경사항 푸시"
	@echo "  make backup   - requirements.txt 백업"

# 가상 환경 활성화 스크립트
venv:
	@echo "가상 환경을 활성화하려면 다음 명령어를 실행하세요:"
	@echo "source venv/bin/activate"
