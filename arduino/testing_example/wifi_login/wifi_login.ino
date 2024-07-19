#include <WiFiManager.h>  // WiFiManager 라이브러리 포함

// 웹 서버를 위한 라이브러리 포함
#include <WebServer.h>

const int ledPin = 8;  // LED 핀 번호
WebServer server(80);  // 웹 서버 포트 설정

void handleRoot() {
  server.send(200, "text/html", "<h1>ESP32 LED Control</h1><button onclick=\"fetch('/ledon')\">LED ON</button><button onclick=\"fetch('/ledoff')\">LED OFF</button>");
}

void handleLedOn() {
  digitalWrite(ledPin, LOW);  // LED 켜기 (반대로 동작)
  server.send(200, "text/html", "LED is ON");
}

void handleLedOff() {
  digitalWrite(ledPin, HIGH);  // LED 끄기 (반대로 동작)
  server.send(200, "text/html", "LED is OFF");
}

void handleNotFound() {
  server.send(404, "text/plain", "Not found");
}

void setup() {
  // 시리얼 포트 시작
  Serial.begin(115200);

  // LED 핀 설정
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);  // LED를 끈 상태로 초기화 (반대로 동작)

  // WiFiManager 초기화
  WiFiManager wifiManager;

  // 이전 설정을 재설정하려면 아래 줄의 주석을 해제합니다.
  // wifiManager.resetSettings();

  // Captive 포털 실행
  if (!wifiManager.autoConnect("ESP32-AP")) {
    Serial.println("Failed to connect and hit timeout");
    // 재부팅
    ESP.restart();
  }

  // Wi-Fi 연결 완료
  Serial.println("Connected to Wi-Fi");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // 웹 서버 경로 설정
  server.on("/", handleRoot);
  server.on("/ledon", handleLedOn);
  server.on("/ledoff", handleLedOff);
  server.onNotFound(handleNotFound);

  // 웹 서버 시작
  server.begin();
}

void loop() {
  // 웹 서버 클라이언트 처리
  server.handleClient();
}
