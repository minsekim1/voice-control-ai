#include <WiFi.h>
#include <ESPAsyncWebSrv.h> // ESPAsyncWebSrv 라이브러리 포함
#include <Preferences.h>

const char* ap_ssid = "ESP32-AP";
const char* ap_password = "12345678";

AsyncWebServer server(80);

const int AlertLedPin = 8;
bool isConnected = false;
int networkCheckCount = 0;

Preferences preferences;

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

void handlePinControl(AsyncWebServerRequest *request) {
    if (!isConnected) {
        request->send(200, "text/plain", "please, connect to wifi.");
        return;
    }
    
    String pinNumber = request->arg("pin");
    String value = request->arg("value");
    String response = "Pin " + pinNumber + " set to " + value;
    Serial.println(response);

    if (pinNumber.length() == 0 || value.length() == 0) {
        request->send(200, "text/plain", "please, enter pin and value.");
        Serial.println("handlePinControl failed.");
        return;
    }
    Serial.println("handlePinControl success.");

    int pin = pinNumber.toInt();
    int val = value.toInt();

    pinMode(pin, OUTPUT);
    digitalWrite(pin, val);
    
    request->send(200, "text/plain", response);
}

void handleSave(AsyncWebServerRequest *request) {
    String ssid = request->arg("ssid");
    String password = request->arg("password");

    if (ssid.length() == 0 || password.length() == 0) {
        request->send(200, "text/plain", "please, enter SSID and wifi password.");
        return;
    }

    preferences.begin("wifi", false);
    preferences.putString("ssid", ssid);
    preferences.putString("password", password);
    preferences.end();

    request->send(200, "text/plain", "save completed! restart device...");

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid.c_str(), password.c_str());

    int attempt = 0;
    while (WiFi.status() != WL_CONNECTED && attempt < 5) {
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
        request->send(200, "text/plain", "WiFi 연결 실패. SSID와 비밀번호를 확인하세요.");
    }
}

void handleNetworkStatus(AsyncWebServerRequest *request) {
    if (WiFi.status() == WL_CONNECTED) {
      networkCheckCount++;
      Serial.println("WiFi 연결 성공 반환");
      Serial.println(networkCheckCount);
        request->send(200, "text/plain", "true");
    } else {
        Serial.println("WiFi 연결 실패 반환");
        request->send(200, "text/plain", "false");
    }
}

void setup() {
    Serial.begin(115200);

    pinMode(AlertLedPin, OUTPUT);
    digitalWrite(AlertLedPin, LOW);

    WiFi.softAP(ap_ssid, ap_password);
    Serial.println("액세스 포인트 모드 설정 완료");
    Serial.print("IP 주소: ");
    Serial.println(WiFi.softAPIP());

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
            Serial.println("saved password:");
            Serial.println(saved_password);
        }
    }

    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
        String currentSSID = WiFi.SSID();
        String pageContent = String(html);
        if (WiFi.status() == WL_CONNECTED) {
            pageContent = "<p>Already connected to '" + currentSSID + "'</p>" + pageContent;
        }
        request->send(200, "text/html", pageContent);
    });

    server.on("/save", HTTP_GET, handleSave);
    server.on("/pin/control", HTTP_GET, handlePinControl);
    server.on("/network/status", HTTP_GET, handleNetworkStatus);

    server.begin();
    Serial.println("웹 서버 시작");
}

void loop() {
    // No need to handle clients manually, AsyncWebServer does this automatically
}
