import sys
import threading
import time
sys.path.insert(0, './module')
from catch_voice import execute_command
from stt import stt_start
from offline_stt import offline_stt_start

def main():
    # 온라인 STT 스레드 시작
    online_thread = threading.Thread(target=stt_start)
    online_thread.daemon = True
    online_thread.start()
    
    # 오프라인 STT 스레드 시작
    offline_thread = threading.Thread(target=offline_stt_start)
    offline_thread.daemon = True
    offline_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
        sys.exit(0)

if __name__ == "__main__":
    main()



# execute_command("화면 밝기")
# execute_command("80")