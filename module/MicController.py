import pyaudio
import audioop
import time
import threading

# 활성 마이크 찾기
class MicController:
    def __init__(self, threshold=500):
        self.p = pyaudio.PyAudio()
        self.threshold = threshold
        self.common_sample_rates = [8000, 16000, 22050, 44100, 48000]
        self.result = []
        self.lock = threading.Lock()  # 스레드 간의 동시 접근 방지를 위한 락

    def test_sample_rate(self, device_info, rate):
        try:
            stream = self.p.open(format=pyaudio.paInt16,
                                 channels=1,
                                 rate=rate,
                                 input=True,
                                 input_device_index=device_info['index'],
                                 frames_per_buffer=1024)
            data = stream.read(1024)
            rms = audioop.rms(data, 2)
            stream.close()

            print(f"Volume for device {device_info['name']} at {rate} Hz: {rms}")

            if rms > self.threshold:
                with self.lock:  # 결과를 공유 리스트에 안전하게 추가
                    if not self.result or rms > self.result[0][2]:
                        self.result = [(device_info['name'], rate, rms)]
        except Exception as e:
            print(f"Failed to open stream at {rate} Hz: {str(e)}")

    def find_uniq_active_microphone(self):
        attempt = 0
        while attempt < 20: # 최대 반복횟수 설정 (20회=6초)
            self.result = []  # 결과 리스트를 리셋
            num_devices = self.p.get_device_count()
            threads = []

            for i in range(num_devices):
                device_info = self.p.get_device_info_by_index(i)
                if not device_info['maxInputChannels'] > 0:
                    continue

                for rate in self.common_sample_rates:
                    thread = threading.Thread(target=self.test_sample_rate, args=(device_info, rate))
                    threads.append(thread)
                    thread.start()

            for thread in threads:
                thread.join()

            if self.result:
                sorted_results = sorted(self.result, key=lambda x: x[2], reverse=True)
                return sorted_results[0][0], sorted_results[0][1]  # 가장 높은 볼륨을 가진 마이크와 레이트 반환

            time.sleep(0.3)
            attempt += 1

        self.terminate()
        return None, None

    def terminate(self):
        self.p.terminate()

# # 사용 예시
# tester = MicController()
# mic, rate = tester.find_uniq_active_microphone()
# if mic:
#     print(f"Most likely active microphone: {mic} at {rate} Hz")
# else:
#     print("No active microphone found.")

