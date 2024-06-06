import speech_recognition as sr

class PythonSpeechRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    # language: 'ko-KR' or 'en-US'
    def transcribe_audio(self, audio_file_path, language='ko-KR'):
        with sr.AudioFile(audio_file_path) as source:
            audio = self.recognizer.record(source)
        try:
            text = self.recognizer.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            return "Google Web Speech API could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Web Speech API; {e}"
