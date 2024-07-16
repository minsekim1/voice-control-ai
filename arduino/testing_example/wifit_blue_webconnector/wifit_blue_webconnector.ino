#include <WiFi.h>
#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

void connectToWiFi(const char* ssid, const char* password) {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_Bluetooth");

  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);

  Serial.println("Waiting for Bluetooth messages...");
}

void loop() {
  if (SerialBT.available()) {
    String input = SerialBT.readString();
    Serial.println("Received: " + input);

    int separatorIndex = input.indexOf(',');
    if (separatorIndex != -1) {
      String newSSID = input.substring(0, separatorIndex);
      String newPassword = input.substring(separatorIndex + 1);

      // Connect to the new WiFi
      connectToWiFi(newSSID.c_str(), newPassword.c_str());
    }
  }
}
