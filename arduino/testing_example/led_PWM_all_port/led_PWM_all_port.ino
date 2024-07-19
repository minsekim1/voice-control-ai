// @desctipion 전체 포트에 대해서 LED 불이 페이드인/아웃 반복합니다.
// GPIO 핀 배열
const int ledPins[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 21};
const int numPins = sizeof(ledPins) / sizeof(ledPins[0]);

void setup() {
  for (int i = 0; i < numPins; i++) {
    pinMode(ledPins[i], OUTPUT); // 각 핀을 출력으로 설정
  }
}

void loop() {
  // 페이드인
  for (int fadeValue = 0; fadeValue <= 255; fadeValue += 5) {
    for (int i = 0; i < numPins; i++) {
      analogWrite(ledPins[i], fadeValue);
    }
    delay(30);
  }
  // 페이드아웃
  for (int fadeValue = 255; fadeValue >= 0; fadeValue -= 5) {
    for (int i = 0; i < numPins; i++) {
      analogWrite(ledPins[i], fadeValue);
    }
    delay(30);
  }
}
