import io
from google.cloud import speech
from google.oauth2 import service_account

class GoogleCloudSpeech:
    def __init__(self, credentials_path):
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = speech.SpeechClient(credentials=credentials)

    def transcribe_audio(self, audio_file_path):
        with io.open(audio_file_path, 'rb') as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code='ko-KR'
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
