import os
import datetime
import pyautogui

# 프로젝트의 루트 디렉토리를 얻습니다.
root_path = os.path.dirname(os.path.abspath(__file__))

# 스크린샷을 저장할 폴더 경로를 설정합니다.
# 뒤로가기 두번 실행
screenshot_directory = os.path.join(root_path, '../..', 'asset', 'screenshot')

# 폴더가 없으면 생성합니다.
if not os.path.exists(screenshot_directory):
    os.makedirs(screenshot_directory)

# 오늘 날짜를 파일 이름으로 사용합니다.
date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"screenshot_{date_string}.png"
file_path = os.path.join(screenshot_directory, filename)

# 스크린샷을 찍고 저장합니다.
screenshot = pyautogui.screenshot()
screenshot.save(file_path)

print(f"Screenshot saved to {file_path}")
