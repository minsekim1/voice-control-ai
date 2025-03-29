# Voice Control AI

음성 인식 및 제어를 위한 AI 시스템입니다. 온라인과 오프라인 음성 인식을 동시에 지원하며, 실시간 음성 스트리밍 처리가 가능합니다.

## 주요 기능

- REST API 엔드포인트 제공
- 실시간 음성 스트리밍 처리
- 온라인/오프라인 음성 인식 동시 지원
- 다중 언어 지원 (한국어, 영어)
- WebSocket을 통한 실시간 결과 전송

## API 엔드포인트

### 음성 인식 API
- `POST /api/v1/recognize`: 음성 파일 업로드 및 인식
- `POST /api/v1/stream`: 실시간 음성 스트리밍 처리
- `GET /api/v1/status`: 서버 상태 확인

### 설정 API
- `GET /api/v1/devices`: 사용 가능한 마이크 장치 목록 조회
- `POST /api/v1/devices`: 마이크 장치 설정 변경
- `GET /api/v1/languages`: 지원하는 언어 목록 조회

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
git checkout voice-server
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

## 서버 실행

```bash
make run
```

서버는 기본적으로 `http://localhost:5000`에서 실행됩니다.

## API 사용 예시

### 음성 파일 업로드 및 인식
```bash
curl -X POST http://localhost:5000/api/v1/recognize \
  -H "Content-Type: multipart/form-data" \
  -F "audio=@audio.wav" \
  -F "language=ko"
```

### 실시간 음성 스트리밍
```python
import websockets
import asyncio

async def stream_audio():
    async with websockets.connect('ws://localhost:5000/api/v1/stream') as websocket:
        while True:
            # 오디오 데이터 전송
            await websocket.send(audio_data)
            # 인식 결과 수신
            result = await websocket.recv()
            print(result)

asyncio.run(stream_audio())
```

## 개발자 가이드

### 프로젝트 구조
```
voice-control-ai/
├── app.py              # 메인 애플리케이션
├── api/                # API 엔드포인트
│   ├── routes.py      # 라우트 정의
│   └── schemas.py     # 데이터 모델
├── core/              # 핵심 기능
│   ├── stt.py        # 온라인 음성 인식
│   ├── offline_stt.py # 오프라인 음성 인식
│   └── audio.py      # 오디오 처리
├── config/           # 설정 파일
└── tests/            # 테스트 코드
```

### Makefile 명령어
- `make setup`: 개발 환경 설정
- `make install`: 패키지 설치
- `make run`: 서버 실행
- `make test`: 테스트 실행
- `make clean`: 캐시 파일 정리
- `make push`: Git 변경사항 푸시

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
