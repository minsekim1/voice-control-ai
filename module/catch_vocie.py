
import os
import sys
import pyautogui

# 음성인식을 진행합니다.
def execute_command(command):
    # 음성 명령에 따라 특정 작업 수행
    if "메모장" in command:
        os.system("notepad")
        return True
    elif "계산기" in command:
        os.system("calc")
        return True
    elif "스크린샷" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')
        return True
    elif "여보세요" in command:
        print("BOT: 안녕?")
        return True
    elif "종료" in command:
        print("BOT: 프로그램을 종료합니다.")
        sys.exit()  # 프로그램 종료
        return True
    else :
    		return False
