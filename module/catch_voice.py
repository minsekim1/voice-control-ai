
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
        command = command[len(last_commands):].strip()

    # 음성 명령에 따라 특정 작업 수행
    current_directory = os.path.dirname(os.path.abspath(__file__))
    script_directory = os.path.join(current_directory, "script")  # 정확한 경로 구성
    scripts = load_scripts_from_directory(script_directory)
    for script_name, script_path in scripts.items():
        if script_name in command.lower():
            subprocess.run(["cmd.exe", "/c", script_path], shell=True)
            # print(f"{script_name} script executed.")
            last_commands = command
            recent_commands = command
            return True
        
    if "여보세요" in command:
        print("BOT: 안녕?")
    elif "유튜브" in command:
        webbrowser.open("https://www.youtube.com")
    # elif "유튜브 검색" in command:
    #     # "유튜브 검색" 다음에 오는 텍스트를 검색 쿼리로 추출
    #     query = command.split("유튜브 검색", 1)[1].strip()
    #     # URL 생성
    #     url = f"https://www.youtube.com/results?search_query={query}"
    #     # 웹 브라우저로 URL 열기
    #     webbrowser.open(url)
    #     return True
    elif "네이버" in command:
        webbrowser.open("https://www.naver.com")
    # elif "네이버 검색" in command:
    #     # "네이버 검색" 다음에 오는 텍스트를 검색 쿼리로 추출
    #     query = command.split("유튜브 검색", 1)[1].strip()
    #     # URL 생성
    #     url = f"https://search.naver.com/search.naver?query={query}"
    #     # 웹 브라우저로 URL 열기
    #     webbrowser.open(url)
    #     return True
    elif "구글" in command:
        webbrowser.open("https://www.google.com")
    elif "스크린샷" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')
    elif "종료" in command:
        sys.exit()
    else:
        return False
        
    last_commands = command
    recent_commands = command
    return True

def load_scripts_from_directory(directory):
    """디렉토리에서 스크립트 목록을 로드합니다."""
    scripts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".bat"):
            script_name = filename[:-4]  # 확장자 '.bat' 제거
            scripts[script_name.lower()] = os.path.join(directory, filename)
    return scripts