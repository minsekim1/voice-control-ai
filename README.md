# Voice Control AI - Android Test App

음성 인식 서버를 테스트하기 위한 안드로이드 앱입니다. 네이버 클라우드 CLOVA Speech Recognition 서버에 음성 데이터를 전송하여 테스트합니다.

## 주요 기능

- 음성 녹음 및 WAV 파일 변환
- 서버로 음성 파일 업로드
- 인식 결과 표시

## 시스템 요구사항

- Android Studio Hedgehog | 2023.1.1
- Android SDK 34 (Android 14.0)
- Kotlin 1.9.0
- 네이버 클라우드 CLOVA Speech Recognition 서버 (http://localhost:8000)

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/minsekim1/voice-control-ai.git
cd voice-control-ai
```

2. Android Studio에서 프로젝트 열기
- `android` 디렉토리를 Android Studio에서 열기

3. 환경 변수 설정
`local.properties` 파일에 서버 URL을 설정합니다:
```
SERVER_URL=http://localhost:8000
```

## 앱 실행

1. Android Studio에서 앱 실행
2. 녹음 버튼을 눌러 음성 녹음 시작
3. 녹음 종료 후 자동으로 서버로 전송
4. 인식 결과 확인

## API 엔드포인트

### 음성 인식
- `POST /api/v1/recognition/file`: 음성 파일 업로드 및 인식

## 개발자 가이드

### 프로젝트 구조
```
android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/voicecontrol/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── api/
│   │   │   │   │   ├── ApiService.kt
│   │   │   │   │   └── RetrofitClient.kt
│   │   │   │   ├── model/
│   │   │   │   │   └── RecognitionResponse.kt
│   │   │   │   └── utils/
│   │   │   │       └── AudioRecorder.kt
│   │   │   └── res/
│   │   │       ├── layout/
│   │   │       │   └── activity_main.xml
│   │   │       └── values/
│   │   │           └── strings.xml
│   │   └── test/
│   └── build.gradle
└── build.gradle
```

### Makefile 명령어
- `make build`: 앱 빌드
- `make install`: 앱 설치
- `make clean`: 빌드 파일 정리
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
