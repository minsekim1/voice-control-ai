# Voice Control AI

음성 인식 서버를 제공하는 프로젝트입니다. 네이버 클라우드 CLOVA Speech Recognition을 사용하여 음성 인식을 지원합니다.

## 주요 기능

- REST API 엔드포인트 제공
- 네이버 클라우드 CLOVA Speech Recognition
- WAV 파일 기반 음성 인식

## API 엔드포인트

### 음성 인식
- `POST /api/v1/recognition/file`: 음성 파일 업로드 및 인식

## 시스템 요구사항

- Python 3.11 이상
- macOS
- 네이버 클라우드 계정 및 CLOVA Speech Recognition 서비스 활성화

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/minsekim1/voice-control-ai.git
cd voice-control-ai
```

2. 개발 환경 설정
```bash
make setup
```

3. 패키지 설치
```bash
make install
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 입력합니다:
```
NAVER_CLOUD_ACCESS_KEY=your_client_id_here
NAVER_CLOUD_SECRET_KEY=your_client_secret_here
```

## 서버 실행

```bash
make start
```

서버는 http://0.0.0.0:8000 에서 실행되며, API 문서는 http://0.0.0.0:8000/docs 에서 확인할 수 있습니다.

## API 사용 예시

### 음성 파일 업로드
```bash
curl -X POST "http://localhost:8000/api/v1/recognition/file" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio.wav"
```

## 개발자 가이드

### 프로젝트 구조
```
voice-control-ai/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── recognition.py
│   │   └── __init__.py
│   ├── core/
│   │   └── naver_stt.py
│   └── main.py
├── tests/
│   ├── audio/
│   └── test_naver_stt.py
├── Makefile
└── requirements.txt
```

### Makefile 명령어
- `make setup`: 개발 환경 설정
- `make install`: 패키지 설치
- `make start`: 서버 실행
- `make test`: 테스트 실행
- `make clean`: 캐시 파일 정리
- `make push`: Git 변경사항 푸시
- `make backup`: requirements.txt 백업

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 기여하기

1. 이슈 생성
2. 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add some amazing feature'`)
4. 브랜치 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 연락처

문제나 제안사항이 있으시면 이슈를 생성해주세요.
