import os
import sys
import subprocess

# 시작 프로그램을 실행하는 함수
def run_program(program_name):
    try:
        # 프로그램 경로가 절대 경로인지 확인하고, 절대 경로가 아니라면 경로를 찾습니다.
        if not os.path.isabs(program_name):
            # 기본 시작 프로그램 경로 설정
            start_menu_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs')
            program_path = None
            for root, dirs, files in os.walk(start_menu_path):
                for file in files:
                    if file.lower() == program_name.lower() + '.lnk':
                        program_path = os.path.join(root, file)
                        break
                if program_path:
                    break
            if program_path is None:
                raise FileNotFoundError(f"프로그램을 찾을 수 없습니다: {program_name}")
        else:
            program_path = program_name

        # 프로그램 실행 (start 명령 사용)
        subprocess.run(['cmd', '/c', 'start', '', program_path], check=False, shell=True)
        print(f"{program_name} 실행 중입니다.")
    except subprocess.CalledProcessError as e:
        print(f"프로그램 실행 중 오류가 발생했습니다: {e}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_program(sys.argv[1])
    else:
        print("프로그램 이름을 명령 줄 인자로 제공해주세요. 예: python [프로그램명].py notepad")
