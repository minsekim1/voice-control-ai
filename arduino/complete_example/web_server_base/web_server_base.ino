#include <WiFi.h>
#include <WiFiAP.h>
#include <WiFiClient.h>

// 출처: https://blog.naver.com/sandcookie20/222006492830
// 와이파이의 ssid와 비밀번호 설정
const char *ssid = "yourAP";
const char *password = "yourPassword";
WiFiServer server(80);

void setup() {
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
            if (client.available()) {        // 만약 클라이언트에서 읽을 바이트가 있으면,
                char c = client.read();      // 그 바이트를 읽고,
                Serial.write(c);             // 그 읽은 바이트를 시리얼 모니터에 출력해줌.
                if (c == '\n') {             // 바이트가 줄 바꿈 문자일 경우

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

                // 클라이언트 요청이 "GET /H"인지 또는 "GET /L"인지 확인:
                if (currentLine.endsWith("GET /H")) {
                    Serial.println("HIGH");
                }
                if (currentLine.endsWith("GET /L")) {
                    Serial.println("LOW");
                }
            }
        }
        client.stop();
        Serial.println("Client Disconnected.");
    }
}