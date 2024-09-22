#include <Preferences.h>
#include <WiFi.h>
#include <WiFiAP.h>
#include <WiFiClient.h>
#include <ESP32Servo.h> // 서보 모터 제어를 위한 라이브러리

const int pin8 = 8;  // GPIO 2 핀 사용

// 와이파이의 ssid와 비밀번호 설정
const char *ssid = "espBoard";
const char *password = "espBoard123";
WiFiServer server(80);
Preferences preferences;  // Preferences 객체 생성


Servo myServo;  // Servo 객체 생성
const int servoPin = 2;  // 서보 신호 핀을 GPIO 2로 설정

void setup() {
    pinMode(0, OUTPUT); // START4x  curl --location 'http://172.30.1.6/pin?pin=0&value=on'
    pinMode(1, OUTPUT); // <<<<<5x  curl --location 'http://172.30.1.6/pin?pin=1&value=on'
    //pinMode(2, OUTPUT); // <<<<<6x  curl --location 'http://172.30.1.6/pin?pin=2&value=on'
    myServo.attach(servoPin);  // GPIO 2에 서보 모터 연결
    pinMode(3, OUTPUT); // <<<<<7x  curl --location 'http://172.30.1.6/pin?pin=3&value=on'
    pinMode(4, OUTPUT); // END  8x  curl --location 'http://172.30.1.6/pin?pin=4&value=on'
    pinMode(5, OUTPUT); // START1x  curl --location 'http://172.30.1.6/pin?pin=5&value=on'
    pinMode(6, OUTPUT); // >>>>>2o  curl --location 'http://172.30.1.6/pin?pin=6&value=on'
    pinMode(7, OUTPUT); // >>>>>3x  curl --location 'http://172.30.1.6/pin?pin=7&value=on'
    pinMode(8, OUTPUT); // >>>>>4o  curl --location 'http://172.30.1.6/pin?pin=8&value=on'
    pinMode(9, OUTPUT); // >>>>>5o  curl --location 'http://172.30.1.6/pin?pin=9&value=on'
    pinMode(10, OUTPUT);// >>>>>6x  curl --location 'http://172.30.1.6/pin?pin=10&value=on'
    pinMode(20, OUTPUT);// >>>>>7x  curl --location 'http://172.30.1.6/pin?pin=20&value=on'
    pinMode(21, OUTPUT);// END  8o  curl --location 'http://172.30.1.6/pin?pin=21&value=on'

    Serial.println("");
    Serial.begin(115200);
    Serial.println();
    Serial.print("[System] ");
    Serial.println("Configuring access point...");
    // 혼합 모드로 설정: 스테이션 + 액세스 포인트 모드
    WiFi.mode(WIFI_AP_STA);
    WiFi.softAP(ssid, password);
    IPAddress myIP = WiFi.softAPIP();
    Serial.print("[System] ");
    Serial.print("AP IP address: ");
    Serial.println(myIP);
    server.begin();
    Serial.print("[System] ");
    Serial.println("Server started");

#pragma region 저장된 와이파이 ssid/pw 가져오기
    // Preferences에서 저장된 Wi-Fi 정보 불러오기
    preferences.begin("wifi-config", true);  // 읽기 모드로 열기
    String saved_ssid = preferences.getString("ssid", "");
    String saved_password = preferences.getString("password", "");
    preferences.end();

    if (saved_ssid != "" && saved_password != "") {
        // 저장된 Wi-Fi 정보가 있다면 스테이션 모드로 연결 시도
        Serial.print("[System] ");
        Serial.println("Attempting to connect to saved Wi-Fi...");
        WiFiClient client = server.available();
        connectToWiFi(client, saved_ssid, saved_password);
    }
#pragma endregion

    Serial.println("");
}

