# googleCloudSpeech.py
import io
from google.cloud import speech

class GoogleCloudSpeech:
    def __init__(self):
        self.client = speech.SpeechClient()

    def transcribe_audio(self, audio_file_path):
        with io.open(audio_file_path, 'rb') as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code='en-US'
        )

        response = self.client.recognize(config=config, audio=audio)

        return response

    def get_transcription(self, audio_file_path):
        response = self.transcribe_audio(audio_file_path)

        transcripts = []
        for result in response.results:
            transcripts.append(result.alternatives[0].transcript)
            print('Transcript: {}'.format(result.alternatives[0].transcript))

        return transcripts
