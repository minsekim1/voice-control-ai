# Voice Control AI

음성 인식 기반의 AI 제어 시스템입니다. 온라인과 오프라인 음성 인식을 동시에 지원하며, 인식된 음성 명령어를 실행합니다.

## 브랜치 구조

### main
- 프로젝트의 기본 문서화 파일만 포함
- `README.md`: 프로젝트 설명 및 사용 방법
- `LICENSE`: MIT 라이선스

### voice-server
- 음성 인식 서버 구현
- 음성 데이터를 텍스트로 변환하는 기능 제공
- REST API 엔드포인트 제공
- 실시간 음성 스트리밍 처리
- 다중 언어 지원 (한국어, 영어)

## 시스템 요구사항

- Python 3.8 이상
- macOS (테스트 완료)
- 마이크 장치
- 인터넷 연결 (온라인 음성 인식용)

## 설치 방법

1. 저장소 클론:
```bash
git clone https://github.com/minsekim1/voice-control-ai.git
cd voice-control-ai
```

2. 개발 환경 설정:
```bash
make setup
```

3. 가상 환경 생성 및 패키지 설치:
```bash
make install
```

4. Vosk 한국어 모델 다운로드:
- [Vosk 모델 다운로드 페이지](https://alphacephei.com/vosk/models)에서 `vosk-model-small-ko-0.22` 모델을 다운로드
- 다운로드한 모델을 프로젝트 루트 디렉토리에 `vosk-model-ko` 이름으로 압축 해제

5. Google Cloud Speech-to-Text API 설정:
- Google Cloud Console에서 프로젝트 생성
- Speech-to-Text API 활성화
- 서비스 계정 키 생성 및 다운로드
- 다운로드한 키 파일을 프로젝트 루트 디렉토리에 `google_credentials.json` 이름으로 저장

## 사용 방법

1. 프로그램 실행:
```bash
make run
```

2. 마이크 장치 선택:
- 프로그램 실행 시 사용 가능한 마이크 장치 목록이 표시됩니다
- 번호를 입력하여 사용할 마이크 장치를 선택합니다

3. 음성 인식:
- 온라인과 오프라인 음성 인식이 동시에 시작됩니다
- 음성을 입력하면 실시간으로 인식 결과가 표시됩니다

4. 프로그램 종료:
- `Ctrl+C`를 눌러 프로그램을 종료합니다

## 개발자 가이드

### 프로젝트 구조
```
voice-control-ai/
├── app.py              # 메인 애플리케이션
├── module/             # 모듈 디렉토리
│   ├── stt.py         # 온라인 음성 인식
│   ├── offline_stt.py # 오프라인 음성 인식
│   └── catch_voice.py # 음성 명령어 처리
├── model/             # 모델 파일 디렉토리
└── requirements.txt   # 의존성 패키지 목록
```

### Makefile 명령어
- `make setup`: 개발 환경 설정
- `make install`: 패키지 설치
- `make run`: 프로그램 실행
- `make clean`: 캐시 파일 정리
- `make push`: Git 변경사항 푸시
- `make backup`: requirements.txt 백업 및 푸시

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 문의

문제나 제안사항이 있으시면 [Issues](https://github.com/minsekim1/voice-control-ai/issues) 페이지를 통해 알려주세요.