void loop() {
    WiFiClient client = server.available();  // 클라이언트 접속 감지
    if (client) {                            // 만약 클라이언트가 감지되면
        Serial.print("[System] ");
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
                Serial.print(" >> ");
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
                      Serial.print(" >> ");
                      Serial.println("LED ON");

                      // HTTP 응답의 내용
                      client.print("<p>LED on complete</p>");
                      client.print("Click <a href=\"/\">here</a> to commands list<br/>");
                    } else if (request.indexOf("GET /off") >= 0) {
                      digitalWrite(pin8, HIGH);  // LED 끄기
                      Serial.print(" >> ");
                      Serial.println("LED OFF");

                      // HTTP 응답의 내용
                      client.print("<p>LED off complete</p>");
                      client.print("Click <a href=\"/\">here</a> to commands list<br/>");
                    } else if (request.indexOf("GET /wifi") >= 0) {
                      Serial.print(" >> ");
                      Serial.println("Wifi connect");

                      // 1. SSID와 Password 추출
                      String ssid = request.substring(request.indexOf("ssid=") + 5, request.indexOf("&"));
                      String password = request.substring(request.indexOf("password=") + 9, request.indexOf(" ", request.indexOf("password=")));
                      Serial.print(" >> ");
                      Serial.print("SSID: ");
                      Serial.println(ssid);
                      Serial.print(" >> ");
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
                    } else if (request.indexOf("GET /pin") >= 0) {
                      // 6, 9, 21번 핀만 되는듯
                      Serial.print(" >> ");
                      Serial.println("LED Pin control");

                      // 1. pin 번호와 value 추출
                      int pinNumber = request.substring(request.indexOf("pin=") + 4, request.indexOf("&")).toInt();
                      String pinValue = request.substring(request.indexOf("value=") + 6, request.indexOf(" ", request.indexOf("value=")));
                      
                      Serial.print(" >> ");
                      Serial.print("pinNumber: ");
                      Serial.println(pinNumber);
                      Serial.print(" >> ");
                      Serial.print("pinValue: ");
                      Serial.println(pinValue);

                      // 2. pinNumver & pinValue 체크
                      // bool isSSID = isSSIDAvailable(ssid);
                      // if (isSSID) {
                      //     // client.print("<p>wifi connect complete</p>");
                      //     connectToWiFi(client, ssid, password);
                      // } else {
                      //     client.print("<p>no wifi name (cannot find ssid)</p>");
                      // }

                      // 3. LED 컨트롤
                      if (pinValue == "on") {
                          digitalWrite(pinNumber, HIGH);  // LED 켜기
                          Serial.print(" >> ");
                          Serial.println("LED ON");

                          client.print("<p>LED on complete</p>");
                      } else if (pinValue == "off") {
                          digitalWrite(pinNumber, LOW);  // LED 끄기
                          Serial.print(" >> ");
                          Serial.println("LED OFF");

                          client.print("<p>LED off complete</p>");
                      } else {
                          Serial.print(" >> ");
                          Serial.println("Invalid value for pin control");
                          client.println("Invalid value! Use 'on' or 'off'.");
                      }

                      // HTTP 응답의 내용
                      client.print("Click <a href=\"/\">here</a> to commands list<br/>");
                    } else if (request.indexOf("GET /servo") >= 0) {
                      Serial.print(" >> ");
                      Serial.println("Servo control");

                      // 1. pin 번호와 value 추출
                      int angle = request.substring(request.indexOf("angle=") + 6, request.indexOf("&")).toInt();
                      
                      Serial.print(" >> ");
                      Serial.print("angle: ");
                      Serial.println(angle);

                      // 2. angle 체크
                      // bool isAvailableAngle = true
                      // if (isSSID) {
                      //     // client.print("<p>wifi connect complete</p>");
                      //     connectToWiFi(client, ssid, password);
                      // } else {
                      //     client.print("<p>no wifi name (cannot find ssid)</p>");
                      // }

                      // 3. LED 컨트롤
                      if (true) {
                          myServo.write(angle);
                          Serial.print(" >> ");
                          Serial.print("Servo at ");
                          Serial.print(angle);
                          Serial.println(" degrees");

                          client.print("<p>Servo move complete</p>");
                      } else {
                          Serial.print(" >> ");
                          Serial.println("Invalid value for pin control");
                          client.println("Invalid value! Use 'on' or 'off'.");
                      }

                      // HTTP 응답의 내용
                      client.print("Click <a href=\"/\">here</a> to commands list<br/>");
                    } else {
                      // HTTP 응답의 내용
                      client.print("Click <a href=\"/on\">here</a> to turn ON the LED.<br/>");
                      client.print("Click <a href=\"/off\">here</a> to turn OFF the LED.<br/>");
                      client.print("Click <a href=\"/wifi?ssid=MIN_2G&password=4cf18fx940\">here</a> to connect wifi.<br/>");
                      client.print("Click <a href=\"/pin?pin=8&value=on\">here</a> to trun on the LED.<br/>");
                      client.print("Click <a href=\"/servo?angle=90\">here</a> to trun 90 angle servo.<br/>");
                    }
#pragma endregion

                    requestHandled = true;  // 요청이 처리되었음을 표시
                }
            }
        }
        // 클라이언트 연결 종료
        client.stop();
        Serial.print("[System] ");
        Serial.println("Client Disconnected.");
        Serial.println("");
    }
}

