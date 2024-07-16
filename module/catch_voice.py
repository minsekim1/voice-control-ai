
import os
import subprocess
import sys
import re  # 정규 표현식 모듈 추가


# 이전 음성 글자들을 포함해서 음성인식
before_voice_text = ""

# 음성 단계(폴더 위치)를 저장
read_folder = []

# debug mode
debug_mode = False

def list_files_and_folders(read_folder):
    """주어진 디렉토리 내의 파일과 폴더의 이름 및 절대 경로를 딕셔너리로 반환합니다."""

    # 음성 명령에 따라 특정 작업 수행
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # 폴더 리스트를 사용하여 경로를 동적으로 구성
    script_directory = os.path.join(current_directory, "script", *read_folder)
    items = {}  # 딕셔너리로 초기화

    for entry in os.scandir(script_directory):
        # 파일 이름에서 확장자를 제거합니다.
        script_name, _ = os.path.splitext(entry.name)
        script_path = os.path.join(script_directory, entry.name)  # 파일의 전체 경로

        # 파일인 경우
        if entry.is_file():
            items[script_name.lower()] = script_path  # 이름을 키로, 경로를 값으로 저장
        # 폴더인 경우
        elif entry.is_dir():
            items[script_name.lower()] = "folder"
    
    # 현재 위치가 폴더일 경우 "뒤로가기" 옵션을 추가할 조건 확인
    if len(read_folder) > 0:
        items["뒤로 가기"] = "Back"

    return items

# 음성인식을 진행합니다.
def execute_command(voice_text):
    # 전역 변수 사용
    global before_voice_text
    global read_folder

    # 디렉토리에서 스크립트와 폴더 목록을 로드합니다.
    voice_text = before_voice_text + voice_text
    before_voice_text = voice_text
    scripts = list_files_and_folders(read_folder)

    # 일반 파일(명령어) / 폴더(경로 들어가기) 실행
    if debug_mode == True : print("일반 파일(명령어) / 폴더(경로 들어가기) 실행")
    for key, value in scripts.items():
        if key in voice_text.lower():
            if scripts[key] == "folder":
                read_folder.append(key)  # 폴더 선택 시 폴더 경로 추가
                print(f"\n> 명령어 경로 선택: \"{key}\"\n")

                # 폴더 리스트를 사용하여 경로를 동적으로 구성
                scripts = list_files_and_folders(read_folder)
                # 폴더 내 스크립트와 폴더를 목록으로 표시
                print(f"다음 명령어를 선택해주세요:\n> 현재 경로: {"./module/script/"+"/".join(read_folder)}")
                for idx, (key, value) in enumerate(scripts.items(), 1):
                    print(f"{idx}. {key.capitalize()}")
                before_voice_text = ""
                return True
            elif value == "Back":
                if read_folder:
                    read_folder.pop()  # "뒤로가기" 선택 시 마지막 폴더를 제거
                print(f"\n이전 경로로 돌아갑니다.\n> 현재 경로: {"./module/script/"+"/".join(read_folder)}")
                before_voice_text = ""
                return True
            elif ".py" in value:
                # .py 일경우 실행
                subprocess.run(["python", value], shell=True)
                print(f"> \"{key}\" 을(를) 실행합니다.\n")
                before_voice_text = ""
                return True
            else :
                print(f"{value} no unavailable file.")
                before_voice_text = ""
                return False
            
    # 파일 / 폴더 없을 경우
    # 현재 폴더 경로 내에 [검색어].py 같이 대괄호로 끝나는 파일이 있으면 파라미터로 넣어서 실행하기
    if debug_mode == True : print("파일 / 폴더 없을 경우")
    if debug_mode == True : print(f"read_folder len:{len(read_folder)}")
    if len(read_folder) > 0:
        # 대괄호로 끝나는 파일 검색 및 실행
        pattern = re.compile(r'\[.*\]$')
        for key, value in scripts.items():
            if debug_mode == True : print(f"k:{key}, v:{value}")
            if pattern.match(key):
                # 패턴 (대괄호) 파일이 존재할 경우 확장자에 맞춰서 실행하기.
                if ".py" in value :
                    subprocess.run(["python", value, voice_text], shell=True)
                    print(f"> \"{key}\" 을(를) 실행합니다.\n")
                    read_folder = []
                    before_voice_text = ""
                    return True

    # 종료만 따로 처리
    if "종료" in voice_text:
        sys.exit()
    
    # 명령어 없을때 처리
    return False


