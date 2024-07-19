// LED를 연결한 핀 번호를 정의합니다.
const int ledPin1 = A5; 
const int ledPin2 = 8;

void setup() {
  // LED 핀을 출력으로 설정합니다.
  pinMode(ledPin1, OUTPUT);     
  pinMode(ledPin2, OUTPUT);     
}

void loop() {
  digitalWrite(ledPin1, HIGH);   // LED를 켭니다.
  digitalWrite(ledPin2, HIGH);
  delay(1000);                  // 1초 동안 유지합니다.
  digitalWrite(ledPin1, LOW);    // LED를 끕니다.
  digitalWrite(ledPin2, LOW);
  delay(1000);                  // 1초 동안 유지합니다.
}



// //아날로그 핀 예제
// const int sensorPin = A5; // 전위차계 연결 핀
// const int ledPin = 8;     // LED 연결 핀

// void setup() {
//   pinMode(sensorPin, INPUT); // 센서 핀을 입력으로 설정
//   pinMode(ledPin, OUTPUT);   // LED 핀을 출력으로 설정
// }

// void loop() {
//   // 센서에서 값을 읽음
//   int sensorValue = analogRead(sensorPin);

//   // LED를 켬
//   digitalWrite(ledPin, HIGH);
//   // sensorValue 밀리초 동안 대기
//   delay(sensorValue);

//   // LED를 끔
//   digitalWrite(ledPin, LOW);
//   // sensorValue 밀리초 동안 다시 대기
//   delay(sensorValue);
// }