// 입력받은 SSID가 주변에 있는지 확인하는 함수
bool isSSIDAvailable(String ssid) {
    WiFi.disconnect(true);  // 이전 연결 및 캐싱된 정보 모두 삭제
    WiFi.scanDelete();      // 이전 스캔 결과 삭제
    delay(1000);            // 약간의 지연 시간 후에 스캔 시작

    Serial.print(" >> ");
    Serial.println("Scanning for available networks...");
    int numNetworks = WiFi.scanNetworks();  // Wi-Fi 네트워크 스캔

    for (int i = 0; i < numNetworks; i++) {
        Serial.print(" >> ");
        Serial.println("Scanning for available networks..." + ssid);
        if (WiFi.SSID(i) == ssid) {  // 입력된 SSID가 존재하는지 확인
            Serial.print(" >> ");
            Serial.print("Found SSID: ");
            Serial.println(ssid);
            return true;
        }
    }
    Serial.print(" >> ");
    Serial.println("SSID not found.");
    return false;
}

// 클라이언트 모드로 전환하여 Wi-Fi 네트워크에 연결하는 함수
void connectToWiFi(WiFiClient client, String ssid, String password) {
    // 연결을 시도하기 전에 WiFi 상태를 초기화
    WiFi.disconnect(true);  // 이전 연결 및 캐싱된 정보 모두 삭제
    delay(1000);            // 약간의 지연을 줘서 네트워크 모듈이 리셋될 시간을 확보

    Serial.print(" >> ");
    Serial.println("Attempting to connect to Wi-Fi...");
    WiFi.begin(ssid.c_str(), password.c_str());  // 입력받은 SSID와 비밀번호로 연결 시도

    int attempts = 0;                                        // 연결 시도 횟수 제한을 위한 변수
    Serial.print(" >> ");
    while (WiFi.status() != WL_CONNECTED && attempts < 3) {  // 최대 3번 시도
        delay(1000);
        Serial.print(".");
        attempts++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("");
        Serial.print(" >> ");
        Serial.println("WiFi connected.");

        Serial.print(" >> ");
        Serial.print("IP address: ");
        Serial.println(WiFi.localIP());

        // Wi-Fi 연결에 성공한 후에 AP 모드 종료
        // WiFi.softAPdisconnect(true);
        // Serial.print(" >> ");
        // Serial.println("AP mode stopped.");

        // SSID 및 비밀번호를 Preferences에 저장
        preferences.begin("wifi-config", false);  // 쓰기 모드로 열기
        preferences.putString("ssid", ssid);
        preferences.putString("password", password);
        preferences.end();

        // HTML 반환 : wifi connected
        client.print("<p>wifi connected.</p><br/>");
    } else {
        Serial.print(" >> ");
        Serial.println("Failed to connect to Wi-Fi during 3 seconds");

        // HTML 반환 : wifi not connected
        client.print("<p>wifi not connected. please check the password.</p><br/>");

        // WiFi 상태 초기화 후 AP 모드로 돌아갈 수 있게 재설정
        WiFi.disconnect();  // 비밀번호가 틀렸을 경우 연결 해제
        delay(1000);        // 네트워크 재설정을 위한 지연
    }
}
