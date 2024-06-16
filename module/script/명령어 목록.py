import os

def load_scripts_from_directory(directory, parent_prefix=""):
    items = []
    for entry in os.scandir(directory):
        # 폴더 경로를 구성합니다.
        entry_path = f"{parent_prefix}{entry.name}" if parent_prefix else entry.name
        
        if entry.is_file() and entry.name.endswith(".py"):
            # 파일일 경우, 파일명을 리스트에 추가합니다.
            items.append(entry_path)
        elif entry.is_dir():
            # 하위 디렉토리를 재귀적으로 탐색합니다.
            subitems = load_scripts_from_directory(entry.path, parent_prefix=f"{entry_path}/")
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
scripts = load_scripts_from_directory(script_directory)

# 로드된 스크립트와 폴더 목록을 출력합니다.
print_scripts_and_folders(scripts)
