int i = 0;  // 카운터 변수 초기화

void setup() {
    Serial.begin(115200);  // 시리얼 통신 시작, 115200 bps로 설정
}

void loop() {
    i++;                // 변수 i에 1씩 더함
    Serial.println(i);  // 변수 i의 값을 시리얼 모니터에 출력
    delay(1000);        // 1초 대기
}
