#include <WiFi.h>
#include <WiFiAP.h>
#include <WiFiClient.h>

const int pin8 = 8;  // GPIO 2 핀 사용

// 와이파이의 ssid와 비밀번호 설정
const char *ssid = "espBoard";
const char *password = "espBoard123";
WiFiServer server(80);

// 사용자가 입력한 Wi-Fi 네트워크 정보
String inputSSID = "";
String inputPassword = "";

void setup() {
    pinMode(pin8, OUTPUT);

    Serial.begin(115200);
    Serial.println();
    Serial.println("Configuring access point...");
    WiFi.softAP(ssid, password);
    IPAddress myIP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(myIP);
    server.begin();
    Serial.println("Server started");
}

void loop() {
    WiFiClient client = server.available();  // 접속 감지
    if (client) {                            // 만약 사용자가 감지되면,
        Serial.println("New Client.");       // 시리얼 포트에 메시지 출력
        String currentLine = "";             // 클라이언트에서 들어오는 데이터를 저장할 문자열 만듦
        while (client.connected()) {         // 사용자가 연결되어 있는 동안 무한 루프
            if (client.available()) {
                char c = client.read();  // 그 바이트를 읽고,
                                         // Serial.write(c);          // 클라이언트의 응답을 시리얼 모니터에 출력해줌.
                if (c == '\n') {         // 바이트가 줄 바꿈 문자일 경우

                    // 현재 행이 비어 있는 경우, 두 개의 새 행 문자를 연속해서 입력
                    // 클라이언트 HTTP 요청의 끝인 경우, 응답을 보냄
                    if (currentLine.length() == 0) {
                        // HTTP 헤더는 항상 응답 코드(예: HTTP/1.1 200 확인)로 시작함
                        // 고객이 무엇이 올지 알 수 있도록 컨텐츠 유형을 선택한 후 다음 빈 줄:
                        client.println("HTTP/1.1 200 OK");
                        client.println("Content-type:text/html");
                        client.println();

                        // HTTP 응답의 내용은 헤더를 따른다:
                        client.print("Click <a href=\"/H\">here</a> to turn ON the LED.<br>");
                        client.print("Click <a href=\"/L\">here</a> to turn OFF the LED.<br>");

                        // HTTP 응답이 다른 빈 행으로 끝나는 경우:
                        client.println();
                        // break out of the while loop:
                        break;
                    } else {  // 새 회선이 있으면 current line 삭제:
                        currentLine = "";
                    }
                } else if (c != '\r') {  // 리턴 문자 말고 다른 것이 있으면
                    currentLine += c;    // currentLine의 끝에 추가함
                }

                // 클라이언트 요청이 "GET /wifi?ssid=xxx&password=xxx"로 시작하는지 확인:
                if (currentLine.endsWith("GET /wifi")) {
                    // SSID와 패스워드를 추출하여 저장
                    int ssidStart = currentLine.indexOf('=') + 1;
                    int ssidEnd = currentLine.indexOf('&');
                    inputSSID = currentLine.substring(ssidStart, ssidEnd);

                    int passwordStart = currentLine.indexOf("password=") + 9;
                    int passwordEnd = currentLine.indexOf(' ', passwordStart);
                    inputPassword = currentLine.substring(passwordStart, passwordEnd);

                    Serial.print("Received SSID: ");
                    Serial.println(inputSSID);
                    Serial.print("Received Password: ");
                    Serial.println(inputPassword);

                    // 입력된 SSID와 비밀번호를 검증
                    if (isSSIDAvailable(inputSSID)) {
                        connectToWiFi(client, inputSSID, inputPassword);  // Wi-Fi 연결 시도
                    } else {
                        Serial.println("SSID not found.");

                        // HTML 반환 : SSID not found
                        client.println("HTTP/1.1 200 OK");
                        client.println("Content-type:text/html");
                        client.print("<p>SSID not found.</p><br/>");
                    }
                }

                // 클라이언트 요청이 "GET /H"인지 또는 "GET /L"인지 확인:
                else if (currentLine.endsWith("GET /H")) {
                    digitalWrite(pin8, HIGH);  // turn on the LED
                    Serial.println("HIGH");

                    // HTML 반환 : LED OFF
                    client.println("HTTP/1.1 200 OK");
                    client.println("Content-type:text/html");
                    client.print("<p>LED OFF complete.</p><br/>");
                    client.print("Click <a href=\"/H\">here</a> to turn ON the LED.<br/>");
                    client.print("Click <a href=\"/L\">here</a> to turn OFF the LED.<br/>");
                } else if (currentLine.endsWith("GET /L")) {
                    digitalWrite(pin8, LOW);  // turn off the LED
                    Serial.println("LOW");

                    // HTML 반환 : LED OFF
                    client.println("HTTP/1.1 200 OK");
                    client.println("Content-type:text/html");
                    client.print("<p>LED OFF complete.</p><br/>");
                    client.print("Click <a href=\"/H\">here</a> to turn ON the LED.<br/>");
                    client.print("Click <a href=\"/L\">here</a> to turn OFF the LED.<br/>");
                } else {
                    // HTML 반환 : 기본
                    client.println("HTTP/1.1 200 OK");
                    client.println("Content-type:text/html");
                    // 웹 페이지 제공 (SSID와 비밀번호 입력 폼)
                    client.println("Click <a href=\"/wifi?ssid=MIN_2G&password=4cf18fx940\">here</a> to turn ON the LED.<br/>");
                    // HTTP 응답의 내용은 헤더를 따른다:
                    client.print("Click <a href=\"/H\">here</a> to turn ON the LED.<br/>");
                    client.print("Click <a href=\"/L\">here</a> to turn OFF the LED.<br/>");
                }
            }
        }
        client.stop();
        Serial.println("Client Disconnected.");
    }
}

