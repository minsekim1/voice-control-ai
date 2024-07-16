#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "ESP32-Access-Point";
const char* password = "12345678";
WebServer server(80);

const int ledPin = 2; // LED 핀 설정 (보드에 따라 핀 번호 확인)

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

  // Wi-Fi AP 모드 설정
  WiFi.softAP(ssid, password);

  Serial.println("Access Point Created");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot);
  server.on("/led/on", handleLEDOn);
  server.on("/led/off", handleLEDOff);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
