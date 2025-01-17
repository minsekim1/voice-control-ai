#include <Preferences.h>
#include <WiFi.h>
#include <WiFiAP.h>
#include <WiFiClient.h>

const int pin8 = 8;  // GPIO 2 핀 사용

// 와이파이의 ssid와 비밀번호 설정
const char *ssid = "espBoard";
const char *password = "espBoard123";
WiFiServer server(80);
Preferences preferences;  // Preferences 객체 생성

void setup() {
    pinMode(pin8, OUTPUT);

    Serial.begin(115200);
    Serial.println();
    Serial.println("Configuring access point...");
    // 혼합 모드로 설정: 스테이션 + 액세스 포인트 모드
    WiFi.mode(WIFI_AP_STA);
    WiFi.softAP(ssid, password);
    IPAddress myIP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(myIP);
    server.begin();
    Serial.println("Server started");

#pragma region 저장된 와이파이 ssid/pw 가져오기
    // Preferences에서 저장된 Wi-Fi 정보 불러오기
    preferences.begin("wifi-config", true);  // 읽기 모드로 열기
    String saved_ssid = preferences.getString("ssid", "");
    String saved_password = preferences.getString("password", "");
    preferences.end();

    if (saved_ssid != "" && saved_password != "") {
        // 저장된 Wi-Fi 정보가 있다면 스테이션 모드로 연결 시도
        Serial.println("Attempting to connect to saved Wi-Fi...");
        WiFiClient client = server.available();
        connectToWiFi(client, saved_ssid, saved_password);
    }
#pragma endregion
}

void loop() {
    WiFiClient client = server.available();  // 클라이언트 접속 감지
    if (client) {                            // 만약 클라이언트가 감지되면
        Serial.println("New Client.");       // 클라이언트 연결 메시지 출력
        char buffer[300];                    // 데이터를 저장할 버퍼 선언 (300바이트 크기)
        int length;                          // 읽어들인 데이터의 길이를 저장할 변수
        bool requestHandled = false;         // 요청이 처리되었는지 여부를 체크하는 플래그

        while (client.connected() && !requestHandled) {  // 클라이언트가 연결되어 있는 동안, 요청 처리 전까지
            if (client.available()) {                    // 클라이언트에서 데이터를 읽을 준비가 되었으면
                // 캐리지 리턴('\r') 문자가 나올 때까지 데이터를 읽고 버퍼에 저장
                length = client.readBytesUntil('\n', buffer, sizeof(buffer) - 1);
                buffer[length] = 0;               // 읽어들인 데이터를 문자열로 처리하기 위해 마지막에 널 문자 추가
                String request = String(buffer);  // 버퍼 내용을 String 객체로 변환
                Serial.println(request);          // 클라이언트 요청을 시리얼 모니터에 출력

                // HTTP 요청의 끝은 빈 줄로 표시되므로, 요청이 끝났으면 응답을 보냄
                if (request.indexOf(" HTTP/") || request == "\r") {
                    // HTTP 응답 헤더
                    client.println("HTTP/1.1 200 OK");
                    client.println("Content-type:text/html");
                    client.println("");

#pragma region 응답 처리
                    if (request.indexOf("GET /on") >= 0) {
                        digitalWrite(pin8, LOW);  // LED 켜기
                        Serial.println("LED ON");

                        // HTTP 응답의 내용
                        client.print("<p>LED on complete</p>");
                        client.print("Click <a href=\"/\">here</a> to commands list<br/>");
                    } else if (request.indexOf("GET /off") >= 0) {
                        digitalWrite(pin8, HIGH);  // LED 끄기
                        Serial.println("LED OFF");

                        // HTTP 응답의 내용
                        client.print("<p>LED off complete</p>");
                        client.print("Click <a href=\"/\">here</a> to commands list<br/>");
                    } else if (request.indexOf("GET /wifi") >= 0) {
                        Serial.println("Wifi connect");

                        // 1. SSID와 Password 추출
                        String ssid = request.substring(request.indexOf("ssid=") + 5, request.indexOf("&"));
                        String password = request.substring(request.indexOf("password=") + 9, request.indexOf(" ", request.indexOf("password=")));
                        Serial.print("SSID: ");
                        Serial.println(ssid);
                        Serial.print("Password: ");
                        Serial.println(password);

                        // 2. SSID 체크
                        bool isSSID = isSSIDAvailable(ssid);
                        if (isSSID) {
                            // client.print("<p>wifi connect complete</p>");
                            connectToWiFi(client, ssid, password);
                        } else {
                            client.print("<p>no wifi name (cannot find ssid)</p>");
                        }

                        // HTTP 응답의 내용
                        client.print("Click <a href=\"/\">here</a> to commands list<br/>");
                    } else {
                        // HTTP 응답의 내용
                        client.print("Click <a href=\"/on\">here</a> to turn ON the LED.<br/>");
                        client.print("Click <a href=\"/off\">here</a> to turn OFF the LED.<br/>");
                        client.print("Click <a href=\"/wifi?ssid=MIN_2G&password=4cf18fx940\">here</a> to connect wifi.<br/>");
                    }
#pragma endregion

                    requestHandled = true;  // 요청이 처리되었음을 표시
                }
            }
        }
        // 클라이언트 연결 종료
        client.stop();
        Serial.println("Client Disconnected.");
    }
}

// 입력받은 SSID가 주변에 있는지 확인하는 함수
bool isSSIDAvailable(String ssid) {
    WiFi.disconnect(true);  // 이전 연결 및 캐싱된 정보 모두 삭제
    WiFi.scanDelete();      // 이전 스캔 결과 삭제
    delay(1000);            // 약간의 지연 시간 후에 스캔 시작

    Serial.println("Scanning for available networks...");
    int numNetworks = WiFi.scanNetworks();  // Wi-Fi 네트워크 스캔

    for (int i = 0; i < numNetworks; i++) {
        Serial.println("Scanning for available networks..." + ssid);
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
    // 연결을 시도하기 전에 WiFi 상태를 초기화
    WiFi.disconnect(true);  // 이전 연결 및 캐싱된 정보 모두 삭제
    delay(1000);            // 약간의 지연을 줘서 네트워크 모듈이 리셋될 시간을 확보

    Serial.println("Attempting to connect to Wi-Fi...");
    WiFi.begin(ssid.c_str(), password.c_str());  // 입력받은 SSID와 비밀번호로 연결 시도

    int attempts = 0;                                        // 연결 시도 횟수 제한을 위한 변수
    while (WiFi.status() != WL_CONNECTED && attempts < 3) {  // 최대 3번 시도
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
        // WiFi.softAPdisconnect(true);
        // Serial.println("AP mode stopped.");

        // SSID 및 비밀번호를 Preferences에 저장
        preferences.begin("wifi-config", false);  // 쓰기 모드로 열기
        preferences.putString("ssid", ssid);
        preferences.putString("password", password);
        preferences.end();

        // HTML 반환 : wifi connected
        client.print("<p>wifi connected.</p><br/>");
    } else {
        Serial.println("");
        Serial.println("Failed to connect to Wi-Fi during 3 seconds");

        // HTML 반환 : wifi not connected
        client.print("<p>wifi not connected. please check the password.</p><br/>");

        // WiFi 상태 초기화 후 AP 모드로 돌아갈 수 있게 재설정
        WiFi.disconnect();  // 비밀번호가 틀렸을 경우 연결 해제
        delay(1000);        // 네트워크 재설정을 위한 지연
    }
}
