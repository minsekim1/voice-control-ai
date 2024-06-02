import pyaudio
import wave

class AudioRecorder:
    def __init__(self, filename="output.wav", format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024, input_device_index=None):
        self.filename = filename
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.input_device_index = input_device_index
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []

    def get_inputs_list(self):
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        input_devices = []

        for i in range(0, numdevices):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') > 0:
                input_devices.append({
                    "index": i,
                    "name": device_info.get('name')
                })
                print(f"Input Available Device {i}: {device_info.get('name')}, Input Channels: {device_info.get('maxInputChannels')}")

        p.terminate()
        return input_devices
            
    def start_recording(self):
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      input_device_index=self.input_device_index,
                                      frames_per_buffer=self.chunk)
        self.frames = []
        print("Recording started")

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        print(f"Recording stopped, saved to {self.filename}")

    def record_chunk(self):
        data = self.stream.read(self.chunk)
        self.frames.append(data)
