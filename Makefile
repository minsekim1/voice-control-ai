.PHONY: clean build run clean-all

# 기본 변수 설정
ANDROID_DIR := android
GRADLE := ./gradlew

# 빌드
build:
	@echo "Building Android project..."
	cd $(ANDROID_DIR) && $(GRADLE) assembleDebug

# 실행
run:
	@echo "Running Android app..."
	cd $(ANDROID_DIR) && $(GRADLE) installDebug

# 클린 빌드
clean:
	@echo "Cleaning Android project..."
	cd $(ANDROID_DIR) && $(GRADLE) clean

# 모든 빌드 파일과 추적되지 않는 파일 제거
clean-all: clean
	@echo "Removing all untracked files..."
	git clean -fd

reset:
	git reset --hard
	git clean -fd

# 도움말
help:
	@echo "Available commands:"
	@echo "  make build      - Build the project"
	@echo "  make run        - Run the app on connected device"
	@echo "  make clean      - Clean build files"
	@echo "  make clean-all  - Clean all files including untracked ones"
	@echo "  make help       - Show this help message" 