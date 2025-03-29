.PHONY: install run clean push backup

# 기본 설정
PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/pip

# 설치
install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

# 실행
run:
	$(PYTHON) app.py

# 정리
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete

# Git 관련
push:
	git add .
	git commit -m "자동 커밋"
	git push origin main

backup:
	$(PIP) freeze > requirements.txt
	git add .
	git commit -m "백업"
	git push origin main

# 개발 환경 설정
setup:
	brew install portaudio
	brew install git-lfs
	git lfs install
	git lfs track "model/**/*.fst"
	git lfs track "model/**/*.mdl"
	git lfs track "model/**/*.mat"
	git lfs track "model/**/*.dubm"
	git lfs track "model/**/*.ie" 