#include "WiFi.h"

void setup() {
  Serial.begin(115200);
  
  // WiFi를 스테이션 모드로 설정하고, 이전에 연결된 경우 AP에서 연결을 끊습니다.
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  
  Serial.println("Setup 완료");
}

void loop() {
  Serial.println("스캔 시작...");
  
  // WiFi.scanNetworks는 발견된 네트워크 수를 반환합니다.
  int n = WiFi.scanNetworks();
  Serial.println("스캔 완료");
  if (n == 0) {
    Serial.println("네트워크를 찾을 수 없음");
  } else {
    Serial.print(n);
    Serial.println(" 네트워크 발견");
    for (int i = 0; i < n; ++i) {
      // 찾은 각 네트워크에 대해 SSID와 RSSI를 출력합니다.
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN) ? " " : "*");
      delay(10);
    }
  }
  Serial.println("");

  // 다시 스캔하기 전에 잠시 기다립니다.
  delay(5000);
}