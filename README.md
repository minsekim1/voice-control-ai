# Voice Control AI

음성 인식 기반의 AI 제어 시스템입니다. 온라인과 오프라인 음성 인식을 동시에 지원하며, 인식된 음성 명령어를 실행합니다.

## 브랜치 구조

### main
- 프로젝트의 기본 문서화 파일만 포함
- `README.md`: 프로젝트 설명 및 사용 방법
- `LICENSE`: MIT 라이선스

### voice-server
- 음성 인식 서버 구현
- 네이버 클라우드 CLOVA Speech Recognition 서버 제공
- REST API 및 WebSocket 엔드포인트 제공
- 실시간 음성 스트리밍 처리

서버 실행 및 상세 기능을 확인하려면 voice-server 브랜치로 전환하세요:
```bash
git checkout voice-server
```

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

## 개발자 가이드

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
