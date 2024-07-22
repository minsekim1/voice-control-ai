#!/bin/bash

# 스크립트 사용 방법 출력
usage() {
  echo "Usage: $0 <port> <sketch_path>"
  echo "Example: $0 COM7 ./arduino/complete_example/wifi_connect"
  exit 1
}

# 인수 검증
if [ "$#" -ne 2 ]; then
  usage
fi

PORT=$1
SKETCH_PATH=$2

# 보드 이름 설정
BOARD_FQBN="esp32:esp32:esp32c3"

# 스케치 컴파일
echo "Compiling sketch at $SKETCH_PATH for board $BOARD_FQBN..."
arduino-cli compile --fqbn $BOARD_FQBN $SKETCH_PATH
if [ $? -ne 0 ]; then
  echo "Failed to compile sketch."
  exit 1
fi

# ESP32 보드로 업로드
echo "Uploading compiled sketch to board on port $PORT..."
arduino-cli upload -p $PORT --fqbn $BOARD_FQBN $SKETCH_PATH
if [ $? -ne 0 ]; then
  echo "Failed to upload sketch."
  exit 1
fi

echo "Sketch uploaded successfully."
