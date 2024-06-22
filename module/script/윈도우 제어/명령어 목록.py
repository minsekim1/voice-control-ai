import os

def get_scripts_from_directory_all(directory, parent_prefix=""):
    items = []
    for entry in os.scandir(directory):
        # 폴더 경로를 구성합니다.
        entry_path = f"{parent_prefix}{entry.name}" if parent_prefix else entry.name
        
        if entry.is_file() and entry.name.endswith(".py"):
            # .bat .sh 추가시 위에 추가하고 catch_voice.py 수정하기
            items.append(entry_path)
        elif entry.is_dir():
            # 하위 디렉토리를 재귀적으로 탐색합니다.
            subitems = get_scripts_from_directory_all(entry.path, parent_prefix=f"{entry_path}/")
            if subitems:
                items.extend(subitems)
            else:
                # 하위 디렉토리가 비어있으면 "명령어 없음"을 추가합니다.
                items.append(f"{entry_path}/명령어 없음")

    return items



def print_scripts_and_folders(scripts):
    # 명령어 목록을 출력합니다.
    scripts.append('(default)종료')
    print("명령어 목록:")
    print(", ".join(scripts))

# 현재 디렉토리 경로를 설정합니다.
current_directory = os.path.dirname(os.path.abspath(__file__))
script_directory = os.path.join(current_directory)  # 스크립트 폴더 경로

# 디렉토리에서 스크립트와 폴더 목록을 로드합니다.
scripts = get_scripts_from_directory_all(script_directory)

# 로드된 스크립트와 폴더 목록을 출력합니다.
print_scripts_and_folders(scripts)


# 출력 예시
# 명령어 목록:
# 계산기.py, 구글/검색.py, 구글/열기.py, 구글/취소.py, 네이버/검색.py, 네이버/열기.py, 네이버/취소.py, 네트워크 연결.py, 디스크 정리.py, 메모장.py, 
# 명령어 목록.py, 방화벽 설정.py, 사용자 계정.py, 설치 프로그램.py, 성능모니터.py, 스크린샷.py, 시스템 정보.py, 시스템속성.py, 여보세요.py, 윈도우 보안.py, 
# 윈도우 서비스.py, 윈도우 프롬프트.py, 유튜브/검색.py, 유튜브/열기.py, 유튜브/취소.py, 이벤트뷰어.py, 작업 관리자.py, 장치관리자.py, 전원옵션.py, 
# 컴퓨터 재시작.py, 컴퓨터 절전.py, 컴퓨터 종료.py, 화면 해상도.py, (default)종료
