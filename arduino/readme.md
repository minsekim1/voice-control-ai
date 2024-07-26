# 보드 업로드 방법

## 설치

- 아두이노 CLI를 설치해야합니다.

## 보드 및 코어 설치:

```
arduino-cli core update-index
arduino-cli core install esp32:esp32
```

## 보드 목록 확인:

```
arduino-cli board list
```

## 스케치 컴파일: 스케치를 컴파일하여 바이너리 파일을 생성합니다.

```
arduino-cli compile --fqbn esp32:esp32:esp32c3 path/to/your/sketch

example) arduino-cli compile --fqbn esp32:esp32:esp32c3 arduino/complete_example/led_fade_in_out

```

## ESP32 보드로 업로드

```
arduino-cli upload -p <포트> --fqbn esp32:esp32:esp32c3 path/to/your/sketch

example) arduino-cli upload -p COM7 --fqbn esp32:esp32:esp32c3 arduino/complete_example/led_fade_in_out

```

## 스크립트로 바이너리 생성 & 업로드

```
./arduino/upload_sketch.sh <포트> path/to/your/sketch

example) ./arduino/upload_sketch.sh COM7 arduino/complete_example/bluetooth_led_control

```

## 아두이노 관련 Q&A

### Seiral.print가 안 먹음

- 시리얼 출력을 하려면 보드 옵션에서 USB CDC On Boot 를 Enable 해야 합니다.

### 갑자기 Arduino IDE에서 실행이 안됨

- 보드 체크 (도구 -> 보드 -> esp32 -> ESP32C3 Dev Module)

### 와이파이 연결안됨

- 5G말고 2.4G로 연결해야됨