// 입력받은 SSID가 주변에 있는지 확인하는 함수
bool isSSIDAvailable(String ssid) {
    Serial.println("Scanning for available networks...");
    int numNetworks = WiFi.scanNetworks();  // Wi-Fi 네트워크 스캔
    for (int i = 0; i < numNetworks; i++) {
        if (WiFi.SSID(i) == ssid) {  // 입력된 SSID가 존재하는지 확인
            Serial.print("Found SSID: ");
            Serial.println(ssid);
            return true;
        }
    }
    Serial.println("SSID not found.");
    return false;
}

// 클라이언트 모드로 전환하여 Wi-Fi 네트워크에 연결하는 함수
void connectToWiFi(WiFiClient client, String ssid, String password) {
    Serial.println("Attempting to connect to Wi-Fi...");
    WiFi.begin(ssid.c_str(), password.c_str());  // 입력받은 SSID와 비밀번호로 연결 시도

    int attempts = 0;                                         // 연결 시도 횟수 제한을 위한 변수
    while (WiFi.status() != WL_CONNECTED && attempts < 10) {  // 최대 10번 시도
        delay(1000);
        Serial.print(".");
        attempts++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("");
        Serial.println("WiFi connected.");
        Serial.println("IP address: ");
        Serial.println(WiFi.localIP());

        // Wi-Fi 연결에 성공한 후에 AP 모드 종료
        WiFi.softAPdisconnect(true);
        Serial.println("AP mode stopped.");

        // HTML 반환 : wifi connected
        client.println("HTTP/1.1 200 OK");
        client.println("Content-type:text/html");
        client.print("<p>wifi connected.</p><br/>");
    } else {
        Serial.println("");
        Serial.println("Failed to connect to Wi-Fi after 10 attempts.");

        // HTML 반환 : wifi not connected
        client.println("HTTP/1.1 200 OK");
        client.println("Content-type:text/html");
        client.print("<p>wifi not connected.</p><br/>");
    }
}