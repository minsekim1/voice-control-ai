# googleCloudSpeech.py
import pyaudio
from google.cloud import speech

class GoogleCloudSpeech:
    def __init__(self):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=24000,
            language_code="ko-KR",
            enable_automatic_punctuation=True,
            model="default",
            audio_channel_count=1,
            enable_word_confidence=True,
            enable_word_time_offsets=True
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True
        )
        self.audio_stream = None
        self.stream = None
        self.p = None

    def start_recognition(self):
        try:
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=24000, input=True, frames_per_buffer=1024)
            self.audio_stream = self.stream_generator(self.stream)
            requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in self.audio_stream)
            responses = self.client.streaming_recognize(self.streaming_config, requests)
            self.listen_print_loop(responses)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.stop_recognition()



    def stop_recognition(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            self.stream = None
            self.p = None
            self.audio_stream = None

    def stream_generator(self, stream):
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            yield data

    def listen_print_loop(self, responses):
        for response in responses:
            for result in response.results:
                print('Transcript: {}'.format(result.alternatives[0].transcript))
                if result.is_final:
                    print('Final transcript: {}'.format(result.alternatives[0].transcript))
