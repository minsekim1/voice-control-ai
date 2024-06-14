
import os
import sys
import pyautogui
import webbrowser  # 웹 브라우저를 제어하기 위한 모듈

# 최근 실행된 명령어를 저장
recent_commands = ""

# 음성인식을 진행합니다.
def execute_command(command):
    global recent_commands  # 전역 변수 사용

    # 명령어가 최근 실행된 명령어 세트에 있는지 확인
    if command == recent_commands:
        return False

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
    elif "컴퓨 절전" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif "작업 관리자" in command:
        os.system("taskmgr")
    elif "디스크 정리" in command:
        os.system("cleanmgr")
    elif "이벤트 뷰어" in command:
        os.system("eventvwr.msc")
    elif "장치 관리자" in command:
        os.system("devmgmt.msc")
    elif "네트워크 연결" in command:
        os.system("ncpa.cpl")
    elif "시스템 정보" in command:
        os.system("msinfo32")
    elif "프로그램 추가/제거" in command:
        os.system("appwiz.cpl")
    elif "방화벽 설정" in command:
        os.system("firewall.cpl")
    elif "보안 및 유지관리" in command:
        os.system("wscui.cpl")
    elif "전원 옵션" in command:
        os.system("powercfg.cpl")
    elif "시스템 속성" in command:
        os.system("sysdm.cpl")
    elif "서비스" in command:
        os.system("services.msc")
    elif "성능 모니터" in command:
        os.system("perfmon.msc")
    elif "사용자 계정" in command:
        os.system("control userpasswords2")
    elif "화면 해상도" in command:
        os.system("desk.cpl")
    elif "커맨드 프롬프트" in command:
        os.system("cmd")
    elif "종료" in command:
        sys.exit()
    else:
        return False
    recent_commands = command
    return True
