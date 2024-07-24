void setup() {
    Serial.begin(9600);  // 시리얼 통신 시작, 115200 bps로 설정
    Serial.println("Enter text:");
}

void loop() {
    // 시리얼 모니터에서 데이터가 들어오는지 확인
    if (Serial.available() > 0) {
        // 시리얼 모니터로부터 입력받은 데이터를 문자열로 읽음
        String input = Serial.readString();

        // 입력받은 데이터를 시리얼 모니터에 출력
        Serial.print("You entered: ");
        Serial.println(input);
    }
}
