import sys
sys.path.insert(0, './module')

from MicController import MicController
import speech_recognition as sr

micController = MicController()
mic, index = micController.find_uniq_active_microphone()
if mic:
    print(f"Most likely active microphone: {mic} at index {index}")
else:
    print("No active microphone found.")

# 음성 인식 시작
if mic:
    try:
        with sr.Microphone(device_index=index) as source:
            print("Listening...")
            audio = micController.recognizer.listen(source)
            print("Recognizing...")
            text = micController.recognizer.recognize_google(audio)
            print("You said:", text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))