#include <WiFi.h>
#include <WebServer.h>

// Wi-Fi 네트워크 이름과 비밀번호 설정
const char* ssid = "KT_GiGA_5G_CC39";
const char* password = "4cf18fx940";

// 웹 서버 포트 설정
WebServer server(80);

// LED 핀 설정
const int ledPin = 8; // GPIO 2 핀 사용

void handleRoot() {
  server.send(200, "text/plain", "Hello, you can control the LED by visiting /led/on or /led/off");
}

void handleLEDOn() {
  digitalWrite(ledPin, HIGH);
  server.send(200, "text/plain", "LED is ON");
}

void handleLEDOff() {
  digitalWrite(ledPin, LOW);
  server.send(200, "text/plain", "LED is OFF");
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  // Wi-Fi 연결 설정
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi...");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected!");

  // 웹 서버 엔드포인트 설정
  server.on("/", handleRoot);
  server.on("/led/on", handleLEDOn);
  server.on("/led/off", handleLEDOff);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
