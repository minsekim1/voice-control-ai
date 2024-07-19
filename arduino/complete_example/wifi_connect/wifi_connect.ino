#include <WiFi.h>

const char* ssid = "KT_GiGA_CC39"; // 여러분의 WiFi 이름
const char* password = "4cf18fx940"; // 여러분의 WiFi 비밀번호

void setup() {
  Serial.begin(115200);
  delay(10);
  
  // WiFi 네트워크에 연결을 시작합니다.
  Serial.println();
  Serial.println();
  Serial.print("연결 중: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi 연결됨.");
  Serial.println("IP 주소: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // 여기에는 반복되는 코드가 없습니다.
}
