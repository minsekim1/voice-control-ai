import speech_recognition as sr

def recognize_speech(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        
    # 구글 음성 인식 서비스로 음성을 텍스트로 변환
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language='ko-KR')
        print("You said: {}".format(text))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(sample_rate=16000)

    while True:
        recognize_speech(recognizer, microphone)
