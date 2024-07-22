#include <WebServer.h>
#include <WiFi.h>

// 핫스팟 설정
const char* ap_ssid = "ESP32-AP";
const char* ap_password = "12345678";

// 웹 서버 포트 설정
WebServer server(80);

// WiFi 설정 페이지 HTML
const char* html = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
  <title>WiFi 설정</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <h1>WiFi 설정 페이지</h1>
  <form action="/save">
    SSID: <input type="text" name="ssid"><br>
    비밀번호: <input type="password" name="password"><br>
    <input type="submit" value="저장">
  </form>
</body>
</html>
)rawliteral";

// WiFi 설정을 저장하고 연결하는 함수
void handleSave() {
    String ssid = server.arg("ssid");
    String password = server.arg("password");

    if (ssid.length() > 0 && password.length() > 0) {
        server.send(200, "text/plain", "저장 완료! 장치를 재시작합니다...");

        // WiFi 연결 시도
        WiFi.mode(WIFI_STA);
        WiFi.begin(ssid.c_str(), password.c_str());

        // 연결 대기
        while (WiFi.status() != WL_CONNECTED) {
            delay(1000);
            Serial.print(".");
        }

        Serial.println("");
        Serial.println("WiFi 연결 완료!");
        Serial.println("IP 주소: ");
        Serial.println(WiFi.localIP());

        // 웹 서버 중지
        server.stop();
    } else {
        server.send(200, "text/plain", "SSID와 비밀번호를 입력해주세요.");
    }
}

// 초기화 함수
void setup() {
    Serial.begin(115200);

    // 액세스 포인트 모드 설정
    WiFi.softAP(ap_ssid, ap_password);
    Serial.println("액세스 포인트 모드 설정 완료");
    Serial.print("IP 주소: ");
    Serial.println(WiFi.softAPIP());

    // 웹 서버 라우팅 설정
    server.on("/", HTTP_GET, []() {
        server.send(200, "text/html", html);
    });
    server.on("/save", HTTP_GET, handleSave);
    server.begin();
    Serial.println("웹 서버 시작");
}

// 메인 루프
void loop() {
    server.handleClient();
}
