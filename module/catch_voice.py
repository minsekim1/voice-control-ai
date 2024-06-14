
import os
import subprocess
import sys
import pyautogui
import webbrowser  # 웹 브라우저를 제어하기 위한 모듈

# 최근 실행된 명령어를 저장
recent_commands = ""
last_commands = ""

# 음성인식을 진행합니다.
def execute_command(command):
    # 전역 변수 사용
    global last_commands  
    global recent_commands

    # 명령어가 최근 실행된 명령어 세트에 있는지 확인
    if command == recent_commands:
        return False
    
    # command가 last_commands로 시작하는 경우, 시작 부분 제거
    if command.startswith(last_commands):
        # last_commands 길이만큼 command에서 제거
        command = command[len(last_commands):].strip()

    # 음성 명령에 따라 특정 작업 수행
    if "메모장" in command:
        os.system("notepad")
    elif "유튜브" in command:
        webbrowser.open("https://www.youtube.com")
    elif "네이버" in command:
        webbrowser.open("https://www.naver.com")
    elif "구글" in command:
        webbrowser.open("https://www.google.com")
    elif "계산기" in command:
        os.system("calc")
    elif "스크린샷" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')
    elif "여보세요" in command:
        print("BOT: 안녕?")
    elif "컴퓨터 재시작" in command:
        os.system("shutdown /r /t 1")
    elif "컴퓨터 종료" in command:
        os.system("shutdown /s /t 1")
    elif "컴퓨터 절전" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif "작업 관리자" in command:
        subprocess.run(["./module/script/작업 관리자.bat"], shell=True)
    elif "디스크 정리" in command:
        subprocess.run(["./module/script/디스크 정리.bat"], shell=True)
    elif "이벤트 뷰어" in command:
        subprocess.run(["./module/script/이벤트 뷰어.bat"], shell=True)
    elif "장치 관리자" in command:
        subprocess.run(["./module/script/장치 관리자.bat"], shell=True)
    elif "네트워크 연결" in command:
         subprocess.run(["./module/script/네트워크 연결.bat"], shell=True)
    elif "시스템 정보" in command:
        subprocess.run(["./module/script/시스템 정보.bat"], shell=True)
    elif "설치 프로그램" in command:
        subprocess.run(["./module/script/설치 프로그램.bat"], shell=True)
    elif "방화벽 설정" in command:
        subprocess.run(["./module/script/방화벽 설정.bat"], shell=True)
    elif "윈도우 보안" in command:
        subprocess.run(["./module/script/윈도우 보안.bat"], shell=True)
    elif "전원 옵션" in command:
        subprocess.run(["./module/script/전원 옵션.bat"], shell=True)
    elif "시스템 속성" in command:
        subprocess.run(["./module/script/시스템 속성.bat"], shell=True)
    elif "서비스" in command:
        subprocess.run(["./module/script/서비스.bat"], shell=True)
    elif "성능 모니터" in command:
        subprocess.run(["./module/script/성능 모니터.bat"], shell=True)
    elif "사용자 계정" in command:
        subprocess.run(["./module/script/사용자 계정.bat"], shell=True)
    elif "화면 해상도" in command:
        subprocess.run(["./module/script/화면 해상도.bat"], shell=True)
    elif "프롬프트" in command:
        subprocess.run(["./module/script/프롬프트.bat"], shell=True)
    elif "종료" in command:
        sys.exit()
    else:
        return False
        
    last_commands = command
    recent_commands = command
    return True
