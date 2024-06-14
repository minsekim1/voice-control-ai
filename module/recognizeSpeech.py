import os
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
        exitProgram(text)

				# 메모장 키기
        exit_commands = ["메모장"]
        for command in exit_commands:
            if command in text:
                print("메모장 프로그램을 실행합니다.")
                os.system("notepad.exe")
            
    except Exception as e:
        print("No message")
        
# STT 서비스 시작하기
def sttStart():
		recognizer = sr.Recognizer()
		microphone = sr.Microphone(sample_rate=16000)
		print("Listening...")
		
		while True:
				recognizeSpeech(recognizer, microphone)
                            

# 특정 명령어가 텍스트에 포함되어 있으면 프로그램 종료
def exitProgram(text):
		exit_commands = ["나가기", "종료", "닫기", "끄기", "꺼 줘"]
		for command in exit_commands:
				if command in text:
						print("프로그램을 종료합니다.")
						sys.exit()