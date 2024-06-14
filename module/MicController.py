import tkinter as tk
from tkinter import ttk
import pyaudio
import audioop
import threading
import time
import speech_recognition as sr

class MicController:
    def __init__(self, threshold=500):
        self.p = pyaudio.PyAudio()
        self.recognizer = sr.Recognizer()
        self.threshold = threshold
        self.common_sample_rates = [8000, 16000, 22050, 44100, 48000]
        self.result = []

    def get_device_list(self):
        num_devices = self.p.get_device_count()
        devices = []
        for i in range(num_devices):
            device_info = self.p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                devices.append((device_info['name'], i))
        return devices

    def test_sample_rate(self, device_index, rate):
        try:
            stream = self.p.open(format=pyaudio.paInt16,
                                 channels=1,
                                 rate=rate,
                                 input=True,
                                 input_device_index=device_index,
                                 frames_per_buffer=1024)
            data = stream.read(1024)
            rms = audioop.rms(data, 2)
            stream.close()
            return rms
        except Exception as e:
            print(f"Failed to open stream at {rate} Hz: {str(e)}")
            return 0

    def get_volume(self, device_index):
        for rate in self.common_sample_rates:
            rms = self.test_sample_rate(device_index, rate)
            if rms > 0:
                return rms
        return 0

    def terminate(self):
        self.p.terminate()

class VolumeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Microphone Volume Monitor")
        self.mic_controller = MicController()

        self.device_list = self.mic_controller.get_device_list()
        self.selected_device = tk.StringVar(value=self.device_list[0][0])

        self.create_widgets()
        self.running = False

    def create_widgets(self):
        ttk.Label(self.root, text="Select Microphone:").grid(column=0, row=0, padx=10, pady=10)

        self.device_combobox = ttk.Combobox(self.root, textvariable=self.selected_device, state="readonly")
        self.device_combobox['values'] = [name for name, index in self.device_list]
        self.device_combobox.grid(column=1, row=0, padx=10, pady=10)

        self.start_button = ttk.Button(self.root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.grid(column=0, row=1, padx=10, pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop Monitoring", command=self.stop_monitoring, state="disabled")
        self.stop_button.grid(column=1, row=1, padx=10, pady=10)

        self.volume_label = ttk.Label(self.root, text="Volume: 0")
        self.volume_label.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

    def start_monitoring(self):
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="enabled")
        self.monitor_volume()

    def stop_monitoring(self):
        self.running = False
        self.start_button.config(state="enabled")
        self.stop_button.config(state="disabled")

    def monitor_volume(self):
        if self.running:
            device_index = next(index for name, index in self.device_list if name == self.selected_device.get())
            volume = self.mic_controller.get_volume(device_index)
            self.volume_label.config(text=f"Volume: {volume}")
            self.root.after(100, self.monitor_volume)

    def on_closing(self):
        self.mic_controller.terminate()
        self.root.destroy()


