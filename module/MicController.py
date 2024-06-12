import audioop
import threading
import pyaudio
import time

class MicController:
    def __init__(self, threshold=500):
        self.p = pyaudio.PyAudio()
        self.threshold = threshold
        self.common_sample_rates = [8000, 16000, 22050, 44100, 48000]
        self.result = []

    def test_sample_rate(self, device_info, rate, i):
        try:
            if not self.p.is_format_supported(rate,
                                              input_device=device_info['index'],
                                              input_channels=1,
                                              input_format=pyaudio.paInt16):
                print(f"Sample rate {rate} Hz not supported by {device_info['name']}")
                return  # 지원하지 않는 샘플 레이트는 테스트하지 않음
        except ValueError as e:
            return  # 에러 발생 시, 다음 샘플 레이트로 넘어감

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

            if rms > self.threshold:
                self.result.append((device_info['name'], device_info['index'], rate, rms))
        except Exception as e:
            print(f"ERR: stream at [{i}]{rate}Hz:{str(e)} {device_info['name'][:20]}")

    def find_uniq_active_microphone(self):
        attempt = 0
        while attempt < 20:
            self.result = []
            num_devices = self.p.get_device_count()
            threads = []

            for i in range(num_devices):
                device_info = self.p.get_device_info_by_index(i)
                if not device_info['maxInputChannels'] > 0:
                    continue

                for rate in self.common_sample_rates:
                    thread = threading.Thread(target=self.test_sample_rate, args=(device_info, rate, i))
                    threads.append(thread)
                    thread.start()

            for thread in threads:
                thread.join()

            if self.result:
                sorted_results = sorted(self.result, key=lambda x: x[3], reverse=True)
                return sorted_results[0][0], sorted_results[0][1], sorted_results[0][2]  # 반환: 마이크 이름, 인덱스, 샘플 레이트

            time.sleep(0.3)
            attempt += 1

        self.terminate()
        return None, None, None

    def terminate(self):
        self.p.terminate()