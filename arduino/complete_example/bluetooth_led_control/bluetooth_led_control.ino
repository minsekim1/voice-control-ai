#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>

#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

#define LED_PIN 8

class MyCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
        String value = pCharacteristic->getValue().c_str();

        if (value == "LED ON") {
            digitalWrite(LED_PIN, LOW);  // LED를 켭니다. (반대로 동작)
            Serial.println("LED ON");
        } else if (value == "LED OFF") {
            digitalWrite(LED_PIN, HIGH);  // LED를 끕니다. (반대로 동작)
            Serial.println("LED OFF");
        } else {
            Serial.println(value);  // String 타입을 직접 출력
        }
    }
};

void setup() {
    Serial.println("setup: bluetooth_led_control");
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);     // LED_PIN을 출력으로 설정합니다.
    digitalWrite(LED_PIN, HIGH);  // 초기 상태를 꺼짐으로 설정합니다.

    BLEDevice::init("MyESP32");
    BLEServer *pServer = BLEDevice::createServer();
    BLEService *pService = pServer->createService(SERVICE_UUID);
    BLECharacteristic *pCharacteristic = pService->createCharacteristic(
        CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_READ |
            BLECharacteristic::PROPERTY_WRITE);

    pCharacteristic->setCallbacks(new MyCallbacks());
    pCharacteristic->setValue("Hello World");
    pService->start();

    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);  // 광고에 서비스 UUID 추가
    pAdvertising->setScanResponse(true);         // 스캔 응답 사용
    pAdvertising->setMinPreferred(0x06);         // 최소 광고 시간
    pAdvertising->setMinPreferred(0x12);         // 최대 광고 시간
    BLEDevice::startAdvertising();               // 광고 시작
    Serial.println("Waiting for a client connection to notify...");
}

void loop() {
    // 이 예제에서는 loop 내용이 필요하지 않습니다.
    delay(2000);
}
