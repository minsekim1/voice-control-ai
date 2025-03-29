# Voice Control AI

음성 인식 서버를 제공하는 프로젝트입니다. 네이버 클라우드 CLOVA Speech Recognition을 사용하여 음성 인식을 지원하며, REST API와 WebSocket을 통해 음성 인식 결과를 제공합니다.

## 주요 기능

- REST API 엔드포인트 제공
- 실시간 음성 스트리밍 처리
- 네이버 클라우드 CLOVA Speech Recognition
- 마이크 장치 관리
- 서버 설정 관리

## API 엔드포인트

### 음성 인식
- `POST /api/v1/recognition/file`: 음성 파일 업로드 및 인식
- `WebSocket /api/v1/recognition/stream`: 실시간 음성 스트리밍 인식

### 장치 관리
- `GET /api/v1/devices/list`: 사용 가능한 오디오 장치 목록 조회
- `GET /api/v1/devices/default`: 기본 입력 장치 정보 조회

### 설정 관리
- `GET /api/v1/settings`: 현재 서버 설정 조회
- `PUT /api/v1/settings`: 서버 설정 업데이트

## 시스템 요구사항

- Python 3.11 이상
- macOS
- 마이크 장치
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

### 실시간 음성 스트리밍
```python
import websockets
import asyncio

async def stream_audio():
    async with websockets.connect('ws://localhost:8000/api/v1/recognition/stream') as websocket:
        # 오디오 스트리밍 로직
        pass

asyncio.get_event_loop().run_until_complete(stream_audio())
```

## 개발자 가이드

### 프로젝트 구조
```
voice-control-ai/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── recognition.py
│   │   │   ├── devices.py
│   │   │   └── settings.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
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
