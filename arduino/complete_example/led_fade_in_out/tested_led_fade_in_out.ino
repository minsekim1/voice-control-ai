//디지털 PWM 예제
//define led according to pin diagam
int ledPin = 8;

void setup() {
  // put your setup code here, to run once:
  pinMode(ledPin, OUTPUT);  
}

void loop() {
  //5 포인트 단위로 최소에서 최대로 페이드인
  for(int fadeValue = 0; fadeValue <= 255; fadeValue += 5){
    analogWrite(ledPin, fadeValue);
    delay(30);
  }
  //5 포인트 단위로 최소에서 최대로 페이드아웃
  for(int fadeValue = 255; fadeValue >= 0; fadeValue -= 5){
    analogWrite(ledPin, fadeValue);
    delay(30);
  }
}
