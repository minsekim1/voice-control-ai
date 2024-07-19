#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

/*
BLE 디바이스를 초기화하고, "MyESP32"라는 이름으로 BLE 서버를 생성합니다.
- UUID를 사용하여 BLE 서비스와 BLE 특성을 생성합니다. 
  이 예제에서는 서비스 UUID와 특성 UUID를 사용합니다.
- BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE 옵션을 사용하여 
  해당 특성이 읽기와 쓰기 모두 가능하도록 설정합니다.
- MyCallbacks 클래스를 통해 특성에 쓰기 작업이 발생할 때마다 호출될 콜백 함수를 설정합니다. 
  콜백 함수 내에서는 새로 쓰여진 값이 시리얼 모니터에 출력됩니다.
- 서비스를 시작하고, BLE 광고를 시작하여 다른 BLE 디바이스들이 이 ESP32 서버를 찾고 연결할 수 
  있게 합니다. 이 코드를 ESP32에 업로드하면, ESP32가 BLE 서버로 동작하게 되고, 
  다른 BLE 디바이스(예: 스마트폰)를 사용하여 이 서버에 연결하고, 
  특성 값을 읽거나 새로운 값으로 쓸 수 있게 됩니다.
*/

// UUID를 생성하려면 다음을 참조하세요: https://www.uuidgenerator.net/
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class MyCallbacks: public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) {
    std::string value = pCharacteristic->getValue();

    if (value.length() > 0) {
      Serial.println("********");
      Serial.print("New Value: ");
      for (int i = 0; i < value.length(); i++)
        Serial.print(value[i]);

      Serial.println();
      Serial.println("********");
    }
  }
};

void setup() {
  Serial.begin(115200);

  BLEDevice::init("MyESP32");
  BLEServer *pServer = BLEDevice::createServer();

  BLEService *pService = pServer->createService(SERVICE_UUID);

  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
                                        CHARACTERISTIC_UUID,
                                        BLECharacteristic::PROPERTY_READ |
                                        BLECharacteristic::PROPERTY_WRITE
                                      );

  pCharacteristic->setCallbacks(new MyCallbacks());

  pCharacteristic->setValue("Hello World");
  pService->start();

  BLEAdvertising *pAdvertising = pServer->getAdvertising();
  pAdvertising->start();
}

void loop() {
  // 여기에는 반복 실행 코드가 없습니다.
  delay(2000);
}
