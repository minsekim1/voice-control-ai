#include <WebServer.h>
#include <WiFi.h>
#include <Preferences.h> // Preferences 라이브러리 포함

// 핫스팟 설정
const char* ap_ssid = "ESP32-AP";
const char* ap_password = "12345678";

// 웹 서버 포트 설정
WebServer server(80);

// LED 핀 설정
const int AlertLedPin = 8;
bool isConnected = false;

Preferences preferences; // Preferences 객체 생성

// WiFi 설정 페이지 HTML
const char* html = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
  <title>WiFi 설정</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta charset="UTF-8">
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

// 핀 제어 함수
void handlePinControl() {
    if (!isConnected) {
        server.send(200, "text/plain", "please, connect to wifi.");
        return;
    }
    
    String pinNumber = server.arg("pin");
    String value = server.arg("value");
    
    if (pinNumber.length() == 0 || value.length() == 0) {
        server.send(200, "text/plain", "please, enter pin and value.");
        return;
    }

    int pin = pinNumber.toInt();
    int val = value.toInt();

    pinMode(pin, OUTPUT); // 핀을 출력 모드로 설정
    digitalWrite(pin, val);

    String response = "Pin " + pinNumber + " set to " + value;
    server.send(200, "text/plain", response);
}

// WiFi 설정을 저장하고 연결하는 함수
void handleSave() {
    String ssid = server.arg("ssid");
    String password = server.arg("password");

    if (ssid.length() == 0 || password.length() == 0) {
        server.send(200, "text/plain", "please, enter SSID and wifi password.");
        return;
    }

    // SSID와 비밀번호를 Preferences에 저장
    preferences.begin("wifi", false);
    preferences.putString("ssid", ssid);
    preferences.putString("password", password);
    preferences.end();

    server.send(200, "text/plain", "save completed! restart device...");

    // WiFi 연결 시도
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid.c_str(), password.c_str());

    // 연결 대기
    int attempt = 0;
    while (WiFi.status() != WL_CONNECTED && attempt < 5) {  // 최대 5초 대기
        delay(1000);
        Serial.print(".");
        attempt++;
    }

    Serial.print("저장된 SSID: ");
    Serial.println(ssid);
    Serial.print("저장된 비밀번호: ");
    Serial.println(password);

    if (WiFi.status() == WL_CONNECTED) {
        isConnected = true;
        
        Serial.println("");
        Serial.println("WiFi 연결 완료!");

        Serial.println("IP 주소: ");
        Serial.println(WiFi.localIP());
        
    } else {
        Serial.println("WiFi 연결 실패");
        server.send(200, "text/plain", "WiFi 연결 실패. SSID와 비밀번호를 확인하세요.");
    }
}

// 초기화 함수
void setup() {
    Serial.begin(115200);

    // LED 핀 설정
    pinMode(AlertLedPin, OUTPUT);
    digitalWrite(AlertLedPin, LOW);  // LED 초기 상태를 OFF로 설정

    // 액세스 포인트 모드 설정
    WiFi.softAP(ap_ssid, ap_password);
    Serial.println("액세스 포인트 모드 설정 완료");
    Serial.print("IP 주소: ");
    Serial.println(WiFi.softAPIP());

    // 저장된 SSID와 비밀번호 불러오기
    preferences.begin("wifi", true);
    String saved_ssid = preferences.getString("ssid", "");
    String saved_password = preferences.getString("password", "");
    preferences.end();

    if (saved_ssid.length() > 0 && saved_password.length() > 0) {
        WiFi.mode(WIFI_STA);
        WiFi.begin(saved_ssid.c_str(), saved_password.c_str());

        int attempt = 0;
        while (WiFi.status() != WL_CONNECTED && attempt < 5) {
            delay(1000);
            Serial.print(".");
            attempt++;
        }

        if (WiFi.status() == WL_CONNECTED) {
            isConnected = true;
            Serial.println("");
            Serial.println("저장된 정보로 WiFi 연결 완료!");
            Serial.println("IP 주소: ");
            Serial.println(WiFi.localIP());
        } else {
            Serial.println("저장된 정보로 WiFi 연결 실패");
            Serial.println("saved Wifi ssid:");
            Serial.println(saved_ssid);
            Serial.println("saved passowrd:");
            Serial.println(saved_password);
            
        }
    }

    // 웹 서버 라우팅 설정
    server.on("/", HTTP_GET, []() {
        String currentSSID = WiFi.SSID();
        String pageContent = String(html);
        // WiFi가 이미 연결되어 있는 경우, 현재 연결된 WiFi 정보를 페이지의 맨 위에 표시
        if (WiFi.status() == WL_CONNECTED) {
            pageContent = "<p>Already connected to '" + currentSSID + "'</p>" + pageContent;
        }
        server.send(200, "text/html", pageContent);
    });
    
    server.on("/save", HTTP_GET, handleSave);
    server.on("/pin/control", HTTP_GET, handlePinControl);
    server.begin();
    Serial.println("웹 서버 시작");
}

// 메인 루프
void loop() {
    server.handleClient();
}
