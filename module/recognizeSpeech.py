import sys
import speech_recognition as sr

def recognizeSpeech(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    # 구글 음성 인식 서비스로 음성을 텍스트로 변환
    try:
        # print("Recognizing...")
        text = recognizer.recognize_google(audio, language='ko-KR')
        print("You said: {}".format(text))
        
        # 특정 명령어가 텍스트에 포함되어 있으면 프로그램 종료
        exit_commands = ["나가기", "종료", "닫기", "끄기", "꺼 줘"]
        for command in exit_commands:
            if command in text:
                print("Exiting program as per the command.")
                sys.exit()
            
    # except sr.UnknownValueError:
    #     print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        # print("Could not request results from Google Speech Recognition service; {0}".format(e))
        print("No message")
        

def sttStart():
		recognizer = sr.Recognizer()
		microphone = sr.Microphone(sample_rate=16000)
		print("Listening...")
		
		while True:
				recognizeSpeech(recognizer, microphone)