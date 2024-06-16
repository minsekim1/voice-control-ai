
import os
import subprocess
import sys

# 최근 실행된 명령어를 저장
recent_commands = ""
last_commands = ""


def list_files_and_folders(directory):
    """주어진 디렉토리 내의 파일과 폴더의 이름 및 절대 경로를 딕셔너리로 반환합니다."""
    items = {}  # 딕셔너리로 초기화
    for entry in os.scandir(directory):

        # 파일 이름에서 확장자를 제거합니다.
        script_name, _ = os.path.splitext(entry.name)
        script_path = os.path.join(directory, entry.name)  # 파일의 전체 경로

        # 파일인 경우
        if entry.is_file():
            items[script_name.lower()] = script_path  # 이름을 키로, 경로를 값으로 저장

        # 폴더인 경우
        elif entry.is_dir():
            items[script_name.lower()] = "folder"
    return items

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
    # 디렉토리에서 스크립트와 폴더 목록을 로드합니다.
    scripts = list_files_and_folders(script_directory)

    print("scripts",scripts)
    for script_name, script_path in scripts.items():
        if script_name in command.lower():
            # .bat .sh 추가시 위에 추가하고 load_scripts_from_directory.py 수정하기
            subprocess.run(["python", script_path], shell=True)
            print(f"{script_name} script executed.")
            last_commands = command
            recent_commands = command
            return True
       
    # 종료만 따로 처리
    if "종료" in command:
        sys.exit()
    
    # 명령어 없을때 처리
    return False


# execute_command("테스트")

