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

### 링크

맥 -> Adafruit QT PyESP32-C3
타오바오 ESP 칩 구매처 -> https://item.taobao.com/item.htm?spm=a1z10.3-c-s.w4002-24438210134.9.27bc6ea3Er0bkc&id=707413078834
ESP32 튜토리얼 -> https://www.nologo.tech/product/esp32/esp32c3SuperMini/esp32C3SuperMini.html#q2-%E4%B8%8A%E4%BC%A0%E4%B9%8B%E5%90%8E%E7%A8%8B%E5%BA%8F%E6%97%A0%E6%B3%95%E8%BF%90%E8%A1%8C
튜토리얼2 -> https://docs.geeksman.com/esp32/#%E7%9B%AE%E5%BD%95-arduino
타오바오 추가 배터리 판매처 -> https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-24438210134.20.5e806ea3sbuxO1&id=756027058909

### 핀번호

#### 좌측

- 5V -> 5V 전원을 공급합니다.
- GND -> 접지 핀입니다.
- 3V -> 3.3V 전원을 공급합니다.
- GPIO4 - SCK-A4 -> SPI 클럭 핀(SCK)으로도 사용할 수 있습니다.
- GPIO3 - SCK-A3 -> SPI 클럭 핀(SCK)으로도 사용할 수 있습니다.
- GPIO2 - SCK-A2 -> SPI 클럭 핀(SCK)으로도 사용할 수 있습니다.
- GPIO1 - SCK-A1 -> SPI 클럭 핀(SCK)으로도 사용할 수 있습니다.
- GPIO0 - SCK-A0 -> SPI 클럭 핀(SCK)으로도 사용할 수 있습니다.

#### 우측

- GPIO5 A5-MISO -> SPI의 MISO (Master In Slave Out) 핀으로도 사용할 수 있습니다.
- GPIO6 MOSI -> SPI의 MOSI (Master Out Slave In) 핀으로도 사용할 수 있습니다.
- GPIO7 - SS -> SPI의 SS (Slave Select) 핀으로도 사용할 수 있습니다.
- GPIO8 - SDA -> I2C의 SDA (Data) 핀으로도 사용할 수 있습니다.
- GPIO9 - SCL -> I2C의 SCL (Clock) 핀으로도 사용할 수 있습니다.
- GPIO10
- GPIO20 - RX -> UART의 RX (Receive) 핀으로 사용될 수 있습니다.
- GPIO21 - TX -> UART의 TX (Transmit) 핀으로 사용될 수 있습니다.
